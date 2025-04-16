# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class TeamConfig(AppConfig):
    name = "gen_flow.apps.team"

    def ready(self):
        from gen_flow.apps.team.signals import register_signals

        register_signals(self)
