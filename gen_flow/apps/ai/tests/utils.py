# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
from os import path as osp
from typing import Optional, Union, Generator, Mapping

from django.conf import settings

from gen_flow.apps.ai.base.ai_provider import AIProvider
from gen_flow.apps.ai.base.model_collection import ModelCollection
from gen_flow.apps.ai.llm.llm_model_collection import LLMModelCollection
from gen_flow.apps.ai.llm.messages import Message, AssistantMessage
from gen_flow.apps.ai.llm.entities import Result

class DummyAIProvider(AIProvider):
    '''
    Dummy AI provider class.
    '''

    PROVIDER_FOLDER = 'dummy_provider'

    def validate_credentials(self, credentials: dict) -> None:
        '''
        Validate provider credentials
        '''
        pass

class DummyModelCollection(ModelCollection):
    '''
    Dummy Model Collection class.
    '''

    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        '''
        Validate model credentials
        '''
        pass

class DummyLLMModelCollection(LLMModelCollection):
    '''
    Dummy LLM Model Collection class.
    '''

    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        '''
        Validate model credentials
        '''
        pass

    RESPONSE = AssistantMessage(content='result')

    def get_tokens_count(
        self,
        model: str,
        credentials: dict,
        messages: list[Message],
    ) -> int:
        '''
        Gets the token counts for a given model and messages.
        '''
        tokens_count = 0
        for message in messages:
            if isinstance(message.content, list):
                for content in message.content:
                    tokens_count += len(content.data)
            else:
                tokens_count += len(message.content)
        return tokens_count

    def _call(
        self,
        model: str,
        credentials: dict,
        messages: list[Message],
        parameters: dict,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[Result, Generator]:
        '''
        Calls the model with the given parameters and messages.
        '''
        input_tokens = self.get_tokens_count(model, credentials, messages)
        output_tokens = self.get_tokens_count(model, credentials, [self.RESPONSE])
        usage = self._calculate_usage(model, input_tokens, output_tokens)
        return Result(model=model, messages=messages, message=self.RESPONSE, usage=usage)

def create_dummy_model_config():
    src_path = osp.join(osp.dirname(__file__), 'assets')
    dist_path = settings.MODEL_CONFIG_ROOT
    os.makedirs(dist_path, exist_ok=True)
    os.system(f'cp -r {src_path}/* {dist_path}')
