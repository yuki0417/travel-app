import os

from decouple import config
from .settings_base import *


SECRET_KEY = config('DEV_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost']
ALLOWED_HOSTS += [
    '192.168.{}.{}'.format(i, j) for i in range(256) for j in range(256)]


ROOT_URLCONF = 'setting.urls_dev'

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

SESSION_ENGINE = 'redis_sessions.session'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=public'
            },
        'NAME': config('DEV_DB_NAME'),
        'USER': config('DEV_DB_USER'),
        'PASSWORD': config('DEV_DB_PASSWORD'),
        'HOST': "postgres",
        'PORT': config('DEV_DB_PORT'),
    },
    'TEST': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=public'
            },
        'NAME': "test_db",
        'USER': "test_user",
        'PASSWORD': "test_password",
        'HOST': "postgres",
        'PORT': config('DEV_DB_PORT'),
    },
}

SESSION_REDIS = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
    'password': config('DEV_REDIS_PASSWORD'),
    'prefix': 'session',
    'socket_timeout': 3,
    'retry_on_timeout': False
}

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = os.path.join(BASE_DIR, 'test-reports')
TEST_OUTPUT_FILE_NAME = 'test.xml'
