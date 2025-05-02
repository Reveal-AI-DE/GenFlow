# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.conf import settings

from genflow.apps.assistant.models import Assistant
from genflow.apps.core.models import EntityGroup
from genflow.apps.core.permissions import EntityBasePermission, EntityGroupPermission
from genflow.apps.iam.permissions import GenFLowBasePermission, StrEnum
from genflow.apps.restriction.mixin import LimitMixin
from genflow.apps.team.models import TeamRole


class AssistantGroupPermission(GenFLowBasePermission, EntityGroupPermission, LimitMixin):
    """
    Handles the permissions for assistant group-related actions.
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
        if view.basename == "assistant-group":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def get_user_usage(self) -> int:
        """
        Get the number of assistant group owned by the user.
        """

        return EntityGroup.objects.filter(
            entity_type=Assistant.__name__.lower(), owner_id=self.user_id
        ).count()

    def get_team_usage(self) -> int:
        """
        Get the number of assistant group owned by the team.
        """

        if self.team_id is None:
            return 0

        return EntityGroup.objects.filter(
            entity_type=Assistant.__name__.lower(), team_id=self.team_id
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
        if self.scope == self.Scopes.CREATE and self.check_limit(
            user_id=self.user_id,
            team_id=self.team_id,
            key="ASSISTANT_GROUP",
        ):
            return False

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value
        return EntityBasePermission.check_base_scopes(self, is_team_owner)

    def filter(self, queryset):
        """
        Filters the queryset based on the user's permissions.
        """

        return EntityGroupPermission.filter(self, queryset)


class AssistantPermission(GenFLowBasePermission, EntityBasePermission, LimitMixin):
    """
    Handles the permissions for assistant-related actions.
    """

    class FileManagementScopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        LIST_FILES = "list_files"
        UPLOAD_FILE = "upload_file"
        DELETE_FILE = "delete_file"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        scopes_dict = EntityBasePermission.get_scopes_dict()

        FileManagementScopes = __class__.FileManagementScopes
        file_management_scopes_dict = {
            "list_files": FileManagementScopes.LIST_FILES,
            "upload_file": FileManagementScopes.UPLOAD_FILE,
            "delete_file": FileManagementScopes.DELETE_FILE,
        }

        scopes_dict.update(file_management_scopes_dict)

        return [scopes_dict.get(view.action, None)]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "assistant":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def get_user_usage(self) -> int:
        """
        Get the number of assistant owned by the user.
        """

        return Assistant.objects.filter(owner_id=self.user_id).count()

    def get_team_usage(self) -> int:
        """
        Get the number of assistant owned by the team.
        """

        if self.team_id is None:
            return 0

        return Assistant.objects.filter(team_id=self.team_id).count()

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
        if self.scope == self.Scopes.CREATE and self.check_limit(
            user_id=self.user_id,
            team_id=self.team_id,
            key="ASSISTANT",
        ):
            return False

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value

        # team member can list files
        if self.scope == self.FileManagementScopes.LIST_FILES:
            return self.team_role is not None

        # team owner or assistant owner can upload a file
        # team owner or assistant owner can delete a file
        if (
            self.scope == self.FileManagementScopes.UPLOAD_FILE
            or self.scope == self.FileManagementScopes.DELETE_FILE
        ):
            return is_team_owner or self.obj.owner_id == self.user_id

        return EntityBasePermission.check_base_scopes(self, is_team_owner)

    def filter(self, queryset):
        """
        Filters the queryset based on the user's permissions.
        """

        return EntityBasePermission.filter(self, queryset)
