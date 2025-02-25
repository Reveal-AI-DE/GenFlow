# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("GEN_FLOW_POSTGRES_HOST", "db"),
        "NAME": os.getenv("GEN_FLOW_POSTGRES_DBNAME", "gen_flow"),
        "USER": os.getenv("GEN_FLOW_POSTGRES_USER", "root"),
        "PASSWORD": os.getenv("GEN_FLOW_POSTGRES_PASSWORD", ""),
        "PORT": os.getenv("GEN_FLOW_POSTGRES_PORT", 5432),
    }
}
