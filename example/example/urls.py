from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from example.views import ExampleAPIDocumentationView, PageNotFoundView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^api-docs/', ExampleAPIDocumentationView.as_view(), name='api-docs'),
    url(r'^api/(?P<version>(\d{4}-\d{2}-\d{2}))/', include('example.urls_api')),

    # API-specific 404 for everything under api/ prefix
    # This one is for when the version is valid
    url(r'^api/(?P<version>(\d{4}-\d{2}-\d{2}))/', PageNotFoundView.as_view()),
    # This one is catch-all for everything else, including invalid versions
    url(r'^api/', PageNotFoundView.as_view()),

    url(r'^admin/', admin.site.urls),
]
