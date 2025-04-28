# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from typing import Dict, List, Optional, cast

from django.db.models.query import QuerySet

from genflow.apps.ai import ai_provider_factory
from genflow.apps.ai.base.entities.provider import AIProviderEntity
from genflow.apps.ai.base.entities.shared import ModelType
from genflow.apps.ai.llm.llm_model_collection import LLMModelCollection
from genflow.apps.common.entities import ConfigurationEntity
from genflow.apps.core.config.entities import (
    AIProviderConfiguration,
    ModelCollectionBundle,
    ModelWithProviderEntity,
    UserConfiguration,
)
from genflow.apps.core.models import Provider


class AIProviderConfigurationService:
    """
    Service class for managing AI provider configurations.
    """

    @staticmethod
    def get_provider_entity(provider_name: str) -> AIProviderEntity:
        """
        Retrieves the AI provider entity schema for the given provider name.
        """

        return ai_provider_factory.get_ai_provider_instance(
            provider_name=provider_name
        ).get_schema()

    @staticmethod
    def get_provider_configuration(
        provider_name: str,
        queryset: Optional[QuerySet[Provider]] = None,
        db_provider: Optional[Provider] = None,
        ai_provider_entity: Optional[AIProviderEntity] = None,
    ) -> AIProviderConfiguration:
        """
        Retrieves the AI provider configuration for the given provider name.
        """

        if ai_provider_entity is None:
            ai_provider_entity = AIProviderConfigurationService.get_provider_entity(provider_name)

        if db_provider is None:
            if queryset is not None:
                db_provider = queryset.filter(provider_name=provider_name).first()
            else:
                raise ValueError("Either queryset or db_provider should be provided")

        user_configuration = UserConfiguration(
            provider=db_provider.user_provider_configuration if db_provider else None,
        )
        system_configuration = db_provider.system_configuration if db_provider else None

        ai_provider_configuration = AIProviderConfiguration(
            ai_provider_entity=ai_provider_entity,
            user_configuration=user_configuration,
            system_configuration=system_configuration,
        )

        return ai_provider_configuration

    @staticmethod
    def get_configuration(queryset: QuerySet[Provider]) -> Dict[str, AIProviderConfiguration]:
        """
        Retrieves configurations for all AI providers.
        """

        ai_provider_entities = ai_provider_factory.get_ai_provider_schemas()
        provider_configurations = {}
        for ai_provider_entity in ai_provider_entities:
            db_provider = queryset.filter(provider_name=ai_provider_entity.id).first()
            ai_provider_configuration = AIProviderConfigurationService.get_provider_configuration(
                provider_name=ai_provider_entity.id,
                queryset=queryset,
                db_provider=db_provider,
                ai_provider_entity=ai_provider_entity,
            )
            provider_configurations[ai_provider_entity.id] = ai_provider_configuration

        return provider_configurations

    @staticmethod
    def get_provider_models(
        provider_name: str,
        queryset: Optional[QuerySet[AIProviderConfiguration]] = None,
        db_provider: Optional[Provider] = None,
        model_type: Optional[str] = None,
        enabled_only: Optional[bool] = False,
    ) -> List[ModelWithProviderEntity]:
        """
        Retrieves models for a specific AI provider.
        """

        ai_provider_configuration = AIProviderConfigurationService.get_provider_configuration(
            provider_name, queryset=queryset, db_provider=db_provider
        )
        if enabled_only and ai_provider_configuration.user_configuration.provider is None:
            return []

        try:
            model_type = ModelType(model_type) if model_type else None
        except ValueError:
            raise ValueError(f"Invalid model type: {model_type}")

        return ai_provider_configuration.get_provider_models(model_type=model_type)

    @staticmethod
    def get_models(
        queryset: Optional[QuerySet[Provider]],
        model_type: Optional[str] = None,
        enabled_only: Optional[bool] = False,
    ) -> List[ModelWithProviderEntity]:
        """
        Retrieves models for all AI providers.
        """

        ai_provider_entities = ai_provider_factory.get_ai_provider_schemas()

        models = []
        for ai_provider_entity in ai_provider_entities:
            db_provider = queryset.filter(provider_name=ai_provider_entity.id).first()
            provider_models = AIProviderConfigurationService.get_provider_models(
                provider_name=ai_provider_entity.id,
                queryset=queryset,
                db_provider=db_provider,
                model_type=model_type,
                enabled_only=enabled_only,
            )

            models.extend(provider_models)

        return models

    # pylint: disable=too-many-positional-arguments
    @staticmethod
    def get_model(
        model_name: str,
        provider_name: Optional[str],
        queryset: Optional[QuerySet[Provider]] = None,
        db_provider: Optional[Provider] = None,
        model_type: Optional[str] = None,
        enabled_only: Optional[bool] = False,
    ) -> ModelWithProviderEntity:
        """
        Retrieves a specific model by name.
        """

        models: List[ModelWithProviderEntity] = []
        if provider_name is not None:
            if db_provider is None:
                db_provider = queryset.filter(provider_name=provider_name).first()
            models = AIProviderConfigurationService.get_provider_models(
                provider_name,
                queryset=queryset,
                db_provider=db_provider,
                model_type=model_type,
                enabled_only=enabled_only,
            )
        else:
            models = AIProviderConfigurationService.get_models(
                queryset=queryset,
                model_type=model_type,
                enabled_only=enabled_only,
            )

        model = next((model for model in models if model.id == model_name), None)

        return model

    @staticmethod
    def get_model_parameter_configs(
        provider_name: str, model_name: str
    ) -> list[ConfigurationEntity]:
        """
        Retrieves the parameter configuration for a specific model from a given provider.
        """
        # Get model instance of LLM
        provider_instance = ai_provider_factory.get_ai_provider_instance(
            provider_name=provider_name
        )
        model_collection_instance = provider_instance.get_model_collection_instance(
            model_type=ModelType.LLM.value
        )
        model_collection_instance = cast(LLMModelCollection, model_collection_instance)
        # Get parameter configurations
        return model_collection_instance.get_parameter_configs(model_name)

    @staticmethod
    def process_model_parameters(
        provider_name: str, model_name: str, model_parameters: dict
    ) -> dict:
        """
        Validates and filters the model parameters for a specific model from a given provider.
        """

        # Get model instance of LLM
        provider_instance = ai_provider_factory.get_ai_provider_instance(
            provider_name=provider_name
        )
        model_collection_instance = provider_instance.get_model_collection_instance(
            model_type=ModelType.LLM.value
        )
        model_collection_instance = cast(LLMModelCollection, model_collection_instance)
        # Process model parameters
        return model_collection_instance._process_model_parameters(model_name, model_parameters)

    @staticmethod
    def get_model_collection_bundle(
        provider_name: str,
        queryset: Optional[QuerySet[Provider]] = None,
        db_provider: Optional[Provider] = None,
        model_type: Optional[str] = ModelType.LLM.value,
    ) -> ModelCollectionBundle:
        """
        Retrieves the model collection bundle for the given provider name.
        """

        ai_provider_configuration = AIProviderConfigurationService.get_provider_configuration(
            provider_name=provider_name, queryset=queryset, db_provider=db_provider
        )
        ai_provider_instance = ai_provider_factory.get_ai_provider_instance(
            provider_name=provider_name
        )

        try:
            model_type = ModelType(model_type) if model_type else ModelType.LLM
        except ValueError:
            raise ValueError("Invalid model type")

        model_collection_instance = ai_provider_instance.get_model_collection_instance(
            model_type=model_type.value
        )

        return ModelCollectionBundle(
            configuration=ai_provider_configuration,
            ai_provider_instance=ai_provider_instance,
            model_collection_instance=model_collection_instance,
        )
