# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from collections.abc import Mapping

from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.base.ai_provider import AIProvider
from gen_flow.apps.ai.providers.registry import register_ai_provider

@register_ai_provider(name='openai')
class OpenAIProvider(AIProvider):
    '''
    A provider class for interacting with OpenAI's API, inheriting from the base AIProvider class.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Initializes the OpenAIProvider instance by calling the parent class constructor.
        '''

        super().__init__(*args, **kwargs)

    def validate_credentials(self, credentials: Mapping) -> None:
        '''
        Validates the AI provided credentials by using the model collection instance for the LLM model type.
        Raises an exception if the validation fails.
        '''

        try:
            model_collection_instance = self.get_model_collection_instance(ModelType.LLM)

            model_collection_instance.validate_credentials(model='gpt-3.5-turbo', credentials=credentials)
        except Exception as ex:
            # ToDo: logging
            raise ex

import gen_flow.apps.ai.providers.openai.llm # noqa
