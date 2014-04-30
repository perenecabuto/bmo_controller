# -*- coding: utf-8 -*-

import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'bmo_controller.sqlite3'),
    }
}

SECRET_KEY = 'DUMMY'

ROOT_URLCONF = 'urls'

STATIC_ROOT = 'static/'
STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django_extensions',

    'bmo_controller',
)
