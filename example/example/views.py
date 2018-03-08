from django.conf import settings
from django.conf.urls import url
from django.urls import include

from tg_apicore.views import APIDocumentationView


class ExampleAPIDocumentationView(APIDocumentationView):
    title = "Example API"

    def get_description(self):
        from example import api_docs

        return api_docs.__doc__.replace('# NOQA', '')

    def get_site_url(self) -> str:
        return settings.SITE_URL

    def get_base_path(self) -> str:
        docs_version = settings.API_VERSION_LATEST
        return '/api/%s/' % docs_version

    def get_patterns(self) -> list:
        from example import urls_api

        return [
            url(r'^%s' % self.get_base_path(), include(urls_api)),
        ]
