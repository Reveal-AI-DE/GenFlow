# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.apps import AppConfig


class IAMConfig(AppConfig):
    name = "genflow.apps.iam"

    def ready(self):
        from .signals import register_signals

        register_signals()
