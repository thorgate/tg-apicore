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
    'ALLOWED_VERSIONS': ('2018-02-21',),
}
