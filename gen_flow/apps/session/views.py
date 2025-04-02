# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import shutil
from os import path as osp

from rest_framework import viewsets, status
from drf_spectacular.utils import (
    OpenApiResponse, OpenApiParameter, OpenApiTypes,
    extend_schema_view, extend_schema
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from gen_flow.apps.session import permissions as perms
from gen_flow.apps.session.models import Session, SessionMessage
from gen_flow.apps.session.serializers import (SessionReadSerializer, SessionWriteSerializer,
    SessionMessageReadSerializer, SessionMessageWriteSerializer)

@extend_schema(tags=['sessions'])
@extend_schema_view(
    list=extend_schema(
        summary='List sessions',
        description='List all sessions that the user has access to.',
        responses={
            200: SessionReadSerializer(many=True),
        }
    ),
    create=extend_schema(
        summary='Create a session',
        description='Create a new session with the given data.',
        request=SessionWriteSerializer,
        responses={
            201: SessionReadSerializer,
        }
    ),
    partial_update=extend_schema(
        summary='Update a session',
        description='Update the session with the given data.',
        request=SessionWriteSerializer,
        responses={
            200: SessionReadSerializer,
        }
    ),
    retrieve=extend_schema(
        summary='Retrieve a session',
        description='Retrieve the session with the given ID.',
        responses={
            200: SessionReadSerializer,
        }
    ),
    destroy=extend_schema(
        summary='Delete a session',
        description='Delete the session with the given ID.',
        responses={
            204: OpenApiResponse(description='The session has been deleted'),
        }
    ),
)
class SessionViewSet(viewsets.ModelViewSet):
    '''
    Provides CRUD operations and additional functionality
    for managing Session objects.
    '''

    queryset = Session.objects.all().order_by('created_date')
    iam_team_field = 'team'

    def get_serializer_class(self):
        '''
        Returns the appropriate serializer class based on the HTTP method.
        '''

        if self.request.method in SAFE_METHODS:
            return SessionReadSerializer
        else:
            return SessionWriteSerializer

    def get_queryset(self):
        '''
        Returns the queryset for the view. Applies additional filtering for the 'list' action
            based on permissions.
        '''

        queryset = super().get_queryset()

        if self.action == 'list':
            perm = perms.SessionPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def perform_create(self, serializer):
        '''
        Saves a new Session instance, associating it with the current user and team.
        '''

        extra_kwargs = {
            'owner': self.request.user,
            'team': self.request.iam_context['team']
        }
        serializer.save(**extra_kwargs)

    def perform_destroy(self, instance: Session):
        '''
        Deletes a Session instance and removes its associated directory if it exists.
        '''

        if osp.exists(instance.dirname):
            shutil.rmtree(instance.dirname)
        return super().perform_destroy(instance)


@extend_schema(tags=['messages'])
@extend_schema_view(
    list=extend_schema(
        summary='List messages',
        description='List all messages that belong to a session.',
        parameters=[
            OpenApiParameter(
                'session',
                description='The ID of the session to filter messages by.',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                required=True,
            ),
        ],
        responses={
            200: SessionMessageReadSerializer(many=True),
        }
    ),
)
class SessionMessageViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
):
    '''
    Provides CRUD operations and additional functionality
    for managing SessionMessage objects.
    '''

    queryset = SessionMessage.objects.all().order_by('created_date')
    filterset_fields = ['session']
    iam_team_field = 'team'

    def get_serializer_class(self):
        '''
        Returns the appropriate serializer class based on the HTTP method.
        '''

        if self.request.method in SAFE_METHODS:
            return SessionMessageReadSerializer

    def get_queryset(self):
        '''
        Returns the queryset for the view. Applies additional filtering for the 'list' action
            based on permissions.
        '''

        queryset = super().get_queryset()

        if self.action == 'list':
            perm = perms.SessionMessagePermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        session = request.query_params.get('session', None)
        if not session:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='session ID is required to list messages'
            )
        return super().list(request, *args, **kwargs)
