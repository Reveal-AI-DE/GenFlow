# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings

from genflow.apps.iam.permissions import GenFLowBasePermission, StrEnum
from genflow.apps.team.models import TeamRole


class SessionPermission(GenFLowBasePermission):
    """
    Handles the permissions for session-related actions.
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
        LIST_FILES = "list_files"
        UPLOAD_FILE = "upload_file"
        DELETE_FILE = "delete_file"

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
                "list_files": Scopes.LIST_FILES,
                "upload_file": Scopes.UPLOAD_FILE,
                "delete_file": Scopes.DELETE_FILE,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "session":
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

        # team member can list sessions
        # team member can create a session
        # team member can retrieve a session
        # team member can upload a file

        if (
            self.scope == self.Scopes.LIST
            or self.scope == self.Scopes.CREATE
            or self.scope == self.Scopes.RETRIEVE
            or self.scope == self.Scopes.UPLOAD_FILE
        ):
            return self.team_role is not None

        # team owner or sessions owner can update the sessions
        # team owner or sessions owner can delete the sessions
         # team owner or sessions owner can list files
        # team owner or sessions owner can delete a file
        if (
            self.scope == self.Scopes.UPDATE
            or self.scope == self.Scopes.DELETE
            or self.scope == self.Scopes.LIST_FILES
            or self.scope == self.Scopes.DELETE_FILE
        ):
            return is_team_owner or self.obj.owner_id == self.user_id

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset


class SessionMessagePermission(GenFLowBasePermission):
    """
    Handles the permissions for session message-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        LIST = "list"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "message":
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

        # team member can list session messages
        if self.scope == self.Scopes.LIST:
            return self.team_role is not None

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset
