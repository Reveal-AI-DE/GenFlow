# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from functools import reduce

from django.db import transaction
from rest_framework import serializers

from gen_flow.apps.team.serializers import BasicUserSerializer
from gen_flow.apps.core.config.llm_model_bundle import LLMModelBundle
from gen_flow.apps.core.serializers import ProviderModelConfigReadSerializer, ProviderModelConfigWriteSerializer
from gen_flow.apps.prompt.models import Prompt
from gen_flow.apps.prompt.serializers import PromptReadSerializer
from gen_flow.apps.session.models import SessionType, Session, SessionMessage


class SessionReadSerializer(serializers.ModelSerializer):
    '''
    Serializer for reading Session data, to be used by get actions.
    '''

    related_model = ProviderModelConfigReadSerializer(required=False)
    related_prompt = PromptReadSerializer(required=False)
    owner = BasicUserSerializer()

    class Meta:
        '''
        Defines the model and fields to be serialized.
        '''

        model = Session
        fields = ('id', 'name', 'session_type', 'session_mode', 'related_model',
            'related_prompt', 'created_date', 'updated_date', 'owner')


class SessionWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for writing Session data, to be used by post/patch actions.
    '''

    related_model = ProviderModelConfigWriteSerializer(required=False)
    related_prompt = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Prompt.objects.none(),  # Default to none
    )

    def __init__(self, *args, **kwargs):
        '''
        Initializes the serializer and dynamically filters
        the `related_prompt` queryset based on the IAM context in the request.
        '''

        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'iam_context'):
            team = request.iam_context.team
            if team:
                # Filter queryset based on the iam_context
                self.fields['related_prompt'].queryset = Prompt.objects.filter(team=team)

    class Meta:
        '''
        Defines the model and fields to be serialized.
        '''

        model = Session
        fields = ('name', 'session_type', 'related_model', 'related_prompt')

    def validate(self, data) -> dict:
        '''
        Validates the input data. Ensures that `related_model` is provided for
        LLM sessions and `related_prompt` is provided for PROMPT sessions.
        '''

        super().validate(data)
        session_type = data.get('session_type')
        if session_type == SessionType.LLM.value and \
            'related_model' not in data:
            raise serializers.ValidationError('related_model is required for LLM session')
        elif session_type == SessionType.PROMPT.value and \
            'related_prompt' not in data:
            raise serializers.ValidationError('related_prompt is required for PROMPT session')
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> Session:
        '''
        Creates a new Session instance. Handles nested creation
        of related models using the `ProviderModelConfigWriteSerializer`.
        '''

        session_type = validated_data.pop('session_type', SessionType.LLM.value)

        if session_type == SessionType.LLM.value:
            related_model_data = validated_data.pop('related_model')
            # Creates a new ProviderModelConfig instance using the 'related_model' data.
            # Using serializer to call the create method of the related model.
            related_model_serializer = ProviderModelConfigWriteSerializer(
                data=related_model_data,
                context=self.context
            )
            related_model = related_model_serializer.create(related_model_data)
            # Creates a new Session instance with the provided data.
            session = Session.objects.create(
                session_type=session_type,
                related_model=related_model,
                **validated_data)

        else:
            # removes the related_model data from the validated data,
            # if it is presented.
            if 'related_model' in validated_data:
                validated_data.pop('related_model')
            # Creates a new Session instance with the provided data.
            session = Session.objects.create(
                session_type=session_type,
                **validated_data)

        return session

    @transaction.atomic
    def update(self, instance: Session, validated_data: dict) -> Session:
        '''
        Updates an existing Session instance. Handles nested updates
        of related models using the `ProviderModelConfigWriteSerializer`.
        '''

        related_model = validated_data.pop('related_model', None)
        if related_model:
            # Updates ProviderModelConfig instance.
            # Using serializer to call the update method of the related model.
            related_model_serializer = ProviderModelConfigWriteSerializer(
                instance=instance.related_model,
                context=self.context
            )
            related_model_serializer.update(instance.related_model, related_model)
        # session type is not allowed to be updated
        if 'session_type' in validated_data:
            instance.session_type = validated_data.pop('session_type')
        return super().update(instance, validated_data)

    def to_representation(self, instance) -> dict:
        '''
        Converts the Session instance into a serialized representation
        using the `SessionReadSerializer`.
        '''

        serializer = SessionReadSerializer(instance, context=self.context)
        return serializer.data


class SessionMessageReadSerializer(serializers.ModelSerializer):
    '''
    Serializer for reading SessionMessage data, to be used by get actions.
    '''

    owner = serializers.StringRelatedField()

    class Meta:
        '''
        Defines the model and fields to be serialized.
        '''

        model = SessionMessage
        fields = ('id', 'query', 'answer', 'created_date', 'updated_date', 'owner')


class SessionMessageWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for writing SessionMessage data, to be used by post/patch actions.
    '''

    session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        '''
        Defines the model and fields to be serialized.
        '''

        model = SessionMessage
        fields = ('session', 'query', 'answer')

    def to_representation(self, instance):
        '''
        Converts the SessionMessage instance into a serialized representation
        using the `SessionMessageReadSerializer`.
        '''

        serializer = SessionMessageReadSerializer(instance, context=self.context)
        return serializer.data


class GenerateRequestSerializer(serializers.Serializer):
    query = serializers.CharField()
    files = serializers.ListField(child=serializers.JSONField(), required=False)
    parameters = serializers.JSONField(required=False)
    stream = serializers.BooleanField(default=False)

    def validate(self, data):
        parameters = data.get('parameters', None)
        if parameters is not None:
            model_bundle: LLMModelBundle = self.context.get('llm_model_bundle')
            provider_model_serializer = ProviderModelConfigWriteSerializer(
                data={
                    'provider_name': model_bundle.configuration.id,
                    'model_name': model_bundle.model_schema.id,
                    'config': {
                        'parameters': parameters
                    }
                },
                context=self.context
            )
            provider_model_serializer.is_valid(raise_exception=True)
            data['related_model'] = provider_model_serializer.data
        return data
