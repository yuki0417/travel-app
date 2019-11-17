import os
from decouple import config
from .settings_base import *


SECRET_KEY = config('STG_SECRET_KEY')

DEBUG = False

# TODO: 検証環境用に適切にホストを設定する
ALLOWED_HOSTS = [config('STG_ALLOWED_HOSTS')]

ROOT_URLCONF = 'setting.urls'

SESSION_ENGINE = 'redis_sessions.session'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=django'
            },
        'NAME': config('STG_DB_NAME'),
        'USER': config('STG_DB_USER'),
        'PASSWORD': config('STG_DB_PASSWORD'),
        'HOST': 'postgres',
        'PORT': config('STG_DB_PORT'),
    }
}

SESSION_REDIS = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
    'password': config('STG_REDIS_PASSWORD'),
    'prefix': 'session',
    'socket_timeout': 3,
    'retry_on_timeout': False
}
