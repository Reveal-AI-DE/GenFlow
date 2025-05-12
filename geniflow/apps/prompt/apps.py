# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.apps import AppConfig


class PromptConfig(AppConfig):
    name = "geniflow.apps.prompt"

    def ready(self):
        from django.conf import settings

        from geniflow.apps.restriction.registry import register_limit

        # Register limits for the prompt app
        register_limit(
            "prompt",
            "PROMPT_GROUP",
            "Max prompt groups",
            default=settings.GF_LIMITS.get("PROMPT_GROUP", None),
        )
        register_limit(
            "prompt", "PROMPT", "Max prompts", default=settings.GF_LIMITS.get("PROMPT", None)
        )

        # pylint: disable=unused-import
        from geniflow.apps.prompt import signals
