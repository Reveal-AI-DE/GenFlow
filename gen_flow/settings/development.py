# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

# pylint: disable=wildcard-import
from gen_flow.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += [
    "django_extensions",
]

# Cross-Origin Resource Sharing settings for GenFlow UI
UI_SCHEME = os.environ.get("UI_SCHEME", "http")
UI_HOST = os.environ.get("UI_HOST", "localhost")
UI_PORT = os.environ.get("UI_PORT", 3000)
CORS_ALLOW_CREDENTIALS = True
UI_URL = "{}://{}".format(UI_SCHEME, UI_HOST)

if UI_PORT and UI_PORT != "80":
    UI_URL += ":{}".format(UI_PORT)

CSRF_TRUSTED_ORIGINS = [UI_URL]

CORS_ORIGIN_WHITELIST = [UI_URL]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": osp.join(BASE_DIR, "db.sqlite3"),
    }
}
