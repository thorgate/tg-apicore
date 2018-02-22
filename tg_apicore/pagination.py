from rest_framework.pagination import CursorPagination as DRFCursorPagination
from rest_framework.pagination import _positive_int
from rest_framework.response import Response


class CursorPagination(DRFCursorPagination):
    """ A json-api compatible cursor pagination format

    Also supports customizable page_size via GET parameter.
    """

    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'links': {
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
            }
        })
