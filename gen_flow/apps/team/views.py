# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import viewsets
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
