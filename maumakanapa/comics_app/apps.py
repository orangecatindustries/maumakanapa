from django.apps import AppConfig


class ComicsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comics_app'

    def ready(self):
        from . import signals
