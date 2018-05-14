from django.db.models import QuerySet

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS


class DetailSerializerViewSet(GenericAPIView):
    """ Use different serializers and querysets for list / detail / modify views.

    This is basically extended variant of DetailSerializerMixin from drf-extensions.

    It provides additional queryset/serializer options for unsafe methods (`*_modify`) and makes it easy to override
    methods that return serializer classes / querysets so that you can add your own logic with minimal effort.

    The detail / modify variants of queryset / serializer are optional and fall back to each other in
    modify -> detail -> list order.
    """

    ENDPOINT_TYPE_LIST = 1
    ENDPOINT_TYPE_DETAIL = 2
    ENDPOINT_TYPE_MODIFY = 3

    serializer_detail_class = None
    serializer_modify_class = None
    queryset_detail = None
    queryset_modify = None

    def get_endpoint_type(self):
        """ Selects endpoint type of the current request - this will be used to select serializer and queryset.
        """

        if self.request and self.request.method not in SAFE_METHODS:
            return self.ENDPOINT_TYPE_MODIFY

        if hasattr(self, 'lookup_url_kwarg'):
            lookup = self.lookup_url_kwarg or self.lookup_field
            if lookup and lookup in self.kwargs:
                return self.ENDPOINT_TYPE_DETAIL

        return self.ENDPOINT_TYPE_LIST

    def get_serializer_class(self):
        """ Selects serializer class, based on current request's endpoint type.
        """

        endpoint_type = self.get_endpoint_type()

        if endpoint_type == self.ENDPOINT_TYPE_MODIFY:
            return self.get_modify_serializer_class()
        elif endpoint_type == self.ENDPOINT_TYPE_DETAIL:
            return self.get_detail_serializer_class()

        return self.get_list_serializer_class()

    def get_docs_serializer(self):
        """ Returns serializer instance used to generate documentation.

        This defaults to the modify-serializer.
        """

        serializer_cls = self.get_modify_serializer_class()
        return serializer_cls(context=self.get_serializer_context())

    def get_queryset(self):
        """ Selects queryset, based on current request's endpoint type.
        """

        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        endpoint_type = self.get_endpoint_type()

        if endpoint_type == self.ENDPOINT_TYPE_MODIFY:
            queryset = self.get_modify_queryset()
        elif endpoint_type == self.ENDPOINT_TYPE_DETAIL:
            queryset = self.get_detail_queryset()
        else:
            queryset = self.get_list_queryset()

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_list_serializer_class(self):
        return self.serializer_class

    def get_detail_serializer_class(self):
        return self.serializer_detail_class or self.get_list_serializer_class()

    def get_modify_serializer_class(self):
        return self.serializer_modify_class or self.get_detail_serializer_class()

    def get_list_queryset(self):
        return self.queryset

    def get_detail_queryset(self):
        return self.queryset_detail or self.get_list_queryset()

    def get_modify_queryset(self):
        return self.queryset_modify or self.get_detail_queryset()
