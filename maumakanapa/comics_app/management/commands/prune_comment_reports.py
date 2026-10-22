from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from comics_app.models import CommentModerationEvent, CommentReport, EpisodeComment
from comics_app.services import record_moderation_event


class Command(BaseCommand):
    help = 'Remove comment reports older than COMMENT_REPORT_RETENTION_DAYS.'

    @transaction.atomic
    def handle(self, *args, **options):
        retention_days = settings.COMMENT_REPORT_RETENTION_DAYS
        if retention_days < 1:
            raise ValueError('COMMENT_REPORT_RETENTION_DAYS must be at least 1.')
        cutoff = timezone.now() - timedelta(days=retention_days)
        expired = CommentReport.objects.filter(created_at__lt=cutoff)
        comment_ids = list(expired.values_list('comment_id', flat=True).distinct())
        for comment in EpisodeComment.objects.filter(pk__in=comment_ids):
            count = expired.filter(comment=comment).count()
            record_moderation_event(
                comment,
                CommentModerationEvent.Action.REPORTS_PRUNED,
                details={'report_count': count, 'cutoff': cutoff.isoformat()},
            )
        deleted_count, _ = expired.delete()
        still_reported = CommentReport.objects.filter(
            comment_id__in=comment_ids
        ).values_list('comment_id', flat=True)
        EpisodeComment.objects.filter(pk__in=comment_ids).exclude(
            pk__in=still_reported
        ).update(is_reported=False)
        self.stdout.write(
            self.style.SUCCESS(
                f'Removed {deleted_count} expired report-related record(s).'
            )
        )
