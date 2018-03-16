from typing import Set

from django.conf import settings
from django.utils.encoding import force_bytes
from django.urls import reverse

from rest_framework.renderers import JSONRenderer as RestJSONRenderer
from rest_framework.response import Response
from rest_framework.test import (APIClient, APILiveServerTestCase, APIRequestFactory, APISimpleTestCase, APITestCase,
                                 APITransactionTestCase)
from rest_framework_json_api.renderers import JSONRenderer as JSONAPIRenderer

from tg_apicore.schemas import replace_variables


class JsonAPIMixin(object):
    """Provide custom rest_framework.test.APIRequestFactory._encode_data

    Customization:
        If selected renderer is JSONAPIRenderer use rest_framework.renderers.JSONRenderer
        to encode input data (and assume it's been correctly structured by the tests)
    """

    def _encode_data(self, data, format=None, content_type=None):  # pylint: disable=redefined-builtin
        """
        Encode the data returning a two tuple of (bytes, content_type)
        """

        if data is None:
            return ('', content_type)

        assert format is None or content_type is None, (
            'You may not set both `format` and `content_type`.'
        )

        if content_type:
            # Content type specified explicitly, treat data as a raw bytestring
            ret = force_bytes(data, settings.DEFAULT_CHARSET)

        else:
            format = format or self.default_format

            assert format in self.renderer_classes, (
                "Invalid format '{0}'. Available formats are {1}. "
                "Set TEST_REQUEST_RENDERER_CLASSES to enable "
                "extra request formats.".format(
                    format,
                    ', '.join(["'" + fmt + "'" for fmt in self.renderer_classes.keys()])
                )
            )

            # Use format and render the data into a bytestring
            renderer = self.renderer_classes[format]()

            # Customization: assume tests provide input data in correct format
            #  and just use the standard JSONRenderer to serialize it
            if isinstance(renderer, JSONAPIRenderer):
                ret = RestJSONRenderer().render(data)

            else:
                ret = renderer.render(data)

            # Determine the content-type header from the renderer
            content_type = "{0}; charset={1}".format(
                renderer.media_type, renderer.charset
            )

            # Coerce text to bytes if required.
            if isinstance(ret, str):
                ret = bytes(ret.encode(renderer.charset))

        return ret, content_type


class JsonAPIRequestFactory(JsonAPIMixin, APIRequestFactory):
    pass


class JsonAPIClient(JsonAPIMixin, APIClient):
    pass


class JsonAPITransactionTestCase(APITransactionTestCase):
    client_class = JsonAPIClient


class JsonAPITestCase(APITestCase):
    client_class = JsonAPIClient


class JsonAPISimpleTestCase(APISimpleTestCase):
    client_class = JsonAPIClient


class JsonAPILiveServerTestCase(APILiveServerTestCase):
    client_class = JsonAPIClient


class APIClient(JsonAPIClient):
    """ Slightly customized DRF APIClient

    - Can force authentication using OAuth2 token.
    - Uses json as default format (no need for settings overrides).
    - Is somewhat api-version-aware (defaulting to settings.API_VERSION_LATEST).
    - Provides version-aware reverse() url helper.
    """

    default_format = 'json'

    def __init__(self, token=None, api_version=None, enforce_csrf_checks=False, **defaults):
        super().__init__(enforce_csrf_checks, **defaults)

        if token is not None:
            # force_authenticate() doesn't work with OAuth2
            self.credentials(HTTP_AUTHORIZATION='Bearer ' + token.token)

        self.api_version = api_version or settings.API_VERSION_LATEST

    def reverse(self, viewname, **kwargs):
        reverse_kwargs = {'version': self.api_version}
        reverse_kwargs.update(kwargs)
        return reverse(viewname, kwargs=reverse_kwargs)

    def replace_variables(self, data):
        site_url = 'http://testserver'
        docs_version = self.api_version
        base_path = '/api/%s/' % docs_version

        return replace_variables(data, site_url, base_path)


def validate_keys(obj: dict, required_keys: Set[str], optional_keys: Set[str] = None) -> None:
    """ Asserts that obj contains all keys in the required set and nothing that isn't in required + optional.
    """

    obj_keys = set(obj.keys())
    if optional_keys is None:
        assert obj_keys == required_keys
    else:
        assert required_keys.issubset(obj_keys), "Required keys missing: %s" % (required_keys - obj_keys)
        allowed_keys = required_keys | optional_keys
        assert obj_keys.issubset(allowed_keys), "Extra keys present: %s" % (obj_keys - allowed_keys)


def validate_response_status_code(resp: Response, expected_status_code: int = 200):
    """ Asserts that response has the given status code.
    """

    assert resp.status_code == expected_status_code, \
        "Unexpected status %d (expected %d): %s" % (resp.status_code, expected_status_code,
                                                    getattr(resp, 'data', resp.content))


def validate_jsonapi_error_response(resp: Response, expected_status_code: int):
    validate_response_status_code(resp, expected_status_code)
    data = resp.json()

    validate_keys(data, {'errors'})


def validate_jsonapi_list_response(
    resp: Response, *, expected_count: int = None,
    expected_attributes: Set[str] = None, expected_relationships: Set[str] = None
) -> dict:
    """ Asserts that the given response is valid JSON API list response.
    """

    validate_response_status_code(resp, 200)
    data = resp.json()

    validate_keys(data, {'data', 'links'}, {'included'})
    items = data['data']
    assert isinstance(items, list)

    if expected_count is not None:
        assert len(items) == expected_count

    if expected_attributes is not None:
        for item in items:
            assert set(item['attributes'].keys()) == expected_attributes
    if expected_relationships is not None:
        for item in items:
            if expected_relationships:
                assert set(item['relationships'].keys()) == expected_relationships
            else:
                assert 'relationships' not in item

    return data


def validate_jsonapi_detail_response(
    resp: Response, *, expected_status_code: int = 200,
    expected_attributes: Set[str] = None, expected_relationships: Set[str] = None
) -> dict:
    """ Asserts that the given response is valid JSON API detail response.
    """

    validate_response_status_code(resp, expected_status_code)
    data = resp.json()

    # Response must contain 'data' and may contain 'included'
    validate_keys(data, {'data'}, {'included'})

    object_data = data['data']
    assert isinstance(object_data, dict)
    validate_keys(object_data, {'type', 'id', 'attributes', 'links'}, {'relationships'})
    if 'included' in data:
        assert isinstance(data['included'], list)

    if expected_attributes is not None:
        assert set(object_data['attributes'].keys()) == expected_attributes
    if expected_relationships is not None:
        if expected_relationships:
            assert set(object_data['relationships'].keys()) == expected_relationships
        else:
            assert 'relationships' not in object_data

    return data
