# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings

from genflow.apps.iam.permissions import GenFLowBasePermission, StrEnum
from genflow.apps.team.models import TeamRole


class ProviderPermission(GenFLowBasePermission):
    """
    Handles the permissions for provider-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        CREATE = "create"
        RETRIEVE = "retrieve"
        DELETE = "delete"
        UPDATE = "update"
        LIST = "list"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "create": Scopes.CREATE,
                "retrieve": Scopes.RETRIEVE,
                "destroy": Scopes.DELETE,
                "partial_update": Scopes.UPDATE,
                "list": Scopes.LIST,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "provider":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        """
        Checks if the user has access based on their group name and team role.
        """

        # admin users have full control
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return True

        # team owner can enable a provider
        # team owner can retrieve enabled a provider
        # team owner can disable a provider
        # team owner can update enabled a provider
        if (
            self.scope == self.Scopes.CREATE
            or self.scope == self.Scopes.RETRIEVE
            or self.scope == self.Scopes.DELETE
            or self.scope == self.Scopes.UPDATE
            or self.scope == self.Scopes.LIST
        ):
            if self.team_role == TeamRole.OWNER.value:
                return True

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset


class AIModelPermission(GenFLowBasePermission):
    """
    Handles the permissions for model-related actions.
    """

    class Scopes(StrEnum):
        """
        Defines the possible scopes of actions.
        """

        LIST = "list"
        RETRIEVE = "retrieve"
        PARAMETER_CONFIG = "parameter_config"

    @staticmethod
    def get_scopes(request, view, obj):
        """
        Returns the scope of the action being performed based on the view's action.
        """

        Scopes = __class__.Scopes
        return [
            {
                "list": Scopes.LIST,
                "retrieve": Scopes.RETRIEVE,
                "parameter_config": Scopes.PARAMETER_CONFIG,
            }.get(view.action, None)
        ]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        """
        Creates and returns a list of permissions based on the request, view, and object.
        """

        permissions = []
        if view.basename == "model":
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        """
        Checks if the user has access based on their group name and team role.
        """

        # admin users have full control
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return True

        # team owner can enable a provider
        # team owner can retrieve enabled a provider
        # team owner can disable a provider
        # team owner can update enabled a provider
        if (
            self.scope == self.Scopes.LIST
            or self.scope == self.Scopes.RETRIEVE
            or self.scope == self.Scopes.PARAMETER_CONFIG
        ):
            if self.team_role == TeamRole.OWNER.value:
                return True

        return False

    def filter(self, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset


class EntityGroupPermission:
    """
    Handles the permissions for entity group-related actions.
    It must be inherited by the entity group permission classes.
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

    @classmethod
    def get_scopes_dict(cls):
        """
        Returns a dictionary of scopes for easy access.
        """

        return {
            "list": cls.Scopes.LIST,
            "create": cls.Scopes.CREATE,
            "retrieve": cls.Scopes.RETRIEVE,
            "destroy": cls.Scopes.DELETE,
            "partial_update": cls.Scopes.UPDATE,
        }

    @classmethod
    def check_base_scopes(cls, subclass: GenFLowBasePermission, is_team_owner: bool) -> bool:
        """
        Checks base scopes for entity-related actions.
        """

        # team member cam list groups
        # team member can create a group
        # team member can retrieve a group
        if (
            subclass.scope == cls.Scopes.LIST
            or subclass.scope == cls.Scopes.CREATE
            or subclass.scope == cls.Scopes.RETRIEVE
        ):
            return subclass.team_role is not None

        # team owner or group owner can update the group
        # team owner or group owner can delete the group
        if subclass.scope == cls.Scopes.UPDATE or subclass.scope == cls.Scopes.DELETE:
            return is_team_owner or subclass.obj.owner_id == subclass.user_id

        return False

    @classmethod
    def filter(cls, subclass: GenFLowBasePermission, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset


class EntityBasePermission:
    """
    Handles the permissions for entity-related actions.
    It must be inherited by the entity permission classes.
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

    @classmethod
    def get_scopes_dict(cls):
        """
        Returns a dictionary of scopes for easy access.
        """

        return {
            "list": cls.Scopes.LIST,
            "create": cls.Scopes.CREATE,
            "retrieve": cls.Scopes.RETRIEVE,
            "destroy": cls.Scopes.DELETE,
            "partial_update": cls.Scopes.UPDATE,
            "upload_avatar": cls.Scopes.UPLOAD_AVATAR,
        }

    @classmethod
    def check_base_scopes(cls, subclass: GenFLowBasePermission, is_team_owner: bool) -> bool:
        """
        Checks base scopes for entity-related actions.
        """

        # team member cam list entities
        # team member can create an entity
        # team member can retrieve an entity
        if (
            subclass.scope == cls.Scopes.LIST
            or subclass.scope == cls.Scopes.CREATE
            or subclass.scope == cls.Scopes.RETRIEVE
        ):
            return subclass.team_role is not None

        # team owner or entity owner can update the entity
        # team owner or entity owner can upload avatar
        # team owner or entity owner can delete the entity
        if (
            subclass.scope == cls.Scopes.UPDATE
            or subclass.scope == cls.Scopes.UPLOAD_AVATAR
            or subclass.scope == cls.Scopes.DELETE
        ):
            return is_team_owner or subclass.obj.owner_id == subclass.user_id

        return False

    @classmethod
    def filter(cls, subclass: GenFLowBasePermission, queryset):
        """'
        Filters the queryset based on the permissions
        """

        return queryset
