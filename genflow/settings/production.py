# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

# pylint: disable=wildcard-import
from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("GF_POSTGRES_HOST", "db"),
        "NAME": os.getenv("GF_POSTGRES_DBNAME", "genflow"),
        "USER": os.getenv("GF_POSTGRES_USER", "root"),
        "PASSWORD": os.getenv("GF_POSTGRES_PASSWORD", ""),
        "PORT": os.getenv("GF_POSTGRES_PORT", 5432),
    }
}

if "GF_EMAIL_HOST_PASSWORD" in os.environ and os.getenv("GF_EMAIL_HOST_PASSWORD").strip():
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("GF_EMAIL_HOST", "smtp.ionos.de")
    EMAIL_PORT = int(os.getenv("GF_EMAIL_PORT", 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("GF_EMAIL_HOST_USER", "noreply@revealai.de")
    EMAIL_HOST_PASSWORD = os.getenv("GF_EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = os.getenv("GF_DEFAULT_FROM_EMAIL", "noreply@revealai.de")
else:
    # https://github.com/pennersr/django-allauth
    ACCOUNT_EMAIL_VERIFICATION = "none"

LOGGING["formatters"]["verbose_uvicorn_access"] = {
    "()": "uvicorn.logging.AccessFormatter",
    "format": '[{asctime}] {levelprefix} {client_addr} - "{request_line}" {status_code}',
    "style": "{",
}
LOGGING["handlers"]["verbose_uvicorn_access"] = {
    "formatter": "verbose_uvicorn_access",
    "class": "logging.StreamHandler",
    "stream": "ext://sys.stdout",
}
LOGGING["loggers"]["uvicorn.access"] = {
    "handlers": ["verbose_uvicorn_access"],
    "level": "INFO",
    "propagate": False,
}
