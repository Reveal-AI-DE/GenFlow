# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional, Any
from json import loads as json_loads, JSONDecodeError

from pydantic import BaseModel
from django.db import models

from gen_flow.apps.common.entities import TranslationEntity, ConfigurationType, ConfigurationEntity
from gen_flow.apps.common.models import TimeAuditModel, UserOwnedModel, TeamAssociatedModel
from gen_flow.apps.common.security import encrypter
from gen_flow.apps.ai import ai_provider_factory
from gen_flow.apps.ai.base.entities.provider import AIProviderEntity
from gen_flow.apps.core.config.entities import UserProviderConfiguration, SystemConfiguration


class AboutSystem(BaseModel):
    '''
    Represents the system information.
    '''

    name: TranslationEntity
    description: TranslationEntity
    license: TranslationEntity
    version: str


class Provider(TimeAuditModel, UserOwnedModel, TeamAssociatedModel):
    '''
    Represents an AI service provider enabled by the user with associated credentials.

    Attributes:
        provider_name (str): The name of the provider.
        encrypted_config (str): The encrypted configuration details for the provider.
        is_valid (bool): Indicates if the provider is valid.
        last_used (datetime): The last time the provider was used.
    '''

    provider_name = models.CharField(max_length=255, null=False, blank=False)
    encrypted_config = models.TextField(null=True)
    is_valid = models.BooleanField(default=False)
    last_used = models.DateTimeField(null=True)

    class Meta:
        # Unique constraint on team and provider_name.
        constraints = [
            models.UniqueConstraint(fields=['team', 'provider_name'], name='unique_provider_team')
        ]

    @property
    def is_enabled(self) -> bool:
        '''
        Returns if the provider is valid.
        '''

        return self.is_valid

    @property
    def user_provider_configuration(self) -> UserProviderConfiguration:
        '''
        Returns the user provider configuration if enabled.
        Credentials are decrypted using the team's RSA key.
        '''

        if not self.is_enabled:
            return None
        else:
            # Get provider credential secret variables
            provider_credential_secret_variables = Provider.extract_secret_variables(provider_name=self.provider_name)
            # fix origin data
            provider_credentials = self.fix_encrypted_config()

            # Get decoding rsa key and cipher for decrypting credentials
            decoding_rsa_key, decoding_cipher_rsa = encrypter.get_decrypt_decoding(str(self.team.id))

            for variable in provider_credential_secret_variables:
                if variable in provider_credentials:
                    try:
                        provider_credentials[variable] = encrypter.decrypt_token_with_decoding(
                            provider_credentials.get(variable), decoding_rsa_key, decoding_cipher_rsa
                        )
                    except ValueError:
                        pass

            return UserProviderConfiguration(provider_id=str(self.id), credentials=provider_credentials)

    @property
    def system_configuration(self) -> SystemConfiguration:
        '''
        Returns the system configuration for the provider.
        '''

        # TODO: for now, all providers are enabled by default at system level
        return SystemConfiguration(enabled=self.is_enabled)

    def fix_encrypted_config(self):
        '''
        Fixes and returns the decrypted configuration details.
        '''

        try:
            if self.encrypted_config:
                if not self.encrypted_config.startswith('{'):
                    original_credentials = {'openai_api_key': self.encrypted_config}
                else:
                    original_credentials = json_loads(self.encrypted_config)
            else:
                original_credentials = {}
        except JSONDecodeError:
            original_credentials = {}

        return original_credentials

    def obfuscated_credentials(self) -> dict:
        # Get provider credential secret variables
        credential_secret_variables = Provider.extract_secret_variables(provider_name=self.provider_name)

        # fix origin data
        credentials = self.fix_encrypted_config()

        # Obfuscate credentials
        for key, value in credentials.items():
            if key in credential_secret_variables:
                credentials[key] = encrypter.obfuscated_token(value)

        return credentials

    @staticmethod
    def extract_secret_variables(provider_name: str) -> list[str]:
        '''
        Extracts secret variables for the given provider name.
        '''

        ai_provider_entity: AIProviderEntity = ai_provider_factory.get_ai_provider_instance(provider_name=provider_name).get_schema()
        credential_form: list[ConfigurationEntity] = ai_provider_entity.credential_form

        secret_input_form_variables = []
        for configuration_entity in credential_form:
            if configuration_entity.type == ConfigurationType.SECRET:
                secret_input_form_variables.append(configuration_entity.name)

        return secret_input_form_variables


class ProviderModelConfig(TimeAuditModel):
    '''
    Represents model configuration including parameters.

    Attributes:
        provider_name (str): The name of the provider.
        model_name (str): The name of the model.
        config (dict): A JSON field containing the configuration details.
    '''

    provider_name = models.CharField(max_length=255, null=False, blank=False)
    model_name = models.CharField(max_length=255, null=False, blank=False)
    config = models.JSONField(null=True, blank=True)

    @property
    def parameters(self) -> dict[str, Any]:
        '''
        Retrieves the 'parameters' from the config JSON field. Defaults to an empty dictionary if not present.
        '''

        return self.config.get('parameters', {})

    @property
    def mode(self) -> Optional[str]:
        '''
        Retrieves the 'mode' from the config JSON field. Defaults to None if not present.
        '''

        return self.config.get('mode', None)

    @property
    def stop(self) -> Optional[list[str]]:
        '''
        Retrieves the 'stop' list from the config JSON field. Defaults to an empty list if not present.
        '''

        return self.config.get('stop', [])
