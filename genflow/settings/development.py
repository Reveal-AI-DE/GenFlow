# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from os import path as osp

# pylint: disable=wildcard-import
from genflow.settings.base import *

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

# set UI url to redirect to after e-mail confirmation
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "{}/#/auth/email-confirmed".format(UI_URL)
INCORRECT_EMAIL_CONFIRMATION_URL = "{}/#/auth/email-not-confirmed".format(UI_URL)
ACCOUNT_EMAIL_VERIFICATION_SENT_REDIRECT_URL = "{}/#/auth/verification-sent".format(UI_URL)

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": osp.join(BASE_DIR, "db.sqlite3"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
