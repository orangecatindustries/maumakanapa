import json
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Create a consistent SQLite database and media ZIP backup.'

    def add_arguments(self, parser):
        parser.add_argument('output', help='Destination ZIP path; must not already exist.')

    def handle(self, *args, **options):
        if connection.vendor != 'sqlite':
            raise CommandError('This backup command currently supports SQLite only.')

        output = Path(options['output']).expanduser().resolve()
        media_root = Path(settings.MEDIA_ROOT).resolve()
        if output.exists():
            raise CommandError(f'Backup already exists: {output}')
        if output == media_root or media_root in output.parents:
            raise CommandError('Store the backup outside MEDIA_ROOT.')
        output.parent.mkdir(parents=True, exist_ok=True)

        connection.ensure_connection()
        with tempfile.TemporaryDirectory(dir=output.parent) as temporary_directory:
            temp_dir = Path(temporary_directory)
            database_snapshot = temp_dir / 'database.sqlite3'
            archive_temp = temp_dir / 'backup.zip'
            target_connection = connection.Database.connect(str(database_snapshot))
            try:
                connection.connection.backup(target_connection)
            finally:
                target_connection.close()

            with zipfile.ZipFile(
                archive_temp, mode='w', compression=zipfile.ZIP_DEFLATED
            ) as archive:
                archive.write(database_snapshot, 'database.sqlite3')
                if media_root.exists():
                    for path in media_root.rglob('*'):
                        if path.is_file():
                            archive.write(
                                path,
                                Path('media') / path.relative_to(media_root),
                            )
                archive.writestr(
                    'manifest.json',
                    json.dumps(
                        {
                            'created_at': datetime.now(timezone.utc).isoformat(),
                            'database': 'SQLite online backup snapshot',
                            'media_root': str(media_root),
                        },
                        indent=2,
                    ),
                )
            archive_temp.replace(output)

        self.stdout.write(self.style.SUCCESS(f'Backup created: {output}'))
