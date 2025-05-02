# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.conf import settings
from django.db.models import Q

from genflow.apps.iam.permissions import GenFLowBasePermission, StrEnum
from genflow.apps.restriction.mixin import LimitMixin
from genflow.apps.team.models import Invitation, Team, TeamRole


class TeamPermission(GenFLowBasePermission, LimitMixin):
    """
    Handles the permissions for team-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines various permission scopes.
        """

        LIST = "list"
        CREATE = "create"
        DELETE = "delete"
        UPDATE = "update"
        VIEW = "view"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Gets the scope based on the view action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
                "create": Scopes.CREATE,
                "destroy": Scopes.DELETE,
                "partial_update": Scopes.UPDATE,
                "retrieve": Scopes.VIEW,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "team":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def get_user_usage(self) -> int:
        """
        Get the number of teams owned by the user.
        """

        return Team.objects.filter(owner_id=self.user_id).count()

    def get_team_usage(self) -> int:
        """
        Get the number of teams owned by the team.
        """

        if self.team_id is None:
            return 0

        return Team.objects.filter(team_id=self.team_id).count()

    def check_access(self) -> bool:
        """
        Check if the user has access based on their role and the scope.
        """

        # admin users have full control
        # filter method will be used to filter queryset in list method

        # check limits
        if self.scope == self.Scopes.CREATE and self.check_limit(
            user_id=self.user_id,
            team_id=self.team_id,
            key="TEAM",
        ):
            return False

        # anyone can create a team for now
        if (
            self.group_name == settings.IAM_ADMIN_ROLE
            or self.scope == self.Scopes.LIST
            or self.scope == self.Scopes.CREATE
        ):
            return True
        # team owner can delete the team
        elif self.scope == self.Scopes.DELETE:
            if self.team_role == TeamRole.OWNER.value:
                return True
        # team owner or admin can change the team's data
        elif self.scope == self.Scopes.UPDATE:
            if self.team_role == TeamRole.OWNER.value or self.team_role == TeamRole.ADMIN.value:
                return True
        # team member can view the team's data
        elif self.scope == self.Scopes.VIEW:
            if self.team_role is not None:
                return True
        return False

    def filter(self, queryset):
        """
        Filters the queryset based on the user's role and membership status.
        """

        # Don't filter queryset for admin
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return queryset
        # get teams where the user is the owner or a member with active membership
        else:
            return queryset.filter(
                Q(owner_id=self.user_id)
                | (Q(members__user_id=self.user_id) & Q(members__is_active=True))
            ).distinct()


class MembershipPermission(GenFLowBasePermission):
    """
    Handles the permissions for membership-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines various permission scopes.
        """

        LIST = "list"
        DELETE = "delete"
        UPDATE = "update"
        VIEW = "view"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Gets the scope based on the view action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
                "destroy": Scopes.DELETE,
                "partial_update": Scopes.UPDATE,
                "retrieve": Scopes.VIEW,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "membership":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        """
        Check if the user has access based on their role and the scope.
        """

        team_owner_or_admin = self.team_role and (
            self.team_role == TeamRole.OWNER.value or self.team_role == TeamRole.ADMIN.value
        )

        # admin users have full control
        # filter method will be used to filter queryset in list method
        if self.group_name == settings.IAM_ADMIN_ROLE or self.scope == self.Scopes.LIST:
            return True
        # team owner or admin can delete its memberships
        elif self.scope == self.Scopes.DELETE:
            if team_owner_or_admin:
                return True
        # team owner or admin can change the membership's data
        elif self.scope == self.Scopes.UPDATE:
            if team_owner_or_admin:
                return True
        # team member can view its membership, in addition to team owner and admin
        elif self.scope == self.Scopes.VIEW:
            if self.obj.user.id == self.user_id or team_owner_or_admin:
                return True
        return False

    def filter(self, queryset):
        """
        Filters the queryset based on the user's role and membership status.
        """

        # Don't filter queryset for admin
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return queryset
        # get memberships where the user is the owner or a member with active membership
        else:
            # user can list their membership in current team
            # in addition to memberships of teams he owns
            if self.team_id:
                return queryset.filter(
                    Q(team_id=self.team_id)
                    & (Q(user_id=self.user_id) | Q(team__owner_id=self.user_id))
                ).distinct()
            # if team_id is not provided, user can list all memberships of teams he owns
            return queryset.filter(Q(team__owner_id=self.user_id)).distinct()


class InvitationPermission(GenFLowBasePermission, LimitMixin):
    """
    Handles the permissions for invitation-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines various permission scopes.
        """

        LIST = "list"
        CREATE = "create"
        UPDATE = "update"
        VIEW = "view"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Gets the scope based on the view action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
                "create": Scopes.CREATE,
                "partial_update": Scopes.UPDATE,
                "retrieve": Scopes.VIEW,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "invitation":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def get_user_usage(self) -> int:
        """
        Get the number of teams owned by the user.
        """

        return Invitation.objects.filter(owner_id=self.user_id).count()

    def get_team_usage(self) -> int:
        """
        Get the number of teams owned by the team.
        """

        if self.team_id is None:
            return 0

        return Invitation.objects.filter(membership__team_id=self.team_id).count()

    def check_access(self) -> bool:
        """
        Check if the user has access based on their role and the scope.
        """

        team_owner_or_admin = self.team_role and (
            self.team_role == TeamRole.OWNER.value or self.team_role == TeamRole.ADMIN.value
        )

        # admin users have full control
        # filter method will be used to filter queryset in list method
        if self.group_name == settings.IAM_ADMIN_ROLE or self.scope == self.Scopes.LIST:
            return True

        # check limits
        if self.scope == self.Scopes.CREATE and self.check_limit(
            user_id=self.user_id,
            team_id=self.team_id,
            key="MAX_INVITATION_PER_TEAM",
        ):
            return False

        # team owner or admin can create an invitation
        # team owner or admin can change the invitation's data
        elif self.scope == self.Scopes.CREATE or self.scope == self.Scopes.UPDATE:
            if team_owner_or_admin:
                return True
        # team member can view its invitation, in addition to team owner and admin
        elif self.scope == self.Scopes.VIEW:
            if self.obj.membership.user.id == self.user_id or team_owner_or_admin:
                return True
        return False

    def filter(self, queryset):
        """
        Filters the queryset based on the user's role and membership status.
        """

        # Don't filter queryset for admin
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return queryset
        # get invitations where the user is the owner or a member with active membership
        else:
            # user can list all invitations he owns or of teams he owns
            return queryset.filter(
                Q(owner_id=self.user_id) | Q(membership__team__owner_id=self.user_id)
            ).distinct()
