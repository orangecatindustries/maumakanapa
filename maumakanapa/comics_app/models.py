import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings


def comment_image_upload_to(instance, filename):
    extension = filename.rsplit('.', 1)[-1].lower()
    return f'comments/{uuid.uuid4().hex}.{extension}'


class webcomic(models.Model):
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('indonesian', 'Indonesian'),
        ('spanish', 'Spanish'),
        ('portuguese', 'Portuguese'),
        ('russian', 'Russian'),
        ('chinese', 'Chinese'),
        ('italiano', 'Italiano'),
        ('filipino', 'Filipino'),
        ('ukrainian', 'Ukrainian')
    ]

    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    ep_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('page', kwargs={
            'lang': self.language,
            'number': self.ep_number
        })
    
    class Meta:
        ordering = ['language', 'ep_number']
        unique_together = ('language', 'ep_number')

    def __str__(self):
        return f'[{self.language.upper()}] Ep {self.ep_number}: {self.title}'


class EpisodeComment(models.Model):
    webcomic = models.ForeignKey(webcomic, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='episode_comments',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    parent = models.ForeignKey(
        'self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE
    )
    display_name = models.CharField(max_length=32, blank=True, default='Anonymous')
    body = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(upload_to=comment_image_upload_to, blank=True)
    owner_key = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_reported = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    moderation_reason = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['created_at', 'pk']

    def __str__(self):
        return f'{self.display_name} on {self.webcomic}'


class CommentLike(models.Model):
    comment = models.ForeignKey(EpisodeComment, related_name='likes', on_delete=models.CASCADE)
    owner_key = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'owner_key'], name='unique_comment_like')
        ]


class CommentReport(models.Model):
    comment = models.ForeignKey(EpisodeComment, related_name='reports', on_delete=models.CASCADE)
    reporter_key = models.CharField(max_length=64)
    reason = models.TextField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'reporter_key'], name='unique_comment_report')
        ]


class CommentModerationEvent(models.Model):
    class Action(models.TextChoices):
        APPROVED = 'approved', 'Comment approved'
        UNAPPROVED = 'unapproved', 'Comment hidden'
        REPORTS_DISMISSED = 'reports_dismissed', 'Reports dismissed'
        REPORTS_DELETED = 'reports_deleted', 'Reports deleted'
        COMMENT_DELETED = 'comment_deleted', 'Comment deleted'
        REPORTS_PRUNED = 'reports_pruned', 'Expired reports removed'

    action = models.CharField(max_length=32, choices=Action.choices)
    comment = models.ForeignKey(
        EpisodeComment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='moderation_events',
    )
    comment_id_snapshot = models.PositiveBigIntegerField()
    comment_snapshot = models.CharField(max_length=300)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comment_moderation_events',
    )
    actor_snapshot = models.CharField(max_length=150)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return f'{self.get_action_display()} for comment {self.comment_id_snapshot}'


class comicPage(models.Model):
    webcomic = models.ForeignKey(webcomic, related_name='pages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comics/pages/')
    page_num = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['webcomic', 'page_num']
        unique_together = ('webcomic', 'page_num')

    def __str__(self):
        return f"{self.webcomic.title} - Page {self.page_num}"