# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import TypeVar, Optional, Dict, Any, Sequence
from abc import ABCMeta, abstractmethod
from enum import Enum

from rest_framework.permissions import BasePermission
from django.conf import settings
from django.db.models import Model

from gen_flow.apps.team.models import Membership, Team

class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value

def get_team(request, obj):
    '''
    Retrieve the team associated with the given object or request.

    Returns:
        Team or None

    Raises:
        AttributeError: If the object does not have a 'team_id' attribute and is not listed in settings.OBJECTS_NOT_RELATED_WITH_TEAM.
    '''

    if isinstance(obj, Team):
        return obj

    if obj:
        try:
            team_id = getattr(obj, 'team_id')
        except AttributeError as exc:
            # Skip initialization of team for those objects that don't related with team
            view = request.parser_context.get('view')
            if view and view.basename in settings.OBJECTS_NOT_RELATED_WITH_TEAM:
                return request.iam_context['team']

            raise exc

        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return None

    return request.iam_context['team']

def get_membership(request, team):
    '''
    Retrieve the active membership of a user in a given team.
    '''

    if team is None:
        return None

    return Membership.objects.filter(
        team=team,
        user=request.user,
        is_active=True
    ).first()

def build_iam_context(request, team: Optional[Team], membership: Optional[Membership]):
    '''
    Builds the IAM context dictionary for a given request, team, and membership.

    Returns:
        dict: A dictionary containing the IAM context with the following keys:
            - 'user_id': The ID of the user making the request.
            - 'group_name': The privilege group name from the IAM context in the request.
            - 'team_id': The ID of the team, or None if the team is not provided.
            - 'team_owner_id': The ID of the team owner, or None if the team is not provided.
            - 'team_role': The role of the user in the team, or None if the membership is not provided.
    '''

    return {
        'user_id': request.user.id,
        'group_name': request.iam_context['privilege'],
        'team_id': getattr(team, 'id', None),
        'team_owner_id': getattr(team.owner, 'id', None)
            if team else None,
        'team_role': getattr(membership, 'role', None),
    }

def get_iam_context(request, obj) -> Dict[str, Any]:
    '''
    Generate the IAM context for a given request and object.
    '''

    team = get_team(request, obj)
    membership = get_membership(request, team)

    return build_iam_context(request, team, membership)

class GenFLowBasePermission(metaclass=ABCMeta):
    '''
    Abstract base class that defines the structure and behavior for permission handling in the GenFlow application.
    '''

    user_id: int
    group_name: Optional[str]
    team_id: Optional[int]
    team_owner_id: Optional[int]
    team_role: Optional[str]
    scope: str
    obj: Optional[Any]

    @classmethod
    @abstractmethod
    def create(cls, request, view, obj, iam_context) -> Sequence['GenFLowBasePermission']:
        '''
        Abstract method to create a list of permissions based on the request, view, object, and IAM context.
        '''
        ...

    @classmethod
    def create_base_perm(cls, request, view, scope, iam_context, obj=None, **kwargs):
        '''
        Class method to create a base permission instance.
        '''

        if not iam_context and request:
            iam_context = get_iam_context(request, obj)
        return cls(
            scope=scope,
            obj=obj,
            **iam_context, **kwargs)

    def __init__(self, **kwargs):
        '''
        Initializes the permission instance with the provided keyword arguments.
        '''

        self.obj = None
        for name, val in kwargs.items():
            setattr(self, name, val)

    @classmethod
    def create_scope_list(cls, request, iam_context=None):
        '''
        Class method to create a permission instance with a 'list' scope.
        '''

        if not iam_context and request:
            iam_context = get_iam_context(request, None)
        return cls(**iam_context, scope='list')

    @abstractmethod
    def check_access(self) -> bool:
        '''
        Abstract method to check if the permission grants access.
        '''
        ...

    @abstractmethod
    def filter(self, queryset):
        '''
        Abstract method to filter a queryset based on the permission.
        '''
        ...

T = TypeVar('T', bound=Model)

def is_public_obj(obj: T) -> bool:
    return getattr(obj, 'is_public', False)

class PermissionEnforcer(BasePermission):
    '''
    Custom permission class that extends BasePermission.
    It provides methods to check permissions for incoming requests in a Django Rest Framework (DRF) application.
    '''

    # pylint: disable=no-self-use
    def check_permission(self, request, view, obj) -> bool:
        '''
        Checks if the request has the necessary permissions to access the object.
        Handles DRF's OPTIONS requests and public objects separately.
        Iterates through all subclasses of GenFlowBasePermission to check access.
        '''

        # DRF can send OPTIONS request. Internally it will try to get
        # information about serializers for PUT and POST requests (clone
        # request and replace the http method). To avoid handling
        # ('POST', 'metadata') and ('PUT', 'metadata') in every request,
        # the condition below is enough.
        if self.is_metadata_request(request, view) or obj and is_public_obj(obj):
            return True

        iam_context = get_iam_context(request, obj)
        for perm_class in GenFLowBasePermission.__subclasses__():
            for perm in perm_class.create(request, view, obj, iam_context):
                result = perm.check_access()
                if not result:
                    return False

        return True

    def has_permission(self, request, view):
        '''
        Checks if the request has the necessary permissions to access the view.
        If the view is not a detail view, it delegates to check_permission.
        '''

        if not view.detail:
            return self.check_permission(request, view, None)
        else:
            return True # has_object_permission will be called later

    def has_object_permission(self, request, view, obj):
        '''
        Checks if the request has the necessary permissions to access the specific object.
        Delegates to check_permission.
        '''

        return self.check_permission(request, view, obj)

    @staticmethod
    def is_metadata_request(request, view):
        '''
        Static method that checks if the request is a metadata request.
        Returns True if the request method is OPTIONS or if it is a POST request with 'metadata' action and no data.
        '''

        return request.method == 'OPTIONS' \
            or (request.method == 'POST' and view.action == 'metadata' and len(request.data) == 0)
