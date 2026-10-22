from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import EpisodeComment


@receiver(post_delete, sender=EpisodeComment)
def delete_comment_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
