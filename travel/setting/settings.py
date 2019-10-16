import os
from decouple import config
from .settings_base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = False

# TODO: 本番環境用に適切にホストを設定する
ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

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
