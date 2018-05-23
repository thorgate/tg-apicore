from django.conf import settings

from rest_framework.settings import api_settings


DEFAULTS = {
    'REST_FRAMEWORK': {
        'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',

        'DEFAULT_PAGINATION_CLASS': 'tg_apicore.pagination.CursorPagination',
        'PAGE_SIZE': 50,

        'DEFAULT_PARSER_CLASSES': (
            'tg_apicore.parsers.JSONParser',
            'rest_framework_json_api.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser'
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'tg_apicore.renderers.JSONRenderer',
            'rest_framework_json_api.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',

        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',

        'SCHEMA_COERCE_METHOD_NAMES': {},

        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        'TEST_REQUEST_RENDERER_CLASSES': (
            'tg_apicore.renderers.JSONRenderer',
            'rest_framework.renderers.MultiPartRenderer',
        ),
    },

    'JSON_API_FORMAT_TYPES': 'underscore',
}

INVALID_DRF_CONFIG_MSG = """You must define %(name)s setting in REST_FRAMEWORK settings!
e.g in your settings.py:

REST_FRAMEWORK = {
    # other settings...
    %(example)s,
}
"""

INVALID_DJANGO_CONFIG_MSG = """You must define %(name)s setting in Django settings!
e.g in your settings.py:

# other settings...
%(example)s
"""


def patch_django_settings():
    if not getattr(settings, 'TG_APICORE_PATCH_DRF_SETTINGS', True):
        return

    for k, v in DEFAULTS.items():
        current = getattr(settings, k, None)

        if current is None:
            setattr(settings, k, v)
            continue

        if isinstance(current, dict) and isinstance(v, dict):
            for subk, subv in v.items():
                if subk not in current:
                    current[subk] = subv


def invalid_setting_error(name, example_config, msg_template):
    return msg_template % {
        'name': name,
        'example': example_config,
    }


def invalid_drf_setting_error(name, example_config):
    return invalid_setting_error(name, example_config, INVALID_DRF_CONFIG_MSG)


def invalid_django_setting_error(name, example_config):
    return invalid_setting_error(name, example_config, INVALID_DJANGO_CONFIG_MSG)


def verify_settings():
    assert api_settings.ALLOWED_VERSIONS is not None, \
        invalid_drf_setting_error('ALLOWED_VERSIONS', "'ALLOWED_VERSIONS': ('2018-01-01',)")
    assert len(api_settings.ALLOWED_VERSIONS) >= 1

    assert get_latest_version() in api_settings.ALLOWED_VERSIONS, \
        "Value of API_VERSION_LATEST setting is not among REST_FRAMEWORK's ALLOWED_VERSIONS"

    # If the API_VERSION_LATEST setting isn't defined, do it now to make it easier to access via Django settings.
    if not hasattr(settings, 'API_VERSION_LATEST'):
        settings.API_VERSION_LATEST = get_latest_version()


def get_latest_version() -> str:
    return getattr(settings, 'API_VERSION_LATEST', None) or api_settings.ALLOWED_VERSIONS[-1]
