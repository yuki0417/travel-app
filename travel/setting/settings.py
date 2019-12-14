import os
from decouple import config
from .settings_base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = False

# TODO: 本番環境用に適切にホストを設定する
ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

ROOT_URLCONF = 'setting.urls'

# 静的ファイルの設定
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# TODO: 本番環境のRDS設定を行う
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=django,public',
            },
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# TODO: 本番環境のElastiCache設定を行う
SESSION_REDIS = {
    'host': config('REDIS_HOST'),
    'port': 6379,
    'db': 0,
    'password': config('REDIS_PASSWORD'),
    'prefix': 'session',
    'socket_timeout': 3,
    'retry_on_timeout': False
}
