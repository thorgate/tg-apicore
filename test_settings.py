DEBUG = True

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

MIDDLEWARE_CLASSES = []

INSTALLED_APPS = [
    'rest_framework',
    'tg_apicore',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


SITE_URL = 'http://127.0.0.1:8000'


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',


    'DEFAULT_PAGINATION_CLASS': 'tg_apicore.pagination.CursorPagination',
    'PAGE_SIZE': 20,

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
    'ALLOWED_VERSIONS': ('2018-02-21',),

    'SCHEMA_COERCE_METHOD_NAMES': {},

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'tg_apicore.renderers.JSONRenderer',
        'rest_framework.renderers.MultiPartRenderer',
    ),
}
API_VERSION_LATEST = REST_FRAMEWORK['ALLOWED_VERSIONS'][-1]

JSON_API_FORMAT_TYPES = 'underscore'
