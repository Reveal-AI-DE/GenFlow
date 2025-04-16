# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

# pylint: disable=wildcard-import
from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("GF_POSTGRES_HOST", "db"),
        "NAME": os.getenv("GF_POSTGRES_DBNAME", "gen_flow"),
        "USER": os.getenv("GF_POSTGRES_USER", "root"),
        "PASSWORD": os.getenv("GF_POSTGRES_PASSWORD", ""),
        "PORT": os.getenv("GF_POSTGRES_PORT", 5432),
    }
}
