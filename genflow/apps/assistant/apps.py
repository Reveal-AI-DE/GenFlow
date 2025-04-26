# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class AssistantConfig(AppConfig):
    name = "genflow.apps.assistant"

    def ready(self):
        from django.conf import settings
        from genflow.apps.restriction.registry import register_limit

        # Register limits for the assistant app
        register_limit("assistant", "ASSISTANT_GROUP", "Max assistant groups", default=settings.GF_LIMITS.get("ASSISTANT_GROUP", None))
        register_limit("assistant", "ASSISTANT", "Max assistants", default=settings.GF_LIMITS.get("ASSISTANT", None))
        register_limit("assistant", "MAX_FILES_PER_ASSISTANT", "Max files upload per assistant", default=settings.GF_LIMITS.get("MAX_FILES_PER_ASSISTANT", None))

        from genflow.apps.assistant import signals

