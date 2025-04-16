# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings

from gen_flow.apps.iam.permissions import GenFLowBasePermission, StrEnum
from gen_flow.apps.team.models import TeamRole


class PromptGroupPermission(GenFLowBasePermission):
    """
    Handles the permissions for prompt group-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        LIST = "list"
        CREATE = "create"
        RETRIEVE = "retrieve"
        UPDATE = "update"
        DELETE = "delete"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
                "create": Scopes.CREATE,
                "retrieve": Scopes.RETRIEVE,
                "destroy": Scopes.DELETE,
                "partial_update": Scopes.UPDATE,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "prompt-group":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        """
        Checks if the user has access based on their group name and team role.
        """
        # if no team -> no access
        if self.team_id is None:
            return False

        # admin users have full control
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return True

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value

        # team member cam list prompt groups
        # team member can create a prompt group
        # team member can retrieve a prompt group
        if (
            self.scope == self.Scopes.LIST
            or self.scope == self.Scopes.CREATE
            or self.scope == self.Scopes.RETRIEVE
        ):
            return self.team_role is not None

        # team owner or prompt group owner can update the prompt group
        # team owner or prompt group owner can delete the prompt group
        if self.scope == self.Scopes.UPDATE or self.scope == self.Scopes.DELETE:
            return is_team_owner or self.obj.owner_id == self.user_id

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset


class PromptPermission(GenFLowBasePermission):
    """
    Handles the permissions for prompt-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        LIST = "list"
        CREATE = "create"
        RETRIEVE = "retrieve"
        UPDATE = "update"
        DELETE = "delete"
        UPLOAD_AVATAR = "upload_avatar"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
                "create": Scopes.CREATE,
                "retrieve": Scopes.RETRIEVE,
                "destroy": Scopes.DELETE,
                "partial_update": Scopes.UPDATE,
                "upload_avatar": Scopes.UPLOAD_AVATAR,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "prompt":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        """
        Checks if the user has access based on their group name and team role.
        """
        # if no team -> no access
        if self.team_id is None:
            return False

        # admin users have full control
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return True

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value

        # team member cam list prompt groups
        # team member can create a prompt group
        # team member can retrieve a prompt group
        if (
            self.scope == self.Scopes.LIST
            or self.scope == self.Scopes.CREATE
            or self.scope == self.Scopes.RETRIEVE
        ):
            return self.team_role is not None

        # team owner or prompt group owner can update the prompt group
        # team owner or prompt group owner can delete the prompt group
        if self.scope == self.Scopes.UPDATE or self.scope == self.Scopes.DELETE:
            return is_team_owner or self.obj.owner_id == self.user_id

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset
