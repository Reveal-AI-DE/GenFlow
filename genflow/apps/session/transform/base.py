# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional

from pydantic import BaseModel

from genflow.apps.ai.base.entities.model import PropertyKey
from genflow.apps.ai.llm.messages import AssistantMessage, Message, UserMessage
from genflow.apps.core.config.llm_model_bundle import LLMModelBundle
from genflow.apps.prompt.models import PromptType
from genflow.apps.session.models import Session, SessionMessage


class PromptTemplateEntity(BaseModel):
    """
    Prompt Template Entity.
    """

    prompt_type: PromptType
    simple_prompt_template: Optional[str] = None


class BasePromptTransform:
    """
    Responsible for managing and transforming chat session messages
    to ensure they fit within the constraints of a language model's token limit. It interacts with
    a session object and a LLM model bundle to process and retrieve chat histories.
    """

    def __init__(self, db_session: Session, llm_model_bundle: LLMModelBundle):
        """
        Initializes the BasePromptTransform with a session and model bundle.
        """

        self.db_session = db_session
        self.llm_model_bundle = llm_model_bundle

    def _append_chat_histories(
        self,
        messages: list[Message],
    ) -> list[Message]:
        """
        Appends historical chat messages to the provided list of messages, ensuring
            the total token count remains within the model's constraints.
        """

        remaining_token = self._calculate_remaining_token(messages)

        histories = self._get_message_history(remaining_token, None)
        messages.extend(histories)

        return messages

    def _calculate_remaining_token(self, messages: list[Message]) -> int:
        """
        Calculates the remaining token capacity available for additional messages
            based on the model's context size and current message tokens.
        """

        rest_tokens = 2000

        model_context_tokens = self.llm_model_bundle.model_schema.properties.get(
            PropertyKey.CONTEXT_SIZE
        )
        if model_context_tokens:
            curr_message_tokens = self.llm_model_bundle.get_tokens_count(messages)

            max_tokens = 0
            for parameter_config in self.llm_model_bundle.model_schema.parameter_configs:
                if parameter_config.name == "max_tokens" or (
                    parameter_config.use_template and parameter_config.use_template == "max_tokens"
                ):
                    max_tokens = (
                        self.llm_model_bundle.parameters.get(parameter_config.name)
                        or self.llm_model_bundle.parameters.get(parameter_config.use_template)
                    ) or 0

            rest_tokens = model_context_tokens - max_tokens - curr_message_tokens
            rest_tokens = max(rest_tokens, 0)

        return rest_tokens

    def _get_message_history(
        self, max_token_limit: int = 2000, message_limit: Optional[int] = None
    ) -> list[Message]:
        """
        Retrieves historical chat messages from the session database, prunes them
            if they exceed the maximum token limit, and returns the processed messages.
        """

        query_set = SessionMessage.objects.filter(session=self.db_session).order_by("-created_date")

        if message_limit and message_limit > 0:
            message_limit = min(message_limit, 500)
        else:
            message_limit = 500

        history = query_set.all()[:message_limit]

        messages = []
        for db_session_message in history:
            messages.append(UserMessage(content=db_session_message.query))
            messages.append(AssistantMessage(content=db_session_message.answer))

        if not messages:
            return []

        # prune the chat message if it exceeds the max token limit
        curr_message_tokens = self.llm_model_bundle.get_tokens_count(messages)

        if curr_message_tokens > max_token_limit:
            pruned_memory = []
            while curr_message_tokens > max_token_limit and len(messages) > 1:
                pruned_memory.append(messages.pop(0))
                curr_message_tokens = self.llm_model_bundle.get_tokens_count(messages)

        return messages
