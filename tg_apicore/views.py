from django.conf.urls import url
from django.views.generic.base import TemplateView

from rest_framework.compat import pygments_css
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from tg_apicore.schemas import generate_api_docs


class APIDocumentationView(TemplateView):
    """ API documentation view

    Subclass it, set title and description attributes and implement the three get_*() methods.
    """

    template_name = 'tg_apicore/docs/index.html'
    # Pygments code style to use. Go to http://pygments.org/demo/ , select an example an
    #  you'll have a dropdown of style options on the right.
    code_style = 'emacs'

    title = "API"
    description = ""

    def generate_docs(self):
        return generate_api_docs(
            title=self.title, description=self.get_description(),
            site_url=self.get_site_url(), base_path=self.get_base_path(), patterns=self.urlpatterns(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        docs = self.generate_docs()
        context.update({
            'api': docs,
            'code_style': pygments_css(self.code_style),
        })

        return context

    def get_description(self) -> str:
        return self.description

    def get_site_url(self) -> str:
        """ Should return your site's url without path, e.g. https://example.com/ """
        raise NotImplementedError()

    def get_base_path(self) -> str:
        """ Should return your API's base path (path prefix), e.g. /api/v1/ """
        raise NotImplementedError()

    def urlpatterns(self) -> list:
        """ Should return urlpatterns of your API """
        raise NotImplementedError()


class PageNotFoundView(APIView):
    """ 404 view for API urls.

    Django's standard 404 page returns HTML. We want everything under API url prefix to return 404 as JSON.
    """

    authentication_classes = ()
    permission_classes = ()

    @classmethod
    def urlpatterns(cls):
        return [
            # This one is for when the version is valid
            url(r'^(?P<version>(\d{4}-\d{2}-\d{2}))/', cls.as_view()),
            # This one is catch-all for everything else, including invalid versions
            url(r'^', cls.as_view()),
        ]

    def initial(self, request, *args, **kwargs):
        # Overriding initial() seems to be like  the easiest way that still keeps most of DRF's logic ala renderers.
        super().initial(request, *args, **kwargs)

        raise NotFound()
