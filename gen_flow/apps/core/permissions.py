# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings

from gen_flow.apps.team.models import TeamRole
from gen_flow.apps.iam.permissions import StrEnum, GenFLowBasePermission

class ProviderPermission(GenFLowBasePermission):
    class Scopes(StrEnum):
        CREATE = 'create'
        RETRIEVE = 'retrieve'
        DELETE = 'delete'
        UPDATE = 'update'

    @staticmethod
    def get_scopes(request, view, obj):
        Scopes = __class__.Scopes
        return [{
            'create': Scopes.CREATE,
            'retrieve': Scopes.RETRIEVE,
            'destroy': Scopes.DELETE,
            'partial_update': Scopes.UPDATE
        }.get(view.action, None)]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        permissions = []
        if view.basename == 'provider':
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        # admin users have full control
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return True

        # team owner can enable a provider
        # team owner can retrieve enabled a provider
        # team owner can disable a provider
        # team owner can update enabled a provider
        if self.scope == self.Scopes.CREATE or \
            self.scope == self.Scopes.RETRIEVE or \
            self.scope == self.Scopes.DELETE or \
            self.scope == self.Scopes.UPDATE:
            if self.team_role == TeamRole.OWNER.value:
                return True

        return False

    def filter(self, queryset):
        return queryset
