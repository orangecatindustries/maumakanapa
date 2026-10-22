from io import BytesIO, StringIO
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from types import SimpleNamespace

from django.core.cache import cache
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Group
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import salted_hmac
from PIL import Image

from .forms import MAX_COMMENT_IMAGE_SIZE
from .models import (
    CommentLike,
    CommentModerationEvent,
    CommentReport,
    EpisodeComment,
    webcomic,
)
from .services import (
    attach_anonymous_comments_to_user,
    claim_browser_comments_for_authenticated_user,
)


@override_settings(COMPRESS_ENABLED=False)
class EpisodeCommentTests(TestCase):
    def setUp(self):
        cache.clear()
        self.comic = webcomic.objects.create(
            language='english', ep_number=1, title='Test episode'
        )
        self.page_url = reverse('page', kwargs={'lang': 'english', 'number': 1})
        self.create_url = reverse('comment_create', kwargs={'lang': 'english', 'number': 1})

    def make_comment(self, client=None, **fields):
        client = client or self.client
        response = client.post(self.create_url, {'body': 'A test comment', **fields})
        self.assertEqual(response.status_code, 302)
        return EpisodeComment.objects.latest('pk')

    def test_episode_page_renders_discussion_and_empty_state(self):
        response = self.client.get(self.page_url)

        self.assertContains(response, 'Episode discussion')
        self.assertContains(response, 'Jump to episode discussion')
        self.assertContains(response, 'No comments yet.')

    def test_anonymous_comment_and_reply_are_saved(self):
        parent = self.make_comment()
        reply = self.make_comment(parent_id=parent.pk, body='A reply')

        self.assertEqual(reply.parent_id, parent.pk)
        self.assertEqual(reply.display_name, 'Anonymous')
        self.assertEqual(reply.owner_key, parent.owner_key)
        self.assertIsNone(parent.edited_at)
        self.assertIsNone(reply.edited_at)
        self.assertContains(self.client.get(self.page_url), 'A reply')

    def test_owner_can_edit_and_delete_but_another_session_cannot(self):
        comment = self.make_comment()
        edit_url = reverse(
            'comment_edit',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        delete_url = reverse(
            'comment_delete',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )

        self.assertIsNone(comment.edited_at)
        self.assertNotContains(self.client.get(self.page_url), '(edited)')
        self.client.post(edit_url, {'body': 'Edited comment'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Edited comment')
        self.assertIsNotNone(comment.edited_at)
        self.assertContains(self.client.get(self.page_url), '(edited)')

        other_client = Client()
        other_client.post(edit_url, {'body': 'Unauthorized edit'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Edited comment')

        other_client.post(delete_url)
        self.assertTrue(EpisodeComment.objects.filter(pk=comment.pk).exists())

        self.client.post(delete_url)
        self.assertFalse(EpisodeComment.objects.filter(pk=comment.pk).exists())

    def test_anonymous_ownership_cookie_survives_a_new_browser_session(self):
        page_response = self.client.get(self.page_url)
        ownership_cookie = page_response.cookies['comment_owner']
        self.assertTrue(ownership_cookie['httponly'])
        self.assertEqual(ownership_cookie['samesite'], 'Lax')
        comment = self.make_comment()

        returning_browser = Client()
        returning_browser.cookies['comment_owner'] = ownership_cookie.value
        self.assertContains(returning_browser.get(self.page_url), 'Edit')
        edit_url = reverse(
            'comment_edit',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        returning_browser.post(edit_url, {'body': 'Edited from a new session'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Edited from a new session')

    def test_anonymous_comments_can_be_claimed_by_a_future_account(self):
        comment = self.make_comment()
        account = get_user_model().objects.create_user(
            username='future-member',
            password='test-password',
        )

        claimed_count = attach_anonymous_comments_to_user(comment.owner_key, account)

        self.assertEqual(claimed_count, 1)
        comment.refresh_from_db()
        self.assertEqual(comment.author, account)
        account_client = Client()
        account_client.force_login(account)
        edit_url = reverse(
            'comment_edit',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        account_client.post(edit_url, {'body': 'Account-owned comment'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Account-owned comment')
        self.assertEqual(
            attach_anonymous_comments_to_user(comment.owner_key, account),
            0,
        )

    def test_legacy_session_owned_comments_migrate_to_persistent_cookie(self):
        session = self.client.session
        session['legacy_session'] = True
        session.save()
        self.client.cookies['sessionid'] = session.session_key
        legacy_key = salted_hmac(
            'episode-comment-owner',
            session.session_key,
        ).hexdigest()
        comment = EpisodeComment.objects.create(
            webcomic=self.comic,
            body='A comment from before the persistent owner cookie.',
            owner_key=legacy_key,
        )
        like = CommentLike.objects.create(comment=comment, owner_key=legacy_key)
        report = CommentReport.objects.create(
            comment=comment,
            reporter_key=legacy_key,
            reason='A report from the legacy session.',
        )

        response = self.client.get(self.page_url)

        comment.refresh_from_db()
        new_token = response.cookies['comment_owner'].value
        persistent_key = salted_hmac(
            'episode-comment-owner-cookie',
            new_token,
        ).hexdigest()
        self.assertEqual(comment.owner_key, persistent_key)
        like.refresh_from_db()
        report.refresh_from_db()
        self.assertEqual(like.owner_key, persistent_key)
        self.assertEqual(report.reporter_key, persistent_key)
        self.assertContains(response, 'Edit')

    def test_future_account_claim_uses_server_side_cookie_identity(self):
        response = self.client.get(self.page_url)
        comment = self.make_comment()
        account = get_user_model().objects.create_user(
            username='cookie-claim-member',
            password='test-password',
        )
        request = SimpleNamespace(
            user=account,
            COOKIES={'comment_owner': response.cookies['comment_owner'].value},
        )

        self.assertEqual(claim_browser_comments_for_authenticated_user(request), 1)
        comment.refresh_from_db()
        self.assertEqual(comment.author, account)

    def test_comment_moderator_group_has_limited_admin_access_and_queue(self):
        comment = self.make_comment(body='Waiting for review.')
        comment.is_reported = True
        comment.save(update_fields=['is_reported'])
        call_command('setup_comment_moderators', stdout=StringIO())
        moderator = get_user_model().objects.create_user(
            username='limited-moderator',
            password='test-password',
            is_staff=True,
        )
        moderator.groups.add(Group.objects.get(name='Comment moderators'))
        admin_client = Client()
        admin_client.force_login(moderator)

        queue_url = reverse(
            'admin:comics_app_episodecomment_moderation_queue'
        )
        queue_response = admin_client.get(queue_url)
        self.assertContains(queue_response, 'Waiting for review.')
        self.assertContains(
            queue_response,
            'Reported or automatically held comments awaiting moderator attention.',
        )
        detail_response = admin_client.get(
            reverse(
                'admin:comics_app_episodecomment_change',
                args=[comment.pk],
            )
        )
        self.assertContains(detail_response, 'name=is_approved')
        self.assertNotContains(detail_response, 'name=body')
        self.assertEqual(
            admin_client.get(
                reverse(
                    'admin:comics_app_episodecomment_add'
                )
            ).status_code,
            403,
        )

    def test_moderation_actions_are_logged(self):
        comment = self.make_comment()
        report_url = reverse(
            'comment_report',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        self.client.post(report_url, {'reason': 'Please review this comment.'})
        moderator = get_user_model().objects.create_superuser(
            username='audit-moderator',
            email='audit@example.com',
            password='test-password',
        )
        admin_client = Client()
        admin_client.force_login(moderator)
        report_list_url = reverse('admin:comics_app_commentreport_changelist')
        admin_client.post(
            report_list_url,
            {
                'action': 'dismiss_selected_reports',
                '_selected_action': [str(comment.reports.get().pk)],
                'index': '0',
            },
        )
        event = CommentModerationEvent.objects.get(
            action=CommentModerationEvent.Action.REPORTS_DISMISSED
        )
        self.assertEqual(event.comment_id_snapshot, comment.pk)
        self.assertEqual(event.actor, moderator)
        self.assertEqual(event.details, {'report_count': 1})

    def test_staff_comments_show_verified_badge_and_use_account_ownership(self):
        staff_user = get_user_model().objects.create_user(
            username='episode-staff',
            password='test-password',
            is_staff=True,
        )
        staff_client = Client()
        staff_client.force_login(staff_user)
        staff_client.post(
            self.create_url,
            {'display_name': 'Fake name', 'body': 'Official staff update.'},
        )
        comment = EpisodeComment.objects.latest('pk')

        self.assertEqual(comment.author, staff_user)
        self.assertEqual(comment.display_name, 'episode-staff')
        response = self.client.get(self.page_url)
        self.assertContains(response, '[STAFF]')
        self.assertContains(response, 'episode-staff')
        staff_page = staff_client.get(self.page_url)
        self.assertContains(staff_page, 'will show the [STAFF] badge')
        self.assertContains(staff_page, 'Post as Anonymous')
        self.assertNotContains(staff_page, 'id_display_name')

        edit_url = reverse(
            'comment_edit',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        delete_url = reverse(
            'comment_delete',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        another_browser = Client()
        another_browser.post(edit_url, {'body': 'Unauthorized change'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Official staff update.')

        same_staff_account = Client()
        same_staff_account.force_login(staff_user)
        same_staff_account.post(edit_url, {'body': 'Updated staff announcement.'})
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'Updated staff announcement.')

        another_browser.post(delete_url)
        self.assertTrue(EpisodeComment.objects.filter(pk=comment.pk).exists())
        same_staff_account.post(delete_url)
        self.assertFalse(EpisodeComment.objects.filter(pk=comment.pk).exists())

    def test_staff_can_post_anonymously_while_retaining_staff_badge(self):
        staff_user = get_user_model().objects.create_user(
            username='anonymous-staff',
            password='test-password',
            is_staff=True,
        )
        staff_client = Client()
        staff_client.force_login(staff_user)
        staff_client.post(
            self.create_url,
            {'body': 'Staff note without my username.', 'post_anonymously': 'on'},
        )
        comment = EpisodeComment.objects.latest('pk')

        self.assertEqual(comment.author, staff_user)
        self.assertEqual(comment.display_name, 'Anonymous')
        response = self.client.get(self.page_url)
        self.assertContains(response, 'Anonymous')
        self.assertContains(response, '[STAFF]')
        self.assertNotContains(response, 'anonymous-staff')

    def test_anonymous_display_name_cannot_claim_staff_badge(self):
        response = self.client.post(
            self.create_url,
            {'display_name': 'Volunteer [STAFF]', 'body': 'A regular comment.'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(EpisodeComment.objects.exists())
        self.assertContains(
            self.client.get(self.page_url),
            'Only verified staff accounts can use the [STAFF] label.',
        )

    def test_like_and_report_are_one_per_session(self):
        comment = self.make_comment()
        url_args = {'lang': 'english', 'number': 1, 'comment_id': comment.pk}
        like_url = reverse('comment_like', kwargs=url_args)
        report_url = reverse('comment_report', kwargs=url_args)

        self.client.post(like_url)
        self.client.post(like_url)
        self.client.post(report_url, {'reason': 'This is a duplicate report reason.'})
        self.client.post(report_url, {'reason': 'Updated report details.'})

        self.assertEqual(CommentLike.objects.filter(comment=comment).count(), 0)
        self.assertEqual(CommentReport.objects.filter(comment=comment).count(), 1)
        comment.refresh_from_db()
        self.assertTrue(comment.is_reported)
        self.assertTrue(comment.is_approved)
        self.assertEqual(comment.reports.get().reason, 'Updated report details.')
        self.assertContains(self.client.get(self.page_url), 'A test comment')

    def test_moderator_can_review_reported_comment_without_bulk_approve_action(self):
        comment = self.make_comment()
        report_url = reverse(
            'comment_report',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        self.client.post(report_url, {'reason': 'This comment looks inappropriate.'})
        comment.refresh_from_db()
        self.assertTrue(comment.is_approved)
        self.assertTrue(comment.is_reported)
        self.assertEqual(comment.reports.get().reason, 'This comment looks inappropriate.')

        moderator = get_user_model().objects.create_superuser(
            username='moderator',
            email='moderator@example.com',
            password='test-password',
        )
        admin_client = Client()
        admin_client.force_login(moderator)
        self.assertContains(
            admin_client.get(
                reverse(
                    'admin:comics_app_episodecomment_change',
                    args=[comment.pk],
                )
            ),
            'This comment looks inappropriate.',
        )
        changelist = admin_client.get(
            reverse('admin:comics_app_episodecomment_changelist')
        )
        self.assertNotContains(changelist, 'Approve selected comments')
        self.assertContains(changelist, 'Delete selected comments and replies')
        comment.refresh_from_db()
        self.assertTrue(comment.is_approved)
        self.assertTrue(comment.is_reported)
        self.assertContains(self.client.get(self.page_url), 'A test comment')

    def test_admin_can_delete_flagged_comment_and_its_replies(self):
        comment = self.make_comment()
        reply = self.make_comment(parent_id=comment.pk, body='A reply to review.')
        self.client.post(
            reverse(
                'comment_report',
                kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
            ),
            {'reason': 'This post needs moderator review.'},
        )
        moderator = get_user_model().objects.create_superuser(
            username='delete-moderator',
            email='moderator@example.com',
            password='test-password',
        )
        admin_client = Client()
        admin_client.force_login(moderator)
        report_list_url = reverse('admin:comics_app_commentreport_changelist')

        self.assertContains(
            admin_client.get(report_list_url),
            'Delete reported comment(s) and replies',
        )
        self.assertContains(
            admin_client.get(report_list_url),
            reverse('admin:comics_app_episodecomment_change', args=[comment.pk]),
        )
        response = admin_client.post(
            report_list_url,
            {
                'action': 'delete_reported_comments',
                '_selected_action': [str(comment.reports.get().pk)],
                'index': '0',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(EpisodeComment.objects.filter(pk=comment.pk).exists())
        self.assertFalse(EpisodeComment.objects.filter(pk=reply.pk).exists())
        self.assertFalse(CommentReport.objects.filter(comment_id=comment.pk).exists())
        deletion_event = CommentModerationEvent.objects.get(
            action=CommentModerationEvent.Action.COMMENT_DELETED,
            comment_id_snapshot=comment.pk,
        )
        self.assertEqual(deletion_event.actor, moderator)

    def test_admin_can_dismiss_non_rule_breaking_report_without_deleting_comment(self):
        comment = self.make_comment(body='A harmless comment.')
        reporter_one = Client()
        reporter_two = Client()
        report_url = reverse(
            'comment_report',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )
        reporter_one.post(report_url, {'reason': 'I disagree with this opinion.'})
        reporter_two.post(report_url, {'reason': 'This is not against the rules.'})

        moderator = get_user_model().objects.create_superuser(
            username='dismiss-moderator',
            email='moderator@example.com',
            password='test-password',
        )
        admin_client = Client()
        admin_client.force_login(moderator)
        report_list_url = reverse('admin:comics_app_commentreport_changelist')
        report_ids = list(comment.reports.values_list('pk', flat=True))

        self.assertContains(
            admin_client.get(report_list_url),
            'Dismiss selected reports (keep comments)',
        )
        response = admin_client.post(
            report_list_url,
            {
                'action': 'dismiss_selected_reports',
                '_selected_action': [str(report_ids[0])],
                'index': '0',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(EpisodeComment.objects.filter(pk=comment.pk).exists())
        self.assertEqual(comment.reports.count(), 1)
        comment.refresh_from_db()
        self.assertTrue(comment.is_reported)

        admin_client.post(
            report_list_url,
            {
                'action': 'dismiss_selected_reports',
                '_selected_action': [str(report_ids[1])],
                'index': '0',
            },
        )
        comment.refresh_from_db()
        self.assertTrue(EpisodeComment.objects.filter(pk=comment.pk).exists())
        self.assertFalse(comment.is_reported)
        self.assertContains(self.client.get(self.page_url), 'A harmless comment.')

    def test_report_requires_a_reason(self):
        comment = self.make_comment()
        report_url = reverse(
            'comment_report',
            kwargs={'lang': 'english', 'number': 1, 'comment_id': comment.pk},
        )

        self.client.post(report_url, {'reason': '   '})

        self.assertFalse(CommentReport.objects.filter(comment=comment).exists())
        comment.refresh_from_db()
        self.assertFalse(comment.is_reported)
        self.assertContains(self.client.get(self.page_url), 'This field is required.')

    def test_expired_reports_are_pruned_without_retaining_report_text(self):
        comment = self.make_comment()
        report = CommentReport.objects.create(
            comment=comment,
            reporter_key='reporter-key',
            reason='Sensitive report text should expire.',
        )
        CommentReport.objects.filter(pk=report.pk).update(
            created_at=timezone.now() - timedelta(days=400)
        )
        EpisodeComment.objects.filter(pk=comment.pk).update(is_reported=True)

        call_command(
            'prune_comment_reports',
            stdout=StringIO(),
        )

        self.assertFalse(CommentReport.objects.filter(pk=report.pk).exists())
        comment.refresh_from_db()
        self.assertFalse(comment.is_reported)
        event = CommentModerationEvent.objects.get(
            action=CommentModerationEvent.Action.REPORTS_PRUNED,
            comment_id_snapshot=comment.pk,
        )
        self.assertEqual(event.details['report_count'], 1)
        self.assertNotIn('Sensitive report text', event.comment_snapshot)

    def test_automatic_screening_holds_suspicious_comments_for_moderation(self):
        comment = self.make_comment(body='You are a piece of shit.')
        self.assertFalse(comment.is_approved)
        self.assertEqual(comment.moderation_reason, 'Possible profanity')
        self.assertNotContains(self.client.get(self.page_url), 'piece of shit')
        moderator = get_user_model().objects.create_superuser(
            username='screening-moderator',
            email='moderator@example.com',
            password='test-password',
        )
        admin_client = Client()
        admin_client.force_login(moderator)
        self.assertContains(
            admin_client.get(reverse('admin:comics_app_episodecomment_changelist')),
            'Possible profanity',
        )

        comment_admin_url = reverse(
            'admin:comics_app_episodecomment_change',
            args=[comment.pk],
        )
        detail_response = admin_client.get(comment_admin_url)
        self.assertContains(detail_response, 'name=is_approved')
        response = admin_client.post(
            comment_admin_url,
            {
                'display_name': comment.display_name,
                'webcomic': str(comment.webcomic_id),
                'parent': '',
                'body': comment.body,
                'image': '',
                'is_approved': 'on',
                'reports-TOTAL_FORMS': '0',
                'reports-INITIAL_FORMS': '0',
                'reports-MIN_NUM_FORMS': '0',
                'reports-MAX_NUM_FORMS': '1000',
                '_save': 'Save',
            },
        )
        comment.refresh_from_db()
        self.assertTrue(comment.is_approved)
        self.assertEqual(comment.moderation_reason, 'Possible profanity')
        self.assertContains(self.client.get(self.page_url), 'piece of shit')
        self.assertTrue(
            CommentModerationEvent.objects.filter(
                action=CommentModerationEvent.Action.APPROVED,
                comment_id_snapshot=comment.pk,
                actor=moderator,
            ).exists()
        )

    def test_ordinary_comment_is_published_and_available_in_admin(self):
        comment = self.make_comment(body='I enjoyed this episode.')

        self.assertTrue(comment.is_approved)
        self.assertContains(self.client.get(self.page_url), 'I enjoyed this episode.')
        moderator = get_user_model().objects.create_superuser(
            username='ordinary-comment-moderator',
            email='moderator@example.com',
            password='test-password',
        )
        admin_client = Client()
        admin_client.force_login(moderator)
        self.assertContains(
            admin_client.get(reverse('admin:comics_app_episodecomment_changelist')),
            'I enjoyed this episode.',
        )

    def test_only_supported_image_files_are_accepted(self):
        image_data = BytesIO()
        Image.new('RGB', (3, 3), color='red').save(image_data, format='GIF')
        valid_gif = SimpleUploadedFile(
            'small.gif', image_data.getvalue(), content_type='image/gif'
        )
        self.client.post(self.create_url, {'body': '', 'image': valid_gif})
        self.assertEqual(EpisodeComment.objects.count(), 1)
        self.assertTrue(EpisodeComment.objects.get().image.name.endswith('.gif'))

        fake_video = SimpleUploadedFile(
            'clip.mp4', b'not an image', content_type='video/mp4'
        )
        self.client.post(self.create_url, {'body': 'No video', 'image': fake_video})
        self.assertEqual(EpisodeComment.objects.count(), 1)

        oversized_gif = SimpleUploadedFile(
            'large.gif',
            image_data.getvalue() + b'\0' * MAX_COMMENT_IMAGE_SIZE,
            content_type='image/gif',
        )
        self.client.post(self.create_url, {'body': 'Too large', 'image': oversized_gif})
        self.assertEqual(EpisodeComment.objects.count(), 1)

    def test_new_comments_are_rate_limited(self):
        for number in range(5):
            self.client.post(self.create_url, {'body': f'Comment {number}'})
        self.client.post(self.create_url, {'body': 'Too many'})

        self.assertEqual(EpisodeComment.objects.count(), 5)
        response = self.client.get(self.page_url)
        self.assertContains(response, "You're posting too quickly.")


class BackupCommandTests(TransactionTestCase):
    def test_backup_command_archives_sqlite_database_and_media(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            media_root = root / 'media'
            media_root.mkdir()
            (media_root / 'sample.txt').write_text('sample media', encoding='utf-8')
            output = root / 'backup.zip'
            with override_settings(MEDIA_ROOT=media_root):
                call_command('backup_site_data', str(output), stdout=StringIO())

            with ZipFile(output) as archive:
                self.assertIn('database.sqlite3', archive.namelist())
                self.assertIn('manifest.json', archive.namelist())
                self.assertEqual(archive.read('media/sample.txt'), b'sample media')
