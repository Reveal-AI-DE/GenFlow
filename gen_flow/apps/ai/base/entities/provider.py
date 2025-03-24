# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from collections.abc import Sequence
from typing import Optional

from gen_flow.apps.common.entities import BaseYamlEntityWithIcons, ConfigurationEntity, HelpEntity
from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.base.entities.model import CommonModelEntity

class CommonAIProviderEntity(BaseYamlEntityWithIcons):
    '''
    Represents a common AI provider entity with associated metadata.
    '''

    id: str
    supported_model_types: Sequence[ModelType]


class SimpleAIProviderEntity(CommonAIProviderEntity):
    '''
    A subclass of CommonAIProviderEntity with a list of models.
    '''

    models: list[CommonModelEntity] = []


class AIProviderEntity(SimpleAIProviderEntity):
    '''
    Represents an AI provider entity with additional attributes and methods.
    '''

    background: Optional[str] = None
    help: Optional[HelpEntity] = None
    credential_form: Optional[list[ConfigurationEntity]] = []

    def to_common_ai_provider(self) -> CommonAIProviderEntity:
        return SimpleAIProviderEntity(
            id=self.id,
            label=self.label,
            description=self.description,
            icon_small=self.icon_small,
            icon_large=self.icon_large,
            supported_model_types=self.supported_model_types,
        )

    def validate_credential_form(self, credentials: dict) -> dict:
        '''
        Validates the credential form for the AI provider.
        '''

        validated_credentials = {}
        for configuration_entity in self.credential_form:
            #  If the variable does not exist in credentials
            if configuration_entity.name not in credentials or not credentials[configuration_entity.name]:
                # If required is True, an exception is thrown
                if configuration_entity.required:
                    raise ValueError(f'Variable {configuration_entity.name} is required')
                else:
                    # Get the value of default
                    if configuration_entity.default:
                        # If it exists, add it to validated_credentials
                        validated_credentials[configuration_entity.name]=configuration_entity.default
                        continue
                    else:
                        # If default does not exist, skip
                        continue

            # If the variable exists in credentials
            # Validate the value
            configuration_entity.validate(credentials[configuration_entity.name], prefix='Variable')
            # Add the value to validated_credentials
            validated_credentials[configuration_entity.name] = credentials[configuration_entity.name]

        return validated_credentials
