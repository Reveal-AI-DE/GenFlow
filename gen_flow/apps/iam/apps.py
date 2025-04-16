# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class IAMConfig(AppConfig):
    name = "gen_flow.apps.iam"

    def ready(self):
        from .signals import register_signals

        register_signals()
