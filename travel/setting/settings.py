import os
from decouple import config
from .settings_base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = False

# TODO: 本番環境用に適切にホストを設定する
ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

ROOT_URLCONF = 'setting.urls'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django'
            },
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# TODO: 本番環境のElastiCache設定を行う
# SESSION_REDIS = {
#     'host': 'ElastiCacheのURL?',
#     'port': 6379,
#     'db': 0,
#     'password': config('REDIS_PASSWORD'),
#     'prefix': 'session',
#     'socket_timeout': 3,
#     'retry_on_timeout': False
# }
