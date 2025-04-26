# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.permissions import SAFE_METHODS

from genflow.apps.common.file_utils import get_files
from genflow.apps.assistant import permissions as perms
from genflow.apps.assistant.models import Assistant
from genflow.apps.assistant.serializers import AssistantReadSerializer, AssistantWriteSerializer
from genflow.apps.core.mixin import EntityGroupViewSetMixin, FileManagementMixin
from genflow.apps.core.serializers import FileEntitySerializer
from genflow.apps.core.views import EntityBaseViewSet


@extend_schema(tags=["assistant-groups"])
class AssistantGroupViewSet(EntityGroupViewSetMixin):
    """
    Provides CRUD operations for the EntityGroup model associated with assistants.
    """

    group_entity_type = Assistant.__name__.lower()

    def get_queryset(self):
        """
        Retrieves the queryset for the view, applying additional filtering
        based on the action being performed.
        """
        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.AssistantGroupPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset


@extend_schema(tags=["assistants"])
@extend_schema_view(
    list=extend_schema(
        summary="List assistants",
        description="List all assistants",
        responses={
            "200": AssistantReadSerializer(many=True),
        },
    ),
    create=extend_schema(
        summary="Create a assistant",
        description="Create a new assistant",
        request=AssistantWriteSerializer,
        responses={
            "201": AssistantReadSerializer,
        },
    ),
    retrieve=extend_schema(
        summary="Get assistant details",
        description="Get details of a assistant",
        responses={
            "200": AssistantReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Update a assistant",
        description="Update an existing assistant",
        request=AssistantWriteSerializer,
        responses={
            "200": AssistantReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete a assistant",
        description="Delete an existing assistant",
        responses={
            "204": OpenApiResponse(description="The assistant has been deleted"),
        },
    ),
    upload_avatar=extend_schema(
        summary="Upload a assistant avatar",
        description="Upload a new avatar image for the assistant",
        responses={
            "200": AssistantReadSerializer,
        },
    ),
    list_files=extend_schema(
        summary="List files",
        description="List all files associated with the entity",
        responses={
            200: FileEntitySerializer(many=True),
        },
    ),
    upload_file=extend_schema(
        summary="Upload a file",
        description="Upload a new file and associate it with the entity",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "The file to upload",
                    },
                },
                "required": ["file"],
            }
        },
        responses={201: FileEntitySerializer()},
    ),
    delete_file=extend_schema(
        summary="delete file",
        description="Delete a specific file associated with the entity",
        responses={204: OpenApiResponse(description="File was removed")},
    ),
)
class AssistantsViewSet(EntityBaseViewSet, FileManagementMixin):
    """
    Provides CRUD operations and additional functionality
    for managing Prompt objects..
    """

    queryset = Assistant.objects.all().order_by("name")
    filterset_fields = EntityBaseViewSet.filterset_fields + ["prompt_type", "assistant_status"]
    ordering_fields = EntityBaseViewSet.ordering_fields + ["prompt_type", "assistant_status"]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """

        if self.request.method in SAFE_METHODS:
            return AssistantReadSerializer
        else:
            return AssistantWriteSerializer

    def get_queryset(self):
        """
        Returns the queryset for the view. Applies additional filtering for the 'list' action
            based on permissions.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.AssistantPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def get_file_limit_key(self) -> str:
        """
        Gets the key for the file limit.
        """

        return "MAX_FILES_PER_ASSISTANT"
