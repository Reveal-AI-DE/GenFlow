# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp
from typing import cast

from drf_spectacular.utils import (
    OpenApiResponse, extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiTypes
)
from rest_framework import viewsets, status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from genflow.apps.common.storage import fs
from genflow.apps.common.file_utils import get_files
from genflow.apps.core.models import EntityGroup
from genflow.apps.core.serializers import EntityGroupReadSerializer, EntityGroupWriteSerializer, FileEntitySerializer
from genflow.apps.team.middleware import HttpRequestWithIamContext


@extend_schema_view(
    list=extend_schema(
        summary="List groups",
        description="List all groups",
        responses={
            "200": EntityGroupReadSerializer(many=True),
        },
    ),
    create=extend_schema(
        summary="Create a group",
        description="Create a new group",
        request=EntityGroupWriteSerializer,
        responses={
            "201": EntityGroupReadSerializer,
        },
    ),
    retrieve=extend_schema(
        summary="Get group details",
        description="Get details of a group",
        responses={
            "200": EntityGroupReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Update a group",
        description="Update an existing group",
        request=EntityGroupWriteSerializer,
        responses={
            "200": EntityGroupReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete a group",
        description="Delete an existing group",
        responses={
            "204": OpenApiResponse(description="The group has been deleted"),
        },
    ),
)
class EntityGroupViewSetMixin(viewsets.ModelViewSet):
    """
    A mixin that filters EntityGroup by entity_type based on the model class name.
    Assumes `queryset` and `serializer_class` are defined.
    """

    queryset = EntityGroup.objects.all().order_by("name")
    iam_team_field = "team"
    group_entity_type = None

    def get_entity_type(self):
        # Default to model name if not overridden
        return self.group_entity_type or self.basename.replace("-group", "")

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method
        """

        if self.request.method in SAFE_METHODS:
            return EntityGroupReadSerializer
        else:
            return EntityGroupWriteSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for the view, applying additional filtering
        based on the action being performed.
        """
        queryset = super().get_queryset()

        # Apply filtering based on entity_type
        entity_type = self.get_entity_type()
        queryset = queryset.filter(entity_type=entity_type)

        return queryset

    def perform_create(self, serializer):
        """
        Saves a new EntityGroup instance with additional fields:
        """

        request = cast(HttpRequestWithIamContext, self.request)
        serializer.save(
            entity_type=self.get_entity_type(),
            owner=self.request.user,
            team=request.iam_context.team,
        )


class FileManagementMixin:
    """
    Mixin to add file management functionality to a viewset.
    Provides endpoints for listing, uploading, and deleting files.
    """

    @action(detail=True, methods=["get"], url_path="files")
    def list_files(self, request, pk=None):
        """
        Lists all files associated with the entity.
        """

        instance = self.get_object()
        if not hasattr(instance, "dirname"):
           return Response(status=status.HTTP_400_BAD_REQUEST)

        files = get_files(instance.dirname)
        serializer = FileEntitySerializer(files, many=True)
        return Response(data={'results': serializer.data, 'count': len(serializer.data)})

    @action(detail=True, methods=["post"])
    def upload_file(self, request, pk=None):
        """
        Uploads a new file and associates it with the entity.
        """

        instance = self.get_object()
        if not hasattr(instance, "dirname"):
           return Response(status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES.get("file", None)
        serializer = FileEntitySerializer(data={
            "dirname": instance.dirname,
            "uploaded_file": uploaded_file
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"], url_path="files/(?P<filename>[^/]+)")
    def delete_file(self, request, pk=None, filename=None):
        """
        Deletes a specific file associated with the entity.
        """

        instance = self.get_object()
        if not hasattr(instance, "dirname"):
           return Response(status=status.HTTP_400_BAD_REQUEST)

        if not filename:
            return Response({"detail": "Filename is required."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = osp.join(instance.dirname, filename)
        if osp.exists(file_path):
            fs.delete(file_path)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
