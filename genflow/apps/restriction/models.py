# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.contrib.auth import get_user_model
from django.db import models

from genflow.apps.common.models import TimeAuditModel
from genflow.apps.team.models import Team


class Limit(TimeAuditModel):
    """
    Model to define limits for users, teams, or globally.
    """

    key = models.CharField(max_length=255, unique=False)
    value = models.IntegerField()
    user = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name="limits"
    )
    team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE, related_name="limits"
    )

    class Meta:
        # Unique constraint on team and user.
        constraints = [
            models.UniqueConstraint(fields=["key", "user", "team"], name="unique_limit_user_team"),
        ]
        verbose_name = "Limit"
        verbose_name_plural = "Limits"

    def __str__(self):
        target = self.user or self.team or "Global"
        return f"{self.key} ({target}): {self.value}"
