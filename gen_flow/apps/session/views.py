# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import shutil
from os import path as osp

from rest_framework import viewsets
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema_view, extend_schema
)
from rest_framework.permissions import SAFE_METHODS

from gen_flow.apps.session import permissions as perms
from gen_flow.apps.session.models import Session
from gen_flow.apps.session.serializers import SessionReadSerializer, SessionWriteSerializer

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
