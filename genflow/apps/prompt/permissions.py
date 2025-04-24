# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings

from genflow.apps.team.models import TeamRole
from genflow.apps.iam.permissions import GenFLowBasePermission
from genflow.apps.core.permissions import EntityGroupPermission, EntityBasePermission


class PromptGroupPermission(GenFLowBasePermission, EntityGroupPermission):
    """
    Handles the permissions for prompt group-related actions.
    """

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        scopes_dict = EntityBasePermission.get_scopes_dict()

        return [
            scopes_dict.get(view.action, None)
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
        return EntityBasePermission.check_base_scopes(self, is_team_owner)

    def filter(self, queryset):
        """
        Filters the queryset based on the user's permissions.
        """

        return EntityGroupPermission.filter(self, queryset)

class PromptPermission(GenFLowBasePermission, EntityBasePermission):
    """
    Handles the permissions for prompt-related actions.
    """

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        scopes_dict = EntityBasePermission.get_scopes_dict()

        return [
            scopes_dict.get(view.action, None)
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
        return EntityBasePermission.check_base_scopes(self, is_team_owner)

    def filter(self, queryset):
        """
        Filters the queryset based on the user's permissions.
        """

        return EntityBasePermission.filter(self, queryset)
