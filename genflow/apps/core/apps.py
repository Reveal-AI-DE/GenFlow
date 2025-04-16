# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "genflow.apps.core"

    def ready(self):
        pass
