from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from tg_apicore.views import PageNotFoundView

from example.views import ExampleAPIDocumentationView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^api-docs/', ExampleAPIDocumentationView.as_view(), name='api-docs'),
    url(r'^api/(?P<version>(\d{4}-\d{2}-\d{2}))/', include('example.urls_api')),

    # API-specific 404 for everything under api/ prefix
    url(r'^api/', include(PageNotFoundView.urlpatterns())),

    url(r'^admin/', admin.site.urls),
]
