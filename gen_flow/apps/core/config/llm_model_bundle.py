# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Any, cast, Optional, Generator, Union

from pydantic import ConfigDict

from gen_flow.apps.ai.llm.llm_model_collection import LLMModelCollection
from gen_flow.apps.ai.llm.messages import Message
from gen_flow.apps.ai.llm.entities import Result
from gen_flow.apps.core.config.entities import ModelBundle, ModelCollectionBundle


class LLMModelBundle(ModelBundle):
    '''
    Represents a model bundle for LLM.
    '''

    model_collection_instance: LLMModelCollection

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        if not isinstance(self.model_collection_instance, LLMModelCollection):
            raise Exception('Model collection instance is not LLMModelCollection')

        self.model_collection_instance = cast(LLMModelCollection, self.model_collection_instance)


    def call(
        self,
        messages: list[Message],
        parameters: Optional[dict] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[Result, Generator]:
        '''
        Call large language model
        '''

        return self.model_collection_instance.call(
            model=self.model_schema.id,
            credentials=self.credentials,
            messages=messages,
            parameters=parameters,
            stop=stop,
            stream=stream,
            user=user,
        )


    def get_tokens_count(
        self,
        messages: list[Message]
    ) -> int:
        '''
        Get number of tokens for llm
        '''

        return self.model_collection_instance.get_tokens_count(
            model=self.model_schema.id,
            messages=messages,
        )

    @staticmethod
    def _fetch_credentials_from_bundle(model: str, model_collection_bundle: ModelCollectionBundle) -> dict:
        '''
        Fetch credentials from model collection bundle
        '''

        configuration = model_collection_bundle.configuration
        credentials = configuration.user_configuration.provider.credentials

        if credentials is None:
            raise Exception(f'Model {model} credentials is not initialized.')

        return credentials
