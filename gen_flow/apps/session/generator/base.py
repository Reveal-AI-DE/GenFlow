# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Callable, Optional, Union, Generator

from gen_flow.apps.ai.base.entities.model import PropertyKey
from gen_flow.apps.ai.llm.messages import Message, AssistantMessage
from gen_flow.apps.ai.llm.entities import Result, Usage
from gen_flow.apps.core.config.llm_model_bundle import LLMModelBundle
from gen_flow.apps.prompt.models import PromptType
from gen_flow.apps.session.models import Session
from gen_flow.apps.session.transform.base import PromptTemplateEntity
from gen_flow.apps.session.transform.simple import SimplePromptTransform

class BaseGenerator:
    '''
    Responsible for managing and generating prompts, calculating token limits,
    and handling model responses in the context of a session and a language model bundle.
    '''

    def __init__(
            self,
            db_session: Session,
            llm_model_bundle: LLMModelBundle
    ) -> None:
        '''
        Initializes the BaseGenerator with a session and a model bundle.
        '''

        self.db_session = db_session
        self.llm_model_bundle = llm_model_bundle

    def get_precalculate_rest_tokens(
        self,
        prompt_template_entity: PromptTemplateEntity,
        files: Optional[str] = None,
        query: Optional[str] = None,
    ) -> int:
        '''
        Calculates the remaining tokens available for the model after accounting for the prompt
            and maximum token limits. Raises an exception if the prompt or query exceeds the token limit
        '''

        model_context_tokens = self.llm_model_bundle.model_schema.properties.get(PropertyKey.CONTEXT_SIZE)

        max_tokens = 0
        for parameter_config in self.llm_model_bundle.model_schema.parameter_configs:
            if parameter_config.name == 'max_tokens' or (
                parameter_config.use_template and parameter_config.use_template == 'max_tokens'
            ):
                max_tokens = (
                    self.llm_model_bundle.parameters.get(parameter_config.name)
                    or self.llm_model_bundle.parameters.get(parameter_config.use_template)
                ) or 0

        if model_context_tokens is None:
            return -1

        if max_tokens is None:
            max_tokens = 0

        # get messages without memory and context
        input_messages, _ = self.organize_input_messages(
            prompt_template_entity=prompt_template_entity,
            files=files,
            query=query,
            memory=False,
        )

        prompt_tokens = self.llm_model_bundle.get_tokens_count(input_messages)

        remaining_tokens = model_context_tokens - max_tokens - prompt_tokens
        if remaining_tokens < 0:
            raise Exception(
                'Query or prefix prompt is too long, you can reduce the prefix prompt, '
                'or shrink the max token, or switch to a llm with a larger token limit size.'
            )

        return remaining_tokens

    def recalculate_max_tokens(
        self, input_messages: list[Message]
    ):
        '''
        Recalculates the maximum tokens allowed if the sum of prompt tokens and max tokens exceeds
            the model's token limit. Updates the model parameters accordingly.'
        '''

        # recalculate max_tokens if sum(prompt_token + max_tokens) over model token limit
        model_context_tokens = self.llm_model_bundle.model_schema.properties.get(PropertyKey.CONTEXT_SIZE)

        max_tokens = 0
        for parameter_config in self.llm_model_bundle.model_schema.parameter_configs:
            if parameter_config.name == 'max_tokens' or (
                parameter_config.use_template and parameter_config.use_template == 'max_tokens'
            ):
                max_tokens = (
                    self.llm_model_bundle.parameters.get(parameter_config.name)
                    or self.llm_model_bundle.parameters.get(parameter_config.use_template)
                ) or 0

        if model_context_tokens is None:
            return -1

        if max_tokens is None:
            max_tokens = 0

        prompt_tokens = self.llm_model_bundle.get_tokens_count(input_messages)

        if prompt_tokens + max_tokens > model_context_tokens:
            max_tokens = max(model_context_tokens - prompt_tokens, 16)

            for parameter_config in self.llm_model_bundle.model_schema.parameter_configs:
                if parameter_config.name == 'max_tokens' or (
                    parameter_config.use_template and parameter_config.use_template == 'max_tokens'
                ):
                    self.llm_model_bundle.parameters[parameter_config.name] = max_tokens

    def organize_input_messages(
        self,
        prompt_template_entity: PromptTemplateEntity,
        files: Optional[str] = None,
        query: Optional[str] = None,
        context: Optional[str] = None,
        memory: bool = False,
    ) -> tuple[list[Message], Optional[list[str]]]:
        '''
        Organizes input messages based on the provided prompt template, files, query,
            context, and memory. Returns the generated input messages and stop tokens.
        '''

        if context is not None and isinstance(context, list):
            context = ' '.join([item.text for item in context])

        if prompt_template_entity is None or prompt_template_entity.prompt_type == PromptType.SIMPLE:
            prompt_transform = SimplePromptTransform(
                db_session=self.db_session,
                llm_model_bundle=self.llm_model_bundle,
            )
            input_messages, stop = prompt_transform.get_prompt(
                prompt_template_entity=prompt_template_entity,
                files=files or "",
                query=query or "",
                context=context or "",
                memory=memory,
            )
        else:
            raise NotImplementedError('Advanced prompt template is not implemented yet.')

        return input_messages, stop

    def _handle_model_response(
        self,
        response: Union[Result, Generator],
        callback: Callable,
        stream: bool,
    ) -> Result:
        '''
        Handles the model response. If streaming is enabled, processes the response in chunks;
            otherwise, returns the full response.

        '''

        if not stream:
            return response
        else:
            return self._handle_model_response_stream(response=response, callback=callback)

    def _handle_model_response_stream(
        self,
        response: Union[Result, Generator],
        callback: Callable
    ) -> Result:
        '''
        Processes the model response in a streaming manner, invoking the callback for each chunk
            of the response. Returns the final result containing the model, messages, and usage details.
        '''

        model = None
        messages = []
        text = ''
        usage = None
        for result in response:
            callback(chunk=result.delta.message.content)

            text += result.delta.message.content

            if not model:
                model = result.model

            if not messages:
                messages = result.prompt_messages

            if result.delta.usage:
                usage = result.delta.usage
        if not usage:
            usage = Usage.empty_usage()

        return Result(
            model=model,
            messages=messages,
            message=AssistantMessage(content=text),
            usage=usage
        )
