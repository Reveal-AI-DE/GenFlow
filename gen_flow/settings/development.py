# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp
from gen_flow.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += [
    "django_extensions",
]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': osp.join(BASE_DIR, 'db.sqlite3'),
    }
}
