# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional, Dict

from django.db.models.query import QuerySet

from gen_flow.apps.ai import ai_provider_factory
from gen_flow.apps.ai.base.entities.provider import AIProviderEntity
from gen_flow.apps.core.models import Provider
from gen_flow.apps.core.config.entities import AIProviderConfiguration, UserConfiguration

class AIProviderConfigurationService:
    staticmethod
    def get_provider_entity(provider_name: str) -> AIProviderEntity:
        return ai_provider_factory.get_ai_provider_instance(provider_name).get_schema()


    @staticmethod
    def get_provider_configuration(
        provider_name: str,
        queryset: Optional[QuerySet[AIProviderConfiguration]] = None,
        db_provider: Optional[Provider] = None,
        ai_provider_entity: Optional[AIProviderEntity] = None,
    ) -> AIProviderConfiguration:
        if ai_provider_entity is None:
            ai_provider_entity = AIProviderConfigurationService.get_provider_entity(provider_name)

        if db_provider is None:
            if queryset is not None:
                db_provider = queryset.filter(provider_name=provider_name).first()
            else:
                raise ValueError('Either queryset or db_provider should be provided')

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
    def get_configuration(queryset: QuerySet[AIProviderConfiguration]) -> Dict[str, AIProviderConfiguration]:
        ai_provider_entities = ai_provider_factory.get_ai_provider_schemas()
        provider_configurations = {}
        for ai_provider_entity in ai_provider_entities:
            db_provider = queryset.filter(provider_name=ai_provider_entity.id).first()
            ai_provider_configuration = AIProviderConfigurationService.get_provider_configuration(
                provider_name=ai_provider_entity.id,
                queryset=queryset,
                db_provider=db_provider,
                ai_provider_entity=ai_provider_entity
            )
            provider_configurations[ai_provider_entity.id] = ai_provider_configuration

        return provider_configurations
