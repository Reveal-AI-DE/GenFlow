# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.conf import settings

from genflow.apps.iam.permissions import GenFLowBasePermission, StrEnum
from genflow.apps.restriction.mixin import LimitMixin
from genflow.apps.session.models import Session, SessionMessage
from genflow.apps.team.models import TeamRole


class SessionPermission(GenFLowBasePermission, LimitMixin):
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
        GENERATE = "generate"
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
                "generate": Scopes.GENERATE,
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
                # special case for generate -> check access should be
                # done in the session message permission with create scope
                if scope == cls.Scopes.GENERATE:
                    self = SessionMessagePermission.create_base_perm(
                        request, view, cls.Scopes.CREATE, iam_context, obj
                    )
                    self.session_id = obj.id
                else:
                    self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def get_user_usage(self) -> int:
        """
        Get the number of session owned by the user.
        """

        return Session.objects.filter(owner_id=self.user_id).count()

    def get_team_usage(self) -> int:
        """
        Get the number of session owned by the team.
        """

        if self.team_id is None:
            return 0

        return Session.objects.filter(team_id=self.team_id).count()

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
            key="SESSION",
        ):
            return False

        is_team_owner = self.team_role and self.team_role == TeamRole.OWNER.value

        # team member can list sessions
        # team member can create a session
        # team member can retrieve a session
        # team member can generate a message
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


class SessionMessagePermission(GenFLowBasePermission, LimitMixin):
    """
    Handles the permissions for session message-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        LIST = "list"
        CREATE = "create"

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

    def get_user_usage(self) -> int:
        """
        Get the number of messages per session owned by the user.
        """

        if hasattr(self, "session_id"):
            return SessionMessage.objects.filter(
                session_id=self.session_id, owner_id=self.user_id
            ).count()

        return SessionMessage.objects.filter(owner_id=self.user_id).count()

    def get_team_usage(self) -> int:
        """
        Get the number of messages per session owned by the team.
        """

        if self.team_id is None:
            return 0

        if hasattr(self, "session_id"):
            return SessionMessage.objects.filter(
                session_id=self.session_id, owner_id=self.user_id
            ).count()

        return SessionMessage.objects.filter(team_id=self.team_id).count()

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
            key="MESSAGE",
        ):
            return False

        # team member can list session messages
        # team member can create a session message
        if self.scope == self.Scopes.LIST or self.scope == self.Scopes.CREATE:
            return self.team_role is not None

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset
