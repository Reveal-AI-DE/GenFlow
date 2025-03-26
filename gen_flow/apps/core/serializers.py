# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp
from typing import Any
from json import dumps as json_dumps

from django.conf import settings
from rest_framework import serializers

from gen_flow.apps.common.security.encrypter import encrypt_token, decrypt_token
from gen_flow.apps.common.entities import TranslationEntity, ConfigurationEntity
from gen_flow.apps.common.file_utils import create_media_symbolic_links
from gen_flow.apps.ai import ai_provider_factory
from gen_flow.apps.ai.base.entities.provider import CommonAIProviderEntity
from gen_flow.apps.team.models import Team
from gen_flow.apps.core.models import Provider, ProviderModelConfig
from gen_flow.apps.core.config.entities import ModelWithProviderEntity, AIProviderConfiguration
from gen_flow.apps.core.config.provider_service import AIProviderConfigurationService


class CommonAIProviderEntitySerializer(serializers.BaseSerializer):
    fields = {}

    def serialize_icon_entity(self, provider_name: str, icon: TranslationEntity) -> dict[str, str] | None:
        if not icon:
            return None

        data = icon.model_dump()

        icons = {}
        for key, value in data.items():
            icons[key] = osp.join(settings.PROVIDERS_URL, provider_name, 'icons', osp.basename(value))

        return icons

    def to_representation(self, instance: CommonAIProviderEntity) -> dict[str, Any]:
        '''
        Serializes CommonAIProviderEntity into json
        '''

        if not instance.id.isalnum():
            raise ValueError('Invalid provider name')

        # Create media paths
        provider_icons_path = osp.join(settings.MODEL_CONFIG_ROOT, instance.id, 'icons')
        provider_icons_media_path = osp.join(settings.PROVIDERS_ROOT, instance.id, 'icons')
        create_media_symbolic_links(provider_icons_path, provider_icons_media_path)

        data = instance.model_dump(mode='json')
        data['icon_small'] = self.serialize_icon_entity(instance.id, instance.icon_small)
        data['icon_large'] = self.serialize_icon_entity(instance.id, instance.icon_large)

        return data


class ModelWithProviderEntitySerializer(serializers.BaseSerializer):
    fields = {}

    def to_representation(self, instance: ModelWithProviderEntity) -> dict[str, Any]:
        '''
        Serializes ModelWithProviderEntity into json
        '''

        data = instance.model_dump(mode='json')
        data['provider'] = CommonAIProviderEntitySerializer(instance.provider).data

        return data

class AIProviderConfigurationSerializer(CommonAIProviderEntitySerializer):
    def to_representation(self, instance: AIProviderConfiguration) -> dict[str, Any]:
        '''
        Serializes AIProviderConfiguration into json
        '''

        common_data = super().to_representation(instance)
        data = instance.model_dump(mode='json')
        data['icon_small'] = common_data['icon_small']
        data['icon_large'] = common_data['icon_large']

        return data


class ProviderReadSerializer(serializers.ModelSerializer):
    '''
    Serializer for reading provider details.
    '''

    credentials = serializers.SerializerMethodField()

    def get_credentials(self, obj: Provider) -> dict:
        '''
        Returns the decrypted credentials.
        '''

        if not obj.is_enabled:
            return {}
        return obj.obfuscated_credentials()

    class Meta:
        model = Provider
        fields = ['id', 'provider_name', 'credentials', 'is_enabled', 'last_used']


class ConfigurationEntitySerializer(serializers.BaseSerializer):
    fields = {}

    def to_representation(self, instance: ConfigurationEntity) -> dict[str, Any]:
        '''
        Serializes ConfigurationEntity into json
        '''

        data = instance.model_dump(mode='json')
        return data

class ProviderWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for writing provider details.
    '''

    HIDDEN_VALUE = '[__HIDDEN__]'

    credentials = serializers.JSONField()


    class Meta:
        model = Provider
        fields = ['provider_name', 'credentials']

    def decrypt_credentials(self, obj: Provider, new_credentials: dict) -> dict:
        '''
        Decrypts the provider's credentials if necessary, if a value in new_credentials is set to [__HIDDEN__]
        '''

        original_credentials = obj.fix_encrypted_config()
        secret_variables = Provider.extract_secret_variables(provider_name=obj.provider_name)
        # decrypt credentials
        for key, value in new_credentials.items():
            if key in secret_variables:
                # if send [__HIDDEN__] in secret input, it will be same as original value
                if value == self.HIDDEN_VALUE and key in original_credentials:
                    new_credentials[key] = decrypt_token(str(obj.team.id), original_credentials[key])

        return new_credentials

    def validate_and_encrypt_credentials(self, provider_name: str, team_id: str, credentials: dict) -> dict:
        '''
        Validates and encrypts the provided credentials for a given provider.

        Raises:
            serializers.ValidationError: If the credentials validation fails.
        '''

        try:
            credentials = ai_provider_factory.validate_credentials(
                provider_name=provider_name, credentials=credentials
            )
        except Exception as ex:
            raise serializers.ValidationError(str(ex))

        secret_variables = Provider.extract_secret_variables(provider_name=provider_name)
        for key, value in credentials.items():
            if key in secret_variables:
                credentials[key] = encrypt_token(team_id, value)

        return credentials

    def validate(self, attrs: dict) -> dict:
        '''
        Validates the provided attributes.

        Raises:
            serializers.ValidationError: If the request context is missing or
                if the team context is missing.
        '''

        # get team from context
        request = self.context.get('request', None)
        if request is None:
            raise serializers.ValidationError('Request context is required.')
        db_team: Team = request.iam_context.get('team', None)
        if db_team is None:
            raise serializers.ValidationError('Team context is required.')

        provider_name = attrs.get('provider_name')
        credentials = attrs.pop('credentials')

        # check if provider already exists
        db_provider = Provider.objects.filter(team=db_team, provider_name=provider_name).first()
        # update request
        if db_provider is not None:
            credentials = self.decrypt_credentials(db_provider, credentials)

        # validate and encrypt credentials
        credentials = self.validate_and_encrypt_credentials(provider_name, str(db_team.id), credentials)

        attrs['encrypted_config'] = json_dumps(credentials)
        attrs['is_valid'] = True
        return attrs

    def update(self, instance, validated_data):
        '''
        Updates the provider instance, ensuring that provider_name cannot be changed.
        '''

        # Remove provider_name from validated_data if present
        validated_data.pop('provider_name', None)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        '''
        Converts the instance to its representation using the ProviderReadSerializer.
        '''

        serializer = ProviderReadSerializer(instance, context=self.context)
        return serializer.data


def get_model(request, model_name: str, provider_name: str) -> ModelWithProviderEntity:
    '''
    Returns the model entity for the given model name and provider name.
    '''
    try:
        db_provider = Provider.objects.get(
            provider_name=provider_name,
            is_valid=True,
            team=request.iam_context.get('team'),
        )
    except Provider.DoesNotExist:
        raise serializers.ValidationError(f'AI Provider {provider_name} not enabled')

    model = AIProviderConfigurationService.get_model(
        model_name=model_name,
        provider_name=provider_name,
        db_provider=db_provider,
        enabled_only=True
    )
    return model


class ProviderModelConfigReadSerializer(serializers.ModelSerializer):
    '''
    Serializer for reading ProviderModelConfig data, to be used by get actions.
    '''

    def get_entity(self, instance: ProviderModelConfig) -> ModelWithProviderEntity:
        '''
        Retrieves a model entity based on the provided instance and request context.
        '''

        return get_model(
            request=self.context.get('request'),
            model_name=instance.model_name,
            provider_name=instance.provider_name
        )

    def get_model_parameter_configs(self, instance: ProviderModelConfig) -> list[ConfigurationEntity]:
        '''
        Retrieves the model parameter configurations for a given provider model instance.
        '''

        parameter_configs = AIProviderConfigurationService.get_model_parameter_configs(
            provider_name=instance.provider_name,
            model_name=instance.model_name,
        )
        return parameter_configs

    class Meta:
        '''
        Defines the model and fields to be serialized.
        '''

        model = ProviderModelConfig
        fields = ('provider_name', 'model_name', 'config',)

    def to_representation(self, instance):
        '''
        Converts the given instance into its serialized representation.
        '''

        data = super().to_representation(instance)

        model_entity = self.get_entity(instance)
        if model_entity:
            model_data = ModelWithProviderEntitySerializer(model_entity).data
            data['entity'] = model_data
            parameter_configs = self.get_model_parameter_configs(instance)
            parameter_configs_data = [ConfigurationEntitySerializer(parameter_config).data for parameter_config in parameter_configs]
            data['entity']['parameter_rules'] = parameter_configs_data

        return data


class ProviderModelConfigWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for writing ProviderModelConfig data, to be used by post/patch actions.
    '''

    class Meta:
        '''
        Defines the model and fields to be serialized.
        '''

        model = ProviderModelConfig
        fields = ('provider_name', 'model_name', 'config')

    def validate(self, data: dict):
        '''
        Validates the input data for the serializer.
        '''
        data = super().validate(data)

        provider_name = data.get('provider_name')
        model_name = data.get('model_name')
        config = data.get('config', None)
        if config is None:
            config = {}

        # Retrieves the AI model using the provided `provider_name` and `model_name`.
        # Raises a `ValidationError` if the model is not found.
        model = get_model(
            request=self.context.get('request'),
            model_name=model_name,
            provider_name=provider_name
        )
        if not model:
            raise serializers.ValidationError(f'AI Model {model_name} not found for provider {provider_name}')


        # Validates and processes the `config` field in the data. If `config` is not
        # provided, it initializes it as an empty dictionary.

        # Ensures that the `parameters` key exists in the `config`
        if 'parameters' not in config:
            config['parameters'] = {}

        # Processes the model parameters sing the `AIProviderConfigurationService`.
        config['parameters'] = AIProviderConfigurationService.process_model_parameters(
            provider_name=provider_name,
            model_name=model_name,
            model_parameters=config['parameters']
        )
        data['config'] = config
        return data
