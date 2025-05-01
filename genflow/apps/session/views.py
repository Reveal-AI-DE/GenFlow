# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import shutil
from os import path as osp
from typing import Generator, Union, cast

from django.http import StreamingHttpResponse
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from genflow.apps.ai.llm.entities import Result
from genflow.apps.core.mixin import FileManagementMixin
from genflow.apps.core.models import Provider
from genflow.apps.core.serializers import FileEntitySerializer
from genflow.apps.prompt.models import Prompt
from genflow.apps.session import permissions as perms
from genflow.apps.session.generator.chat import ChatGenerator
from genflow.apps.session.generator.entities import ChatResponse, ChatResponseType, GenerateRequest
from genflow.apps.session.models import Session, SessionMessage
from genflow.apps.session.serializers import (
    GenerateRequestSerializer,
    SessionMessageReadSerializer,
    SessionMessageWriteSerializer,
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
    generate=extend_schema(
        summary="Generate a message",
        description="Generate a message from the LLM AI model.",
        request=GenerateRequestSerializer,
        responses={
            200: ChatResponse,
        },
    ),
)
class SessionViewSet(viewsets.ModelViewSet, FileManagementMixin):
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
        elif self.action == "generate":
            return GenerateRequestSerializer
        else:
            return SessionWriteSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """

        context = super().get_serializer_context()
        if self.action == "generate" and hasattr(self, "message_generator"):
            context["llm_model_bundle"] = self.message_generator.generate_entity.llm_model_bundle
            return context
        else:
            return context

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

    def get_file_limit_key(self) -> str:
        """
        Gets the key for the file limit.
        """

        return "MAX_FILES_PER_SESSION"

    @action(detail=True, methods=["post"])
    def generate(self, request, *args, **kwargs):
        try:
            request = cast(HttpRequestWithIamContext, request)
            db_session = self.get_object()
            # initialize provider queryset and generator
            queryset = Provider.objects.filter(team=request.iam_context.team)
            self.message_generator = ChatGenerator(queryset=queryset, db_session=db_session)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return self.perform_generate(request, serializer)
        except Exception as e:
            # Handle any exceptions that occur during the generation process
            message = ChatResponse(
                type=ChatResponseType.ERROR,
                data={
                    "message": str(e),
                },
            )
            return Response(
                message.model_dump(mode="json"),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def handle_final_result(
        self, generate_request: GenerateRequest, model_config: dict, result: Result
    ) -> SessionMessageWriteSerializer:
        # create a SessionMessage instance
        data = {
            "query": generate_request.query,
            "answer": result.message.content,
            "usage": result.usage.model_dump_json(),
            "session_id": self.message_generator.db_session.id,
        }
        if model_config is not None:
            data["related_model"] = model_config

        message_serializer = SessionMessageWriteSerializer(
            data=data,
            context=self.get_serializer_context(),
        )
        message_serializer.is_valid(raise_exception=True)
        message_serializer.save(
            owner=self.request.user,
            team=self.request.iam_context.team,
        )
        return message_serializer

    def handle_stream(self, generate_request: GenerateRequest, model_config: dict) -> Generator:
        """
        Handles the streaming of the generation process.
        """
        response: Union[Result, Generator] = self.message_generator.generate(
            generate_request=generate_request
        )

        for chunk in response:
            message = None
            if isinstance(chunk, str):
                message = ChatResponse(
                    type=ChatResponseType.CHUNK,
                    data=chunk,
                )
            elif isinstance(chunk, Result):
                result = chunk
                message_serializer = self.handle_final_result(
                    generate_request=generate_request,
                    model_config=model_config,
                    result=result,
                )
                message = ChatResponse(
                    type=ChatResponseType.MESSAGE,
                    data=message_serializer.data,
                )
            yield f"{message.model_dump(mode="json")}\n\n"

    def perform_generate(
        self, request: HttpRequestWithIamContext, serializer: GenerateRequestSerializer
    ) -> SessionMessage:
        """
        generate a message from the LLM AI model.
        """

        related_model_data = serializer.validated_data.pop("related_model", None)
        generate_request = serializer.save(user=request.user)
        if generate_request.stream:
            return StreamingHttpResponse(
                self.handle_stream(generate_request, model_config=related_model_data)
            )
        else:
            result: Result = self.message_generator.generate(generate_request=generate_request)
            message_serializer = self.handle_final_result(
                generate_request=generate_request,
                model_config=related_model_data,
                result=result,
            )
            message = ChatResponse(
                type=ChatResponseType.MESSAGE,
                data=message_serializer.data,
            )
            return Response(
                message.model_dump(mode="json"),
                status=status.HTTP_200_OK,
            )


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
        else:
            return GenerateRequestSerializer

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
