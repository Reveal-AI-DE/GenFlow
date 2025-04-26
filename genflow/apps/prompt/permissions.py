# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings

from genflow.apps.core.permissions import EntityBasePermission, EntityGroupPermission
from genflow.apps.iam.permissions import GenFLowBasePermission
from genflow.apps.team.models import TeamRole
from genflow.apps.restriction.mixin import LimitMixin
from genflow.apps.core.models import EntityGroup
from genflow.apps.prompt.models import Prompt


class PromptGroupPermission(GenFLowBasePermission, EntityGroupPermission, LimitMixin):
    """
    Handles the permissions for prompt group-related actions.
    """

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        scopes_dict = EntityBasePermission.get_scopes_dict()

        return [scopes_dict.get(view.action, None)]

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

    def get_user_usage(self) -> int:
        """
        Get the number of prompt group owned by the user.
        """

        return EntityGroup.objects.filter(
            entity_type=Prompt.__name__.lower(),
            owner_id=self.user_id
        ).count()

    def get_team_usage(self) -> int:
        """
        Get the number of prompt group owned by the team.
        """

        if self.team_id is None:
            return 0

        return EntityGroup.objects.filter(
            entity_type=Prompt.__name__.lower(),
            team_id=self.team_id
        ).count()

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

        # check limits
        if (
            self.scope == self.Scopes.CREATE
            and self.check_limit(
                user_id=self.user_id,
                team_id=self.team_id,
                key="PROMPT_GROUP",
            )
        ):
            return False

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value
        return EntityBasePermission.check_base_scopes(self, is_team_owner)

    def filter(self, queryset):
        """
        Filters the queryset based on the user's permissions.
        """

        return EntityGroupPermission.filter(self, queryset)


class PromptPermission(GenFLowBasePermission, EntityBasePermission, LimitMixin):
    """
    Handles the permissions for prompt-related actions.
    """

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        scopes_dict = EntityBasePermission.get_scopes_dict()

        return [scopes_dict.get(view.action, None)]

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

    def get_user_usage(self) -> int:
        """
        Get the number of prompt owned by the user.
        """

        return Prompt.objects.filter(
            owner_id=self.user_id
        ).count()

    def get_team_usage(self) -> int:
        """
        Get the number of prompt owned by the team.
        """

        if self.team_id is None:
            return 0

        return Prompt.objects.filter(
            team_id=self.team_id
        ).count()

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

        # check limits
        if (
            self.scope == self.Scopes.CREATE
            and self.check_limit(
                user_id=self.user_id,
                team_id=self.team_id,
                key="PROMPT",
            )
        ):
            return False

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value
        return EntityBasePermission.check_base_scopes(self, is_team_owner)

    def filter(self, queryset):
        """
        Filters the queryset based on the user's permissions.
        """

        return EntityBasePermission.filter(self, queryset)
