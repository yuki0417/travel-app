import os

from .settings_base import *


SECRET_KEY = ')0gwbry_12@or-!^_0+vjqsao9(0ht4uo0bq1j!h0+26k^3(4v'

DEBUG = True

ROOT_URLCONF = 'setting.urls'

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
        'TEST': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'OPTIONS': {
                'options': '-c search_path=django'
                },
            'NAME': 'djangodb_ci',
            'USER': 'travel_ci',
            'PASSWORD': 'travel_ci',
            'HOST': 'postgres',
            'PORT': '5432',
        },
    }
}

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = os.path.join(BASE_DIR, 'test-reports/unittest')
TEST_OUTPUT_FILE_NAME = 'unittest.xml'
