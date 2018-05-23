=======
History
=======

0.3.0 (2018-05-23)
------------------

* Add Usage section to README (to make starting up easier)
* Most ``REST_FRAMEWORK`` settings are now automatically configured by Thorgate API Core.
  Users only need to specify ``ALLOWED_VERSIONS``, the rest is optional.


0.2.1 (2018-04-14)
------------------

* Fix packaging (tg_apicore subdirs weren't included)


0.2.0 (2018-04-14)
------------------

* Added PageNotFoundView (JSON-based 404 views)
* Added DetailSerializerViewSet (different serializers and queryset for list/detail/edit views)
* Added CreateOnlyFieldsSerializerMixin, ModelValidationSerializerMixin and BaseModelSerializer
* Renamed APIDocumentationView.get_patterns() to .urlpatterns()
* Improved example app a lot. It now also includes tests that partially test tg-apicore itself


0.1.0 (2018-03-08)
------------------

* First release on PyPI.
