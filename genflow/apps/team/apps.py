# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.apps import AppConfig


class TeamConfig(AppConfig):
    name = "genflow.apps.team"

    def ready(self):
        from genflow.apps.team.signals import register_signals

        register_signals(self)
