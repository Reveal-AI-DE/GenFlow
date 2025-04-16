# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import timezone

from genflow.apps.common.models import TimeAuditModel, UserOwnedModel


class TeamRole(models.TextChoices):
    """
    Enum class representing different roles within a team.
    """

    OWNER = "owner"
    ADMIN = "admin"
    ENGINEER = "engineer"
    MEMBER = "member"


class Team(TimeAuditModel, UserOwnedModel):
    """
    Team model representing a team entity with attributes for name, description, and encryption public key.

    Attributes:
        name (CharField): The name of the team, with a maximum length of 255 characters. Cannot  be blank.
        description (TextField): A text description of the team. Can be blank.
        encrypt_public_key (TextField): The public key used for encryption. Can be blank.
    """

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True)
    encrypt_public_key = models.TextField(blank=True)

    class Meta:
        default_permissions = ()

    @property
    def is_personal(self) -> bool:
        """
        Returns True if the team name matches the default user team name from settings.
        """

        return self.name == settings.USER_DEFAULT_TEAM_NAME

    def __str__(self):
        """
        Returns the name of the team as its string representation.
        """

        return self.name


class Membership(TimeAuditModel):
    """
    Membership model representing the membership of a user in a team.

    Attributes:
        user (ForeignKey): The user who is a member of the team.
        team (ForeignKey): The team to which the user belongs.
        is_active (BooleanField): Indicates whether the membership is active.
        joined_date (DateTimeField): The date when the user joined the team.
        role (CharField): The role of the user within the team.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="memberships")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    is_active = models.BooleanField(default=False)
    joined_date = models.DateTimeField(null=True)
    role = models.CharField(max_length=16, choices=TeamRole.choices, default=TeamRole.MEMBER)

    class Meta:
        default_permissions = ()
        constraints = [models.UniqueConstraint(fields=["user", "team"], name="unique_membership")]

    def __str__(self):
        return f"{self.user} - {self.team}"


class Invitation(UserOwnedModel):
    """
    Invitation model represents an invitation sent to a user to join a team.

    Attributes:
        key (CharField): A unique key for the invitation.
        created_date (DateTimeField): The date and time when the invitation was created.
        sent_date (DateTimeField): The date and time when the invitation was sent.
        membership (OneToOneField): A one-to-one relationship with the Membership model.
    """

    key = models.CharField(max_length=64, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sent_date = models.DateTimeField(null=True)
    membership = models.OneToOneField(
        Membership, on_delete=models.CASCADE, related_name="invitation"
    )

    class Meta:
        default_permissions = ()

    @property
    def team_id(self):
        """
        Returns the ID of the team associated with the invitation.
        """

        return self.membership.team.id

    @property
    def accepted(self):
        """
        Returns whether the invitation has been accepted.
        """

        return self.membership.is_active

    def send(self):
        """
        Sends the invitation using the configured email backend.
        """

        # TODO: use email backend to send invitations as well
        if settings.EMAIL_BACKEND is None:
            raise ImproperlyConfigured("Email backend is not configured")

    def accept(self, date=None):
        """
        Accepts the invitation and activates the membership.
        """

        if not self.membership.is_active:
            self.membership.is_active = True
            if date is None:
                self.membership.joined_date = timezone.now()
            else:
                self.membership.joined_date = date
            self.membership.save()
