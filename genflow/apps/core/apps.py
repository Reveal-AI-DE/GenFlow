# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "genflow.apps.core"

    def ready(self):
        pass
