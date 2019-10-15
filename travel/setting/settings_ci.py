from django.core.management.utils import get_random_secret_key
from .settings import *


SECRET_KEY = get_random_secret_key()

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django_ci'
            },
        'NAME': 'djangodb_ci',
        'USER': 'travel_ci',
        'PASSWORD': 'travel_ci',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
