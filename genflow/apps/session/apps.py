# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class SessionConfig(AppConfig):
    name = "genflow.apps.session"

    def ready(self):
        from django.conf import settings
        from genflow.apps.restriction.registry import register_limit

        # Register limits for the session app
        register_limit("session", "SESSION", "Max sessions", default=settings.GF_LIMITS.get("SESSION", None))
        register_limit("session", "MESSAGE", "Max messages per session", default=settings.GF_LIMITS.get("MESSAGE", None))
        register_limit("session", "MAX_FILES_PER_SESSION", "Max files upload per session", default=settings.GF_LIMITS.get("MAX_FILES_PER_SESSION", None))

        from genflow.apps.session import signals
