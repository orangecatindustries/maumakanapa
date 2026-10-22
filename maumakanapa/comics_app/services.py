from django.db import transaction
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.crypto import salted_hmac

from .models import (
    CommentLike,
    CommentModerationEvent,
    CommentReport,
    EpisodeComment,
)


@transaction.atomic
def attach_anonymous_comments_to_user(owner_key, user):
    """Claim comments from a verified browser identity after a future login."""
    if not owner_key:
        raise ValueError('An anonymous ownership key is required.')
    if not user or not user.is_authenticated:
        raise ValueError('An authenticated user is required to claim comments.')
    return EpisodeComment.objects.filter(
        owner_key=owner_key,
        author__isnull=True,
    ).update(author=user)


def claim_browser_comments_for_authenticated_user(request):
    """Claim anonymous comments using the logged-in user's signed browser token."""
    if not request.user.is_authenticated:
        raise PermissionDenied('Sign in before claiming anonymous comments.')
    token = request.COOKIES.get(settings.COMMENT_OWNER_COOKIE_NAME, '')
    if len(token) < 32 or len(token) > 128 or not token.isascii():
        raise ValueError('No valid anonymous ownership cookie was provided.')
    owner_key = salted_hmac('episode-comment-owner-cookie', token).hexdigest()
    return attach_anonymous_comments_to_user(owner_key, request.user)


@transaction.atomic
def migrate_legacy_owner_key(legacy_key, persistent_key):
    """Upgrade the old session-derived identity while that session still exists."""
    if not legacy_key or not persistent_key or legacy_key == persistent_key:
        return 0
    comments_updated = EpisodeComment.objects.filter(
        owner_key=legacy_key,
        author__isnull=True,
    ).update(owner_key=persistent_key)
    _migrate_unique_owner_records(
        CommentLike,
        'owner_key',
        legacy_key,
        persistent_key,
    )
    _migrate_unique_owner_records(
        CommentReport,
        'reporter_key',
        legacy_key,
        persistent_key,
    )
    return comments_updated


def _migrate_unique_owner_records(model, identity_field, legacy_key, persistent_key):
    for record in model.objects.filter(**{identity_field: legacy_key}).only(
        'pk', 'comment_id'
    ).iterator():
        duplicate_exists = model.objects.filter(
            comment_id=record.comment_id,
            **{identity_field: persistent_key},
        ).exists()
        if duplicate_exists:
            record.delete()
        else:
            model.objects.filter(pk=record.pk).update(
                **{identity_field: persistent_key}
            )


def record_moderation_event(comment, action, actor=None, details=None):
    return CommentModerationEvent.objects.create(
        action=action,
        comment=comment,
        comment_id_snapshot=comment.pk,
        comment_snapshot=f'Comment {comment.pk} by {comment.display_name}'[:300],
        actor=actor if actor and actor.is_authenticated else None,
        actor_snapshot=(
            actor.get_username()
            if actor and actor.is_authenticated
            else 'System'
        ),
        details=details or {},
    )
