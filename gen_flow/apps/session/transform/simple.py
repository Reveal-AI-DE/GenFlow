# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import List, Optional

from gen_flow.apps.ai.llm.messages import Message, SystemMessage, UserMessage
from gen_flow.apps.core.config.llm_model_bundle import LLMModelBundle
from gen_flow.apps.session.models import Session
from gen_flow.apps.session.transform.base import BasePromptTransform, PromptTemplateEntity


class SimplePromptTransform(BasePromptTransform):
    """
    SimplePromptTransform is a class that extends the BasePromptTransform to handle
    the transformation of prompts for a session using a LLM model bundle. It
    constructs chat model messages based on the provided prompt template, files,
    query, context, and memory.
    """

    def __init__(self, db_session: Session, llm_model_bundle: LLMModelBundle):
        """
        Initializes the SimplePromptTransform with a session and a language
            model bundle.
        """

        super().__init__(db_session, llm_model_bundle)

    # pylint: disable=too-many-positional-arguments
    def get_prompt(
        self,
        prompt_template_entity: PromptTemplateEntity,
        files: str,
        query: str,
        context: Optional[str],
        memory: bool,
    ) -> tuple[List[Message], Optional[List[str]]]:
        """
        Generates a list of chat model messages and optionally a list of
            additional strings based on the provided parameters.
        """

        return self._get_chat_model_messages(
            pre_prompt=(
                prompt_template_entity.simple_prompt_template if prompt_template_entity else None
            ),
            files=files,
            query=query,
            context=context,
            memory=memory,
        )

    # pylint: disable=too-many-positional-arguments
    def _get_chat_model_messages(
        self,
        pre_prompt: str,
        files: str,
        query: Optional[str],
        context: Optional[str],
        memory: bool,
    ) -> tuple[list[Message], Optional[list[str]]]:
        """
        Constructs the chat model messages by combining the pre-prompt,
            context, query, and memory. Appends user messages based on the query
            and files.
        """

        messages = []
        prompt = pre_prompt

        if context is not None:
            prompt = f"{prompt}\nCONTEXT:{context}\n"
        if prompt and query:
            messages.append(SystemMessage(content=prompt))

        if memory:
            messages = self._append_chat_histories(
                messages=messages,
            )

        if query:
            messages.append(self.get_last_user_message(query, files))
        else:
            messages.append(self.get_last_user_message(prompt, files))

        return messages, None

    def get_last_user_message(
        self,
        prompt: str,
        files: str,
    ) -> UserMessage:
        """
        Creates and returns the last user message by combining the prompt and
            files into a single message content.
        """

        message_contents = f"{prompt}\n{files}"
        message = UserMessage(content=message_contents)

        return message
