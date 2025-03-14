# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.db.models import Q

from gen_flow.apps.team.models import TeamRole
from gen_flow.apps.iam.permissions import StrEnum, GenFLowBasePermission


class TeamPermission(GenFLowBasePermission):
    '''
    Handles the permissions for team-related actions.
    '''

    class Scopes(StrEnum):
        '''
        Defines various permission scopes.
        '''

        LIST = 'list'
        CREATE = 'create'
        DELETE = 'delete'
        UPDATE = 'update'
        VIEW = 'view'

    @staticmethod
    def get_scopes(request, view, obj):
        '''
        Gets the scope based on the view action.
        '''

        Scopes = __class__.Scopes
        return [{
            'list': Scopes.LIST,
            'create': Scopes.CREATE,
            'destroy': Scopes.DELETE,
            'partial_update': Scopes.UPDATE,
            'retrieve': Scopes.VIEW,
        }.get(view.action, None)]

    @classmethod
    def create(cls, request, view, obj, iam_context):
        '''
        Creates permissions based on the request, view, and object.
        '''

        permissions = []
        if view.basename == 'team':
            for scope in cls.get_scopes(request, view, obj):
                self = cls.create_base_perm(request, view, scope, iam_context, obj)
                permissions.append(self)

        return permissions

    def check_access(self) -> bool:
        '''
        Check if the user has access based on their role and the scope.
        '''

        # admin users have full control
        # filter method will be used to filter queryset in list method

        # anyone can create a team for now
        if self.group_name == settings.IAM_ADMIN_ROLE or \
            self.scope == self.Scopes.LIST or \
            self.scope == self.Scopes.CREATE:
            return True
        # team owner can delete the team
        elif self.scope == self.Scopes.DELETE:
            if self.team_role == TeamRole.OWNER.value:
                return True
        # team owner or admin can change the team's data
        elif self.scope == self.Scopes.UPDATE:
            if self.team_role == TeamRole.OWNER.value \
                or self.team_role == TeamRole.ADMIN.value:
                return True
        # team member can view the team's data
        elif self.scope == self.Scopes.VIEW:
            if self.team_role is not None:
                return True
        return False

    def filter(self, queryset):
        '''
        Filters the queryset based on the user's role and membership status.
        '''

        # Don't filter queryset for admin
        if self.group_name == settings.IAM_ADMIN_ROLE:
            return queryset
        # get teams where the user is the owner or a member with active membership
        else:
            return queryset.filter(
                Q(owner_id=self.user_id) |
                (Q(members__user_id=self.user_id) & Q(members__is_active=True))
            ).distinct()
