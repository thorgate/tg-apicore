from django.apps import AppConfig

from tg_apicore import settings


class TgApicoreConfig(AppConfig):
    name = 'tg_apicore'

    def ready(self):
        super().ready()

        settings.patch_django_settings()
        settings.verify_settings()
