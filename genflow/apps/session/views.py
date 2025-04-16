# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import shutil
from os import path as osp
from typing import cast

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from genflow.apps.prompt.models import Prompt
from genflow.apps.session import permissions as perms
from genflow.apps.session.models import Session, SessionMessage
from genflow.apps.session.serializers import (
    SessionMessageReadSerializer,
    SessionReadSerializer,
    SessionWriteSerializer,
)
from genflow.apps.team.middleware import HttpRequestWithIamContext


@extend_schema(tags=["sessions"])
@extend_schema_view(
    list=extend_schema(
        summary="List sessions",
        description="List all sessions that the user has access to.",
        responses={
            200: SessionReadSerializer(many=True),
        },
    ),
    create=extend_schema(
        summary="Create a session",
        description="Create a new session with the given data.",
        parameters=[
            OpenApiParameter(
                "testing",
                description="Whether the created session is a prompt test session.",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.BOOL,
                required=False,
            ),
        ],
        request=SessionWriteSerializer,
        responses={
            201: SessionReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Update a session",
        description="Update the session with the given data.",
        request=SessionWriteSerializer,
        responses={
            200: SessionReadSerializer,
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a session",
        description="Retrieve the session with the given ID.",
        responses={
            200: SessionReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete a session",
        description="Delete the session with the given ID.",
        responses={
            204: OpenApiResponse(description="The session has been deleted"),
        },
    ),
)
class SessionViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations and additional functionality
    for managing Session objects.
    """

    queryset = Session.objects.all().order_by("created_date")
    iam_team_field = "team"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """

        if self.request.method in SAFE_METHODS:
            return SessionReadSerializer
        else:
            return SessionWriteSerializer

    def get_queryset(self):
        """
        Returns the queryset for the view. Applies additional filtering for the 'list' action
            based on permissions.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.SessionPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_session = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # It is a prompt test session
        testing = request.query_params.get("testing", False)
        db_prompt: Prompt = db_session.related_prompt
        if testing and db_prompt is not None:
            db_prompt.related_test_session = db_session.id
            db_prompt.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer) -> Session:
        """
        Saves a new Session instance, associating it with the current user and team.
        """
        request = cast(HttpRequestWithIamContext, self.request)
        return serializer.save(
            owner=self.request.user,
            team=request.iam_context.team,
        )

    def perform_destroy(self, instance: Session):
        """
        Deletes a Session instance and removes its associated directory if it exists.
        """

        if osp.exists(instance.dirname):
            shutil.rmtree(instance.dirname)
        return super().perform_destroy(instance)


@extend_schema(tags=["messages"])
@extend_schema_view(
    list=extend_schema(
        summary="List messages",
        description="List all messages that belong to a session.",
        parameters=[
            OpenApiParameter(
                "session",
                description="The ID of the session to filter messages by.",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                required=True,
            ),
        ],
        responses={
            200: SessionMessageReadSerializer(many=True),
        },
    ),
)
class SessionMessageViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
):
    """
    Provides CRUD operations and additional functionality
    for managing SessionMessage objects.
    """

    queryset = SessionMessage.objects.all().order_by("created_date")
    filterset_fields = ["session"]
    iam_team_field = "team"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """

        if self.request.method in SAFE_METHODS:
            return SessionMessageReadSerializer

    def get_queryset(self):
        """
        Returns the queryset for the view. Applies additional filtering for the 'list' action
            based on permissions.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.SessionMessagePermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        session = request.query_params.get("session", None)
        if not session:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data="session ID is required to list messages"
            )
        return super().list(request, *args, **kwargs)
