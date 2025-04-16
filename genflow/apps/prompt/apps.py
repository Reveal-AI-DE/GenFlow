# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class PromptConfig(AppConfig):
    name = "genflow.apps.prompt"

    def ready(self):
        pass
