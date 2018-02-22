from rest_framework import routers


class APIRootView(routers.APIRootView):
    required_scopes = []


class Router(routers.DefaultRouter):
    """ Slightly more JSON-API compatible router that disables PUT method.

    JSON-API always uses PATCH for updating objects, so PUT is superfluous.
    """

    APIRootView = APIRootView

    def get_method_map(self, viewset, method_map):
        method_map = super().get_method_map(viewset, method_map)
        if 'put' in method_map:
            del method_map['put']

        return method_map
