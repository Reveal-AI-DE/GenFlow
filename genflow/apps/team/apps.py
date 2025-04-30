# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.apps import AppConfig


class TeamConfig(AppConfig):
    name = "genflow.apps.team"

    def ready(self):
        from django.conf import settings

        from genflow.apps.restriction.registry import register_limit

        # Register limits for the team app
        register_limit(
            "team", "TEAM", "Max teams", default=settings.GF_LIMITS.get("TEAM", None)
        )
        register_limit(
            "team",
            "MAX_INVITATION_PER_TEAM",
            "Max invitations per team",
            default=settings.GF_LIMITS.get("MAX_INVITATION_PER_TEAM", None),
        )

        from genflow.apps.team.signals import register_signals

        register_signals(self)
