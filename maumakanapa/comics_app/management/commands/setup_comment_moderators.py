from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or refresh the least-privilege Comment moderators group.'

    permission_codenames = (
        'view_episodecomment',
        'change_episodecomment',
        'delete_episodecomment',
        'view_commentreport',
        'delete_commentreport',
        'view_commentmoderationevent',
    )

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='Comment moderators')
        permissions = list(
            Permission.objects.filter(
                content_type__app_label='comics_app',
                codename__in=self.permission_codenames,
            )
        )
        found = {permission.codename for permission in permissions}
        missing = set(self.permission_codenames) - found
        if missing:
            raise CommandError(
                'Missing permissions; run migrations first: '
                + ', '.join(sorted(missing))
            )
        group.permissions.set(permissions)
        self.stdout.write(
            self.style.SUCCESS(
                'Comment moderators group is ready. Assign users to it in Django admin '
                'and ensure their staff status is enabled.'
            )
        )
