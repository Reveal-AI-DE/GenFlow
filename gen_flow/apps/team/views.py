# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import mixins, viewsets
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.permissions import SAFE_METHODS

import gen_flow.apps.team.models as models
import gen_flow.apps.team.serializers as serializers


@extend_schema(tags=['teams'])
@extend_schema_view(
    list=extend_schema(
        summary='List teams',
        description='Retrieve a list of all teams. Supports '
            'filtering and searching by name and owner username.',
        responses={
            '200': serializers.TeamReadSerializer(many=True),
        }),
    retrieve=extend_schema(
        summary='Get team details',
        description='Retrieve detailed information about a specific team by its ID.',
        responses={
            '200': serializers.TeamReadSerializer,
        }),
    partial_update=extend_schema(
        summary='Updates a team',
        description='Partially update the details of a specific team.'
            'Only the provided fields will be updated.',
        request= serializers.TeamWriteSerializer(partial=True),
        responses={
            '200': serializers.TeamReadSerializer,
        }),
    create=extend_schema(
        summary='Create a team',
        description='Create a new team with the provided details.',
        request=serializers.TeamWriteSerializer,
        responses={
            '201': serializers.TeamReadSerializer,
        }),
    destroy=extend_schema(
        summary='Delete a team',
        description='Delete a specific team by its ID.',
        responses={
            '204': OpenApiResponse(description='The team has been deleted'),
        })
)
class TeamViewSet(viewsets.ModelViewSet):
    '''
    TeamViewSet is a viewset for handling CRUD operations on the Team model.
    '''

    queryset = models.Team.objects.select_related('owner').all()
    search_fields = ('name', 'owner__username')
    filterset_fields = list(search_fields) + ['id']
    ordering_fields = list(filterset_fields)
    ordering = '-id'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        '''
        Returns the appropriate serializer class based on the request method.'
        '''

        if self.request.method in SAFE_METHODS:
            return serializers.TeamReadSerializer
        else:
            return serializers.TeamWriteSerializer

    def perform_create(self, serializer):
        '''
        Saves the serializer with additional keyword arguments.
        '''

        extra_kwargs = {'owner': self.request.user}
        serializer.save(**extra_kwargs)


@extend_schema(tags=['memberships'])
@extend_schema_view(
    retrieve=extend_schema(
        summary='Get membership details',
        description='Retrieve detailed information about a specific membership by its ID.',
        responses={
            '200': serializers.MembershipReadSerializer,
        }),
    list=extend_schema(
        summary='List memberships',
        description='Retrieve a list of all memberships.'
            'Supports filtering and searching by user username and role.',
        responses={
            '200': serializers.MembershipReadSerializer(many=True),
        }),
    partial_update=extend_schema(
        summary='Update a membership',
        description='Partially update the details of a specific membership.'
            'Only the provided fields will be updated.',
        request=serializers.MembershipWriteSerializer(partial=True),
        responses={
            '200': serializers.MembershipReadSerializer,
        }),
    destroy=extend_schema(
        summary='Delete a membership',
        description='Delete a specific membership by its ID.',
        responses={
            '204': OpenApiResponse(description='The membership has been deleted'),
        })
)
class MembershipViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    '''
    MembershipViewSet is a viewset for handling CRUD operations on the Membership model.
    '''

    queryset = models.Membership.objects.select_related('invitation', 'user').all()
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    search_fields = ('user__username', 'role')
    filterset_fields = list(search_fields) + ['id']
    ordering_fields = list(filterset_fields)
    ordering = '-joined_date'

    def get_serializer_class(self):
        '''
        Returns the appropriate serializer class based on the request method.
        '''

        if self.request.method in SAFE_METHODS:
            return serializers.MembershipReadSerializer
        else:
            return serializers.MembershipWriteSerializer
