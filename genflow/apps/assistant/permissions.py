# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from genflow.apps.iam.permissions import GenFLowBasePermission
from genflow.apps.core.permissions import EntityGroupPermission, EntityBasePermission


class AssistantGroupPermission(GenFLowBasePermission, EntityGroupPermission):
    """
    Handles the permissions for assistant group-related actions.
    """

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

    def check_access(self) -> bool:
        return EntityGroupPermission.check_access(self)

    def filter(self, queryset):
       return EntityGroupPermission.filter(self, queryset)


class AssistantPermission(GenFLowBasePermission, EntityBasePermission):
    """
    Handles the permissions for assistant-related actions.
    """

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

    def check_access(self) -> bool:
        return EntityBasePermission.check_access(self)

    def filter(self, queryset):
       return EntityBasePermission.filter(self, queryset)
