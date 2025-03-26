# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import shutil
from os import path as osp

from rest_framework import viewsets, status
from drf_spectacular.utils import (
    OpenApiTypes, OpenApiParameter, OpenApiResponse,
    extend_schema_view, extend_schema
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action

from gen_flow.apps.prompt import permissions as perms
from gen_flow.apps.prompt.models import PromptGroup, Prompt
from gen_flow.apps.prompt.serializers import (PromptGroupReadSerializer, PromptGroupWriteSerializer,
    PromptReadSerializer, PromptWriteSerializer)


@extend_schema(tags=['prompt-groups'])
@extend_schema_view(
    list=extend_schema(
        summary='List prompt groups',
        description='List all prompt groups',
        responses={
            '200': PromptGroupReadSerializer(many=True),
        }
    ),
    create=extend_schema(
        summary='Create a prompt group',
        description='Create a new prompt group',
        request=PromptGroupWriteSerializer,
        responses={
            '201': PromptGroupReadSerializer,
        }
    ),
    retrieve=extend_schema(
        summary='Get prompt group details',
        description='Get details of a prompt group',
        responses={
            '200': PromptGroupReadSerializer,
        }
    ),
    partial_update=extend_schema(
        summary='Update a prompt group',
        description='Update an existing prompt group',
        request=PromptGroupWriteSerializer,
        responses={
            '200': PromptGroupReadSerializer,
        }
    ),
    destroy=extend_schema(
        summary='Delete a prompt group',
        description='Delete an existing prompt group',
        responses={
            '204': OpenApiResponse(description='The prompt group has been deleted'),
        }
    )
)
class PromptGroupViewSet(viewsets.ModelViewSet):
    '''
    Provides CRUD operations for the PromptGroup model.
    '''
    queryset = PromptGroup.objects.all().order_by('name')
    iam_team_field = 'team'

    def get_serializer_class(self):
        '''
        Returns the appropriate serializer class based on the HTTP method
        '''

        if self.request.method in SAFE_METHODS:
            return PromptGroupReadSerializer
        else:
            return PromptGroupWriteSerializer

    def get_queryset(self):
        '''
        Retrieves the queryset for the view, applying additional filtering
        based on the action being performed.
        '''

        queryset = super().get_queryset()

        if self.action == 'list':
            perm = perms.PromptGroupPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def perform_create(self, serializer):
        '''
        Saves a new PromptGroup instance with additional fields:
        '''

        serializer.save(
            owner=self.request.user,
            team=self.request.iam_context['team'],
        )
