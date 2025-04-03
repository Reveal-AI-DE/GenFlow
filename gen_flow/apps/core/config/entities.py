# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, field_serializer

from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.base.entities.model import CommonModelEntity, ModelEntity
from gen_flow.apps.ai.base.entities.provider import CommonAIProviderEntity, AIProviderEntity
from gen_flow.apps.ai.base.ai_provider import AIProvider
from gen_flow.apps.ai.base.model_collection import ModelCollection
from gen_flow.apps.ai import ai_provider_factory


class UserModelConfiguration(BaseModel):
    '''
    Represents a model configuration provided by the user.
    '''

    model: str
    credentials: dict


class UserProviderConfiguration(BaseModel):
    '''
    Represents an AI provider configuration provided by the user.
    '''

    provider_id: str
    credentials: dict


class UserConfiguration(BaseModel):
    '''
    Represents configuration provided by the user for an AI provider and a list of its models.
    '''

    provider: Optional[UserProviderConfiguration] = None
    models: list[UserModelConfiguration] = []


class SystemConfiguration(BaseModel):
    '''
    Represents configuration provided by the system.
    '''

    provider: Optional[str] = None
    enabled: bool
    credentials: Optional[dict] = None


class ModelWithProviderEntity(CommonModelEntity):
    '''
    Extends CommonModelEntity to include a provider and an active status.
    '''

    active: bool
    provider: CommonAIProviderEntity


class AIProviderConfiguration(AIProviderEntity):
    '''
    Configuration entity for AI providers, inheriting from AIProviderEntity.
    '''

    user_configuration: Optional[UserConfiguration] = None
    system_configuration: Optional[SystemConfiguration] = None

    def __init__(self,
            ai_provider_entity: AIProviderEntity,
            user_configuration: Optional[UserConfiguration] = None,
            system_configuration: Optional[SystemConfiguration] = None,
        ) -> 'AIProviderConfiguration':
        '''
        Initializes an AIProviderConfiguration instance with the given parameters.
        '''

        super().__init__(
            id=ai_provider_entity.id,
            label=ai_provider_entity.label,
            icon_small=ai_provider_entity.icon_small,
            icon_large=ai_provider_entity.icon_large,
            supported_model_types=ai_provider_entity.supported_model_types,
            description=ai_provider_entity.description,
            background=ai_provider_entity.background,
            help=ai_provider_entity.help,
            credential_form=ai_provider_entity.credential_form,
        )
        self.user_configuration=user_configuration
        self.system_configuration=system_configuration

    @field_serializer('user_configuration')
    def get_user_configuration(self, user_configuration: UserConfiguration) -> dict[str, Any]:
        '''
        Serializes UserConfiguration into a dictionary.
        '''

        active =  user_configuration is not None and \
            (user_configuration.provider is not None or len(user_configuration.models) > 0)
        provider = user_configuration.provider.provider_id \
            if user_configuration is not None and user_configuration.provider is not None \
            else None
        return {
            'active': active,
            'provider': provider,
        }

    @field_serializer('system_configuration')
    def get_system_configuration(self, system_configuration: SystemConfiguration) -> dict[str, Any]:
        '''
        Serializes SystemConfiguration into a dictionary.
        '''

        active = system_configuration is not None and system_configuration.enabled
        return {
            'active': active,
        }

    def get_provider_models(self, model_type: ModelType=None):
        '''
        Retrieves models from the AI provider instance based on the specified model type.
        '''

        ai_provider_instance = ai_provider_factory.get_ai_provider_instance(provider_name=self.id)

        model_types = []
        if model_type:
            model_types.append(model_type)
        else:
            model_types = self.supported_model_types

        provider_entity = ai_provider_instance.get_schema()
        all_models = []
        for model_type in model_types:
            models = ai_provider_instance.get_models(model_type=model_type.value)
            for model in models:
                model_with_provider_entity = ModelWithProviderEntity(
                    id=model.id,
                    label=model.label,
                    type=model.type,
                    features=model.features,
                    properties=model.properties,
                    deprecated=model.deprecated,
                    active=True,
                    provider=provider_entity.to_common_ai_provider(),
                )
                all_models.append(model_with_provider_entity)

        return all_models


class ModelCollectionBundle(BaseModel):
    '''
    Encapsulates the configuration and instances
    related to an AI provider and specific model type.
    '''

    configuration: AIProviderConfiguration
    ai_provider_instance: AIProvider
    model_collection_instance: ModelCollection

    # pydantic configs
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())


class ModelBundle(ModelCollectionBundle):
    '''
    Encapsulates the ModelCollectionBundle along with specific model schema
    and provided parameters and credentials.
    '''

    model_schema: ModelEntity
    parameters: dict[str, Any] = {}
    credentials: dict[str, Any] = {}

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())
