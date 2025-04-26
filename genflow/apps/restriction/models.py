# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.db import models
from django.contrib.auth import get_user_model
from genflow.apps.team.models import Team

from genflow.apps.common.models import TimeAuditModel

class Limit(TimeAuditModel):
    """
    Model to define limits for users, teams, or globally.
    """

    key = models.CharField(max_length=255, unique=False)
    value = models.IntegerField()
    user = models.ForeignKey(get_user_model(), null=True, blank=True,
            on_delete=models.CASCADE, related_name="limits")
    team = models.ForeignKey(Team, null=True, blank=True,
            on_delete=models.CASCADE, related_name="limits")

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
