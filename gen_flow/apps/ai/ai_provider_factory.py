# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional
from collections.abc import Sequence

from gen_flow.apps.ai.base.entities.provider import AIProviderEntity
from gen_flow.apps.ai.base.ai_provider import AIProvider
from gen_flow.apps.ai.providers.registry import AI_PROVIDERS, AIProviderExtension

class AIProviderFactory:
    '''
    Manages AI providers and their models.
    '''

    schemas: Optional[Sequence[AIProviderEntity]] = None

    def __init__(self) -> None:
        '''
        Initializes the factory and retrieves AI providers
        '''

        self.schemas = self.get_ai_provider_schemas()

    def get_ai_provider_schemas(self) -> Sequence[AIProviderEntity]:
        '''
        Retrieves and returns a list of AI provider schemas with their supported models.
        '''

        if self.schemas is not None:
            return self.schemas

        ai_provider_extensions = self._get_ai_provider_map()

        ai_provider_schemas = []
        for ai_provider_extension in ai_provider_extensions.values():
            # retrieve the provider schema
            ai_provider_instance = ai_provider_extension.ai_provider_instance
            ai_provider_schema = ai_provider_instance.get_schema()

            # retrieve the models for the provider
            # based on supported model types
            for model_type in ai_provider_schema.supported_model_types:
                models = ai_provider_instance.get_models(model_type=model_type.value)
                if models:
                    ai_provider_schema.models.extend(models)

            ai_provider_schemas.append(ai_provider_schema)

        # cache the ai_providers
        self.schemas = ai_provider_schemas

        return ai_provider_schemas

    def get_ai_provider_instance(self, provider: str) -> AIProvider:
        '''
        Retrieves and returns the instance of the specified ai provider.
        '''

        # scan all providers
        ai_provider_extensions = self._get_ai_provider_map()

        # get the provider extension
        ai_provider_extension = ai_provider_extensions.get(provider)
        if not ai_provider_extension:
            raise Exception(f'Invalid AI provider: {provider}')

        # get the provider instance
        ai_provider_instance = ai_provider_extension.ai_provider_instance

        return ai_provider_instance

    def validate_credentials(self, provider: str, credentials: dict) -> dict:
        '''
        Validates the credentials for a given ai provider and returns the filtered credentials.
        '''

        ai_provider_instance = self.get_ai_provider_instance(provider)
        ai_provider_schema = ai_provider_instance.get_schema()

        if not ai_provider_schema.credential_form:
            raise ValueError(f'AI Provider {provider} does not have credential_form')

        # validate credential form
        filtered_credentials = ai_provider_schema.validate_credential_form(credentials)

        # validate the credentials, raise exception if validation failed
        ai_provider_instance.validate_credentials(filtered_credentials)

        return filtered_credentials

    def _get_ai_provider_map(self) -> dict[str, AIProviderExtension]:
        '''
        Retrieves and returns the map of AI provider extensions.
        '''

        return AI_PROVIDERS
