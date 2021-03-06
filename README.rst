=================
Thorgate API Core
=================


.. image:: https://img.shields.io/pypi/v/tg-apicore.svg
        :target: https://pypi.python.org/pypi/tg-apicore

.. image:: https://img.shields.io/travis/thorgate/tg-apicore.svg
        :target: https://travis-ci.org/thorgate/tg-apicore

.. image:: https://readthedocs.org/projects/tg-apicore/badge/?version=latest
        :target: https://tg-apicore.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Opinionated API framework on top of Django REST framework


* Free software: ISC license

Supports Python 3.5+, Django 1.11+, Django REST framework 3.6+


Features
--------

* API documentation automatically generated from your views
    * General intro can be added
    * You can add example request/response data
    * Autogenerated Python `requests`-based examples
    * Not interactive yet
* Integrates `JSON API <http://jsonapi.org/>`_
    * Cursor pagination with configurable page size
* Viewset classes for using different serializers and querysets for list/detail/edit endpoints
* API-specific 404 view
* Test utilities, e.g. for response validation
* Versioning (WIP)
    * Transformer-based approach, inspired by
      `djangorestframework-version-transforms <https://github.com/mrhwick/django-rest-framework-version-transforms>`_
      and `Stripe <https://stripe.com/blog/api-versioning>`_


Usage
-----

- ``pip install tg-apicore``
- Add ``tg_apicore`` to ``INSTALLED_APPS``
- Ensure your ``REST_FRAMEWORK`` setting contains ``ALLOWED_VERSIONS``, e.g:

  .. code:: python

      # In your Django project settings:
      REST_FRAMEWORK = {
          'ALLOWED_VERSIONS': ('2018-01-01',),
      }

- Note that the default paginator requires that your models have ``created`` field

- Create API documentation view by subclassing ``APIDocumentationView`` and making necessary modifications.
  See ``example/example/views.py`` for example.
- Add main API urls plus 404 view (as fallback).


Here's an example ``urls.py``:

.. code:: python

    from tg_apicore.views import PageNotFoundView

    from myproject.views import MyProjectAPIDocumentationView

    urlpatterns = [
        # The documentation view
        url(r'^api-docs/', MyProjectAPIDocumentationView.as_view(), name='api-docs'),

        # myproject.urls_api should contain your API urls patterns
        url(r'^api/(?P<version>(\d{4}-\d{2}-\d{2}))/', include('myproject.urls_api')),

        # API-specific 404 for everything under api/ prefix
        url(r'^api/', include(PageNotFoundView.urlpatterns())),
    ]

See ``example`` directory for a more in-depth demo.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
