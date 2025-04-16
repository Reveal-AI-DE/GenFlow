# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import shutil
from os import path as osp
from typing import cast

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from genflow.apps.core.mixin import EntityGroupViewSetMixin
from genflow.apps.prompt import permissions as perms
from genflow.apps.prompt.models import Prompt
from genflow.apps.prompt.serializers import PromptReadSerializer, PromptWriteSerializer
from genflow.apps.team.middleware import HttpRequestWithIamContext


@extend_schema(tags=["prompt-groups"])
class PromptGroupViewSet(EntityGroupViewSetMixin):
    """
    Provides CRUD operations for the EntityGroup model associated with prompts.
    """

    group_entity_type = Prompt.__name__.lower()

    def get_queryset(self):
        """
        Retrieves the queryset for the view, applying additional filtering
        based on the action being performed.
        """
        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.PromptGroupPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset


@extend_schema(tags=["prompts"])
@extend_schema_view(
    list=extend_schema(
        summary="List prompts",
        description="List all prompts",
        responses={
            "200": PromptReadSerializer(many=True),
        },
    ),
    create=extend_schema(
        summary="Create a prompt",
        description="Create a new prompt",
        request=PromptWriteSerializer,
        responses={
            "201": PromptReadSerializer,
        },
    ),
    retrieve=extend_schema(
        summary="Get prompt details",
        description="Get details of a prompt",
        responses={
            "200": PromptReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Update a prompt",
        description="Update an existing prompt",
        request=PromptWriteSerializer,
        responses={
            "200": PromptReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete a prompt",
        description="Delete an existing prompt",
        responses={
            "204": OpenApiResponse(description="The prompt has been deleted"),
        },
    ),
    upload_avatar=extend_schema(
        summary="Upload a prompt avatar",
        description="Upload a new avatar image for the prompt",
        responses={
            "200": PromptReadSerializer,
        },
    ),
)
class PromptViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations and additional functionality
    for managing Prompt objects..
    """

    queryset = Prompt.objects.all().order_by("name")
    search_fields = ["name", "description"]
    filterset_fields = ["group__id", "type", "status", "is_pinned"]
    ordering_fields = ["name", "type", "status", "group__name"]
    iam_team_field = "team"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """

        if self.request.method in SAFE_METHODS:
            return PromptReadSerializer
        else:
            return PromptWriteSerializer

    def get_queryset(self):
        """
        Returns the queryset for the view. Applies additional filtering for the 'list' action
            based on permissions.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.PromptPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def perform_create(self, serializer):
        """
        Saves a new Prompt instance, associating it with the current user and team.
        """

        request = cast(HttpRequestWithIamContext, self.request)
        serializer.save(
            owner=self.request.user,
            team=request.iam_context.team,
        )

    def perform_destroy(self, instance: Prompt):
        """
        Deletes a Prompt instance and removes its associated media directory if it exists.
        """

        if osp.exists(instance.media_dir()):
            shutil.rmtree(instance.media_dir())
        return super().perform_destroy(instance)

    @action(detail=True, methods=["post"])
    def upload_avatar(self, request, pk=None):
        """
        A custom action to upload an avatar for a specific Prompt instance.
        """

        prompt: Prompt = self.get_object()
        prompt.avatar = request.FILES.get("avatar", None)
        prompt.save()
        return Response(status=status.HTTP_200_OK)
