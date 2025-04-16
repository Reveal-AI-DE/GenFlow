# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class PromptConfig(AppConfig):
    name = "gen_flow.apps.prompt"

    def ready(self):
        pass
