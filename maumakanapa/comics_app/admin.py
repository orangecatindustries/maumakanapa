import re
from django import forms
from django.contrib import admin
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from .forms import CommentImageValidationMixin
from .models import (
    CommentModerationEvent,
    CommentReport,
    EpisodeComment,
    comicPage,
    webcomic,
)
from .services import record_moderation_event


def clear_reported_flag_without_reports(comment_ids):
    still_reported_ids = CommentReport.objects.filter(
        comment_id__in=comment_ids
    ).values_list('comment_id', flat=True)
    EpisodeComment.objects.filter(pk__in=comment_ids).exclude(
        pk__in=still_reported_ids
    ).update(is_reported=False)


class EpisodeCommentAdminForm(CommentImageValidationMixin, forms.ModelForm):
    class Meta:
        model = EpisodeComment
        fields = '__all__'


class CommentReportInline(admin.TabularInline):
    model = CommentReport
    extra = 0
    readonly_fields = ('reason', 'reporter_key', 'created_at')
    fields = ('reason', 'reporter_key', 'created_at')
    can_delete = False


@admin.register(EpisodeComment)
class EpisodeCommentAdmin(admin.ModelAdmin):
    form = EpisodeCommentAdminForm
    list_display = (
        'display_name', 'author', 'comment_preview', 'webcomic', 'created_at', 'is_reported',
        'is_approved', 'moderation_reason',
    )
    list_filter = ('is_approved', 'is_reported', 'webcomic__language')
    search_fields = ('display_name', 'body', 'webcomic__title')
    readonly_fields = (
        'owner_key', 'author', 'created_at', 'updated_at', 'edited_at', 'is_reported',
        'moderation_reason',
    )
    inlines = (CommentReportInline,)
    actions = ('delete_selected_comments',)
    change_list_template = 'admin/comics_app/episodecomment/change_list.html'

    def get_urls(self):
        return [
            path(
                'moderation-queue/',
                self.admin_site.admin_view(self.moderation_queue_view),
                name='comics_app_episodecomment_moderation_queue',
            ),
            *super().get_urls(),
        ]

    def moderation_queue_view(self, request):
        if not self.has_view_or_change_permission(request):
            return HttpResponseForbidden()
        queue = (
            self.get_queryset(request)
            .filter(Q(is_reported=True) | Q(is_approved=False))
            .prefetch_related('reports')
            .order_by('created_at', 'pk')
        )
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Comment moderation queue',
            'comments': queue,
            'media': self.media,
        }
        return TemplateResponse(
            request,
            'admin/comics_app/episodecomment/moderation_queue.html',
            context,
        )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if (
            not request.user.is_superuser
            and request.user.groups.filter(name='Comment moderators').exists()
        ):
            readonly.extend(
                field.name
                for field in self.model._meta.fields
                if field.name != 'is_approved' and field.name not in readonly
            )
        return readonly

    def has_add_permission(self, request):
        if (
            not request.user.is_superuser
            and request.user.groups.filter(name='Comment moderators').exists()
        ):
            return False
        return super().has_add_permission(request)

    @admin.display(description='Comment')
    def comment_preview(self, obj):
        return obj.body[:120] or ('[image attachment]' if obj.image else '[empty]')

    @admin.action(description='Delete selected comments and replies')
    def delete_selected_comments(self, request, queryset):
        comments = list(queryset)
        for comment in comments:
            record_moderation_event(
                comment,
                CommentModerationEvent.Action.COMMENT_DELETED,
                actor=request.user,
                details={'source': 'episode_comments_admin'},
            )
        count, _ = queryset.delete()
        self.message_user(request, f'{count} comment-related record(s) deleted.')

    def save_model(self, request, obj, form, change):
        previous_approved = None
        if change:
            previous_approved = EpisodeComment.objects.only('is_approved').get(
                pk=obj.pk
            ).is_approved
        super().save_model(request, obj, form, change)
        if change and previous_approved != obj.is_approved:
            action = (
                CommentModerationEvent.Action.APPROVED
                if obj.is_approved
                else CommentModerationEvent.Action.UNAPPROVED
            )
            record_moderation_event(obj, action, actor=request.user)

    def delete_model(self, request, obj):
        record_moderation_event(
            obj,
            CommentModerationEvent.Action.COMMENT_DELETED,
            actor=request.user,
            details={'source': 'episode_comment_admin'},
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for comment in queryset.iterator():
            record_moderation_event(
                comment,
                CommentModerationEvent.Action.COMMENT_DELETED,
                actor=request.user,
                details={'source': 'episode_comments_admin'},
            )
        super().delete_queryset(request, queryset)


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ('comment_link', 'reason', 'created_at')
    readonly_fields = ('comment', 'reporter_key', 'created_at')
    search_fields = ('comment__body', 'reason', 'comment__display_name')
    actions = ('dismiss_selected_reports', 'delete_reported_comments')

    @admin.display(description='Reported comment')
    def comment_link(self, obj):
        url = reverse(
            'admin:comics_app_episodecomment_change',
            args=[obj.comment_id],
        )
        return format_html('<a href="{}">{}</a>', url, obj.comment)

    def delete_model(self, request, obj):
        comment_id = obj.comment_id
        record_moderation_event(
            obj.comment,
            CommentModerationEvent.Action.REPORTS_DELETED,
            actor=request.user,
            details={'report_count': 1, 'source': 'comment_report_admin'},
        )
        super().delete_model(request, obj)
        clear_reported_flag_without_reports([comment_id])

    def delete_queryset(self, request, queryset):
        comment_ids = list(queryset.values_list('comment_id', flat=True).distinct())
        counts_by_comment = {}
        for row in queryset.values('comment_id').annotate(report_count=Count('pk')):
            counts_by_comment[row['comment_id']] = row['report_count']
        for comment in EpisodeComment.objects.filter(pk__in=counts_by_comment):
            record_moderation_event(
                comment,
                CommentModerationEvent.Action.REPORTS_DELETED,
                actor=request.user,
                details={
                    'report_count': counts_by_comment[comment.pk],
                    'source': 'comment_reports_admin',
                },
            )
        super().delete_queryset(request, queryset)
        clear_reported_flag_without_reports(comment_ids)

    @admin.action(
        description='Dismiss selected reports (keep comments)',
        permissions=['delete'],
    )
    def dismiss_selected_reports(self, request, queryset):
        comment_ids = list(queryset.values_list('comment_id', flat=True).distinct())
        for comment in EpisodeComment.objects.filter(pk__in=comment_ids):
            count = queryset.filter(comment=comment).count()
            record_moderation_event(
                comment,
                CommentModerationEvent.Action.REPORTS_DISMISSED,
                actor=request.user,
                details={'report_count': count},
            )
        dismissed, _ = queryset.delete()
        clear_reported_flag_without_reports(comment_ids)
        self.message_user(
            request,
            f'{dismissed} report(s) dismissed; comments were kept.',
        )

    @admin.action(
        description='Delete reported comment(s) and replies',
        permissions=['delete'],
    )
    def delete_reported_comments(self, request, queryset):
        comment_ids = queryset.values_list('comment_id', flat=True).distinct()
        comments = EpisodeComment.objects.filter(pk__in=comment_ids)
        deleted_comments = comments.count()
        for comment in comments:
            record_moderation_event(
                comment,
                CommentModerationEvent.Action.COMMENT_DELETED,
                actor=request.user,
                details={'source': 'reported_comments_admin'},
            )
        comments.delete()
        self.message_user(
            request,
            f'{deleted_comments} reported comment(s) and their replies deleted.',
        )


@admin.register(CommentModerationEvent)
class CommentModerationEventAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'action',
        'comment_id_snapshot',
        'comment_snapshot',
        'actor_snapshot',
    )
    list_filter = ('action', 'created_at')
    search_fields = ('comment_snapshot', 'actor_snapshot')
    readonly_fields = (
        'action',
        'comment',
        'comment_id_snapshot',
        'comment_snapshot',
        'actor',
        'actor_snapshot',
        'details',
        'created_at',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def natural_sort_key(filename):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', filename)]

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(d, initial) for d in data]
        return super().clean(data, initial)

class comicPageInline(admin.TabularInline):
    model = comicPage
    extra = 0
    fields = ('page_num', 'image')
    ordering = ('page_num',)

class WebcomicAdminForm(forms.ModelForm):
    bulk_images = MultipleFileField(
        required=False,
        help_text="add yo shit here twin"
    )

    class Meta:
        model = webcomic
        fields = '__all__'

@admin.register(webcomic)
class webcomicAdmin(admin.ModelAdmin):
    form = WebcomicAdminForm
    list_display = ('language', 'ep_number', 'title')
    list_filter = ('language',)
    search_fields = ('title', 'subtitle')
    inlines = [comicPageInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        files = form.cleaned_data.get('bulk_images')
        if files:
            files_sorted = sorted(files, key=lambda f: natural_sort_key(f.name))
            start_num = obj.pages.count() + 1
            for i, f in enumerate(files_sorted, start=start_num):
                comicPage.objects.create(webcomic=obj, image=f, page_num=i)