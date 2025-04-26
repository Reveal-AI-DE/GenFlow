# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import asyncio

from channels.db import database_sync_to_async

from genflow.apps.ai.llm.entities import Result
from genflow.apps.core.models import Provider
from genflow.apps.restriction.models import Limit
from genflow.apps.session.generator.chat import ChatGenerator
from genflow.apps.session.generator.entities import GenerateRequest
from genflow.apps.session.models import Session, SessionMessage
from genflow.apps.session.serializers import GenerateRequestSerializer, SessionMessageReadSerializer
from genflow.apps.websocket.auth_middleware import WebSocketRequest
from genflow.apps.websocket.consumer import exception
from genflow.apps.websocket.consumer.base import BaseConsumer
from genflow.apps.websocket.messages import ChatResponse, ChatResponseType


class ChatGenerateConsumer(BaseConsumer):
    """
    Handles chat generation requests.
    It validates user permissions, processes incoming requests, and sends responses
    back to the client.
    """

    @database_sync_to_async
    def check_permission(self):
        """
        Validates if the user has the necessary permissions to access the session.
            Ensures the user belongs to a team and the team matches the session's team.
            Initializes the ChatGenerator instance for processing requests.
        """

        try:
            request: WebSocketRequest = self.scope["request"]
            # check if team is provided
            team = request.iam_context.team
            if team is None:
                raise exception.BadRequestError("Team is not specified")

            # check if user is a team member is provided
            if request.iam_context.team_role is None:
                raise exception.ForbiddenError("User must be a member of a team")

            session_id = self.scope["url_route"]["kwargs"]["session_id"]
            db_session = Session.objects.get(pk=session_id)

            # check if user team is the session team
            if db_session.team != team:
                raise exception.ForbiddenError("You do not have permission to access this session")

            # check limit
            if self.check_limit(db_session):
                raise exception.ForbiddenError("User has reached the message limit")

            # initialize provider queryset
            queryset = Provider.objects.filter(team=team)

            self.generator = ChatGenerator(queryset=queryset, db_session=db_session)
        except Session.DoesNotExist:
            raise exception.NotFoundError("Session not found")
        except Exception as e:
            raise e

    def check_limit(self, db_session: Session) -> bool:
        """
        Checks if the user has reached their message limit.
        """

        try:
            global_limit = Limit.objects.get(key="MESSAGE", user=None, team=None)
            return bool(global_limit.value <= db_session.sessionmessage_set.count())
        except Limit.DoesNotExist:
            # If no limit is set globally, return False (not limited)
            return False

    def send_chunk(self, chunk: str = None):
        """
        Sends a chunk of data as a JSON response to the WebSocket client.
        """

        response = ChatResponse(type=ChatResponseType.CHUNK, data=chunk)
        asyncio.run(self.send_json(response.model_dump(mode="json")))

    async def receive_json(self, json_data, **kwargs):
        """
        Handles incoming JSON data from the WebSocket client. Validates the data,
            processes the request, and sends the appropriate response back to the client.
        """

        try:
            serializer = GenerateRequestSerializer(
                data=json_data,
                context={
                    "request": self.scope["request"],
                    "llm_model_bundle": self.generator.generate_entity.llm_model_bundle,
                },
            )
            # call model
            session_message = await self.handle_request(serializer)

            # construct response
            serializer = SessionMessageReadSerializer(instance=session_message)
            response = ChatResponse(type=ChatResponseType.MESSAGE, data=serializer.data)

            await self.send_json(response.model_dump(mode="json"))

        except Exception as e:
            response = ChatResponse(type=ChatResponseType.ERROR, data=str(e))
            await self.send_json(response.model_dump(mode="json"))

    @database_sync_to_async
    def handle_request(self, serializer: GenerateRequestSerializer) -> SessionMessage:
        """
        Processes the validated request data, generates a response using the ChatGenerator,
            updates the session model parameters, and creates a SessionMessage instance.
        """
        serializer.is_valid(raise_exception=True)

        related_model_data = serializer.validated_data.pop("related_model", None)

        generate_request = GenerateRequest(**serializer.validated_data)
        generate_request.user_id = str(self.scope["user"].id)
        generate_request.callback = self.send_chunk
        result: Result = self.generator.generate(generate_request=generate_request)

        # update model parameters
        db_session = self.generator.db_session
        if related_model_data is not None:
            db_session.related_model.config = related_model_data["config"]
            db_session.related_model.save()

        request: WebSocketRequest = self.scope["request"]
        session_message = SessionMessage.objects.create(
            query=generate_request.query,
            answer=result.message.content,
            usage=result.usage.model_dump_json(),
            session=db_session,
            owner=self.scope["user"],
            team=request.iam_context.team,
        )

        return session_message
