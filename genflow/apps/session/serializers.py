# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import pandas as pd
from django.db import transaction
from rest_framework import serializers

from genflow.apps.core.config.llm_model_bundle import LLMModelBundle
from genflow.apps.core.serializers import (
    ProviderModelConfigReadSerializer,
    ProviderModelConfigWriteSerializer,
)
from genflow.apps.team.serializers import BasicUserSerializer
from genflow.apps.prompt.models import Prompt
from genflow.apps.prompt.serializers import PromptReadSerializer
from genflow.apps.assistant.models import Assistant
from genflow.apps.assistant.serializers import AssistantReadSerializer
from genflow.apps.session.models import Session, SessionMessage, SessionType


class SessionReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Session data, to be used by get actions.
    """

    related_model = ProviderModelConfigReadSerializer(required=False)
    related_prompt = PromptReadSerializer(required=False)
    related_assistant = AssistantReadSerializer(required=False)
    owner = BasicUserSerializer()
    usage = serializers.SerializerMethodField()

    def get_usage(self, instance: Session) -> dict:
        usage = {
            "total_messages": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_price": 0,
            "total_input_price": 0,
            "total_output_price": 0,
            "currency": "USD",
            "per_day": [],
        }
        # Check if there are any messages in the session
        count = instance.sessionmessage_set.count()
        if count == 0:
            return usage

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(instance.get_usage())

        # Calculate the total usage
        usage["total_messages"] = count
        usage["total_input_tokens"] = df["input_tokens"].sum()
        usage["total_output_tokens"] = df["output_tokens"].sum()
        usage["total_price"] = df["total_price"].sum()

        # Calculate the total input/output price
        usage["total_input_price"] = df.apply(
            lambda row: row["input_tokens"] * row["input_unit_price"] * row["input_price_unit"],
            axis=1,
        ).sum()
        usage["total_output_price"] = df.apply(
            lambda row: row["output_tokens"] * row["output_unit_price"] * row["output_price_unit"],
            axis=1,
        ).sum()

        # Calculate the per day usage
        per_day = (
            df.groupby(df["created_date"].dt.date)
            .agg(total_messages=("input_tokens", "count"), total_price=("total_price", "sum"))
            .reset_index()
        )
        per_day["created_date"] = pd.to_datetime(per_day["created_date"])
        per_day["day"] = per_day["created_date"].dt.strftime("%Y-%m-%d")
        per_day = per_day.drop(columns=["created_date"])
        per_day = per_day.to_dict(orient="records")
        usage["per_day"] = per_day

        return usage

    class Meta:
        """
        Defines the model and fields to be serialized.
        """

        model = Session
        fields = (
            "id",
            "name",
            "session_type",
            "session_mode",
            "related_model",
            "related_prompt",
            "related_assistant",
            "created_date",
            "updated_date",
            "owner",
            "usage",
        )


class SessionWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing Session data, to be used by post/patch actions.
    """

    related_model = ProviderModelConfigWriteSerializer(required=False)
    related_prompt = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Prompt.objects.none(),  # Default to none
    )
    related_assistant = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Assistant.objects.none(), # Default to none
    )


    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer and dynamically filters
        the `related_prompt` and `related_assistant` queryset based on the IAM context in the request.
        """

        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "iam_context"):
            team = request.iam_context.team
            if team:
                # Filter querysets based on the iam_context
                self.fields["related_prompt"].queryset = Prompt.objects.filter(team=team)
                # Filter querysets based on the iam_context
                self.fields["related_assistant"].queryset = Assistant.objects.filter(team=team)

    class Meta:
        """
        Defines the model and fields to be serialized.
        """

        model = Session
        fields = ("name", "session_type", "session_mode", "related_model", "related_prompt", "related_assistant")

    def validate(self, data) -> dict:
        """
        Validates the input data. Ensures that `related_model` is provided for
        LLM sessions and `related_prompt` is provided for PROMPT sessions.
        """

        super().validate(data)
        session_type = data.get("session_type")
        if session_type == SessionType.LLM.value and "related_model" not in data:
            raise serializers.ValidationError("related_model is required for LLM session")
        elif session_type == SessionType.PROMPT.value and "related_prompt" not in data:
            raise serializers.ValidationError("related_prompt is required for PROMPT session")
        elif session_type == SessionType.ASSISTANT.value and "related_assistant" not in data:
            raise serializers.ValidationError("related_assistant is required for ASSISTANT session")
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> Session:
        """
        Creates a new Session instance. Handles nested creation
        of related models using the `ProviderModelConfigWriteSerializer`.
        """

        session_type = validated_data.pop("session_type", SessionType.LLM.value)

        if session_type == SessionType.LLM.value:
            related_model_data = validated_data.pop("related_model")
            # Creates a new ProviderModelConfig instance using the 'related_model' data.
            # Using serializer to call the create method of the related model.
            related_model_serializer = ProviderModelConfigWriteSerializer(
                data=related_model_data, context=self.context
            )
            related_model = related_model_serializer.create(related_model_data)
            # Creates a new Session instance with the provided data.
            session = Session.objects.create(
                session_type=session_type, related_model=related_model, **validated_data
            )

        else:
            # removes the related_model data from the validated data,
            # if it is presented.
            if "related_model" in validated_data:
                validated_data.pop("related_model")
            # Creates a new Session instance with the provided data.
            session = Session.objects.create(session_type=session_type, **validated_data)

        return session

    @transaction.atomic
    def update(self, instance: Session, validated_data: dict) -> Session:
        """
        Updates an existing Session instance. Handles nested updates
        of related models using the `ProviderModelConfigWriteSerializer`.
        """

        related_model = validated_data.pop("related_model", None)
        if related_model:
            # Updates ProviderModelConfig instance.
            # Using serializer to call the update method of the related model.
            related_model_serializer = ProviderModelConfigWriteSerializer(
                instance=instance.related_model, context=self.context
            )
            related_model_serializer.update(instance.related_model, related_model)
        # session type is not allowed to be updated
        if "session_type" in validated_data:
            instance.session_type = validated_data.pop("session_type")
        return super().update(instance, validated_data)

    def to_representation(self, instance) -> dict:
        """
        Converts the Session instance into a serialized representation
        using the `SessionReadSerializer`.
        """

        serializer = SessionReadSerializer(instance, context=self.context)
        return serializer.data


class SessionMessageReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading SessionMessage data, to be used by get actions.
    """

    owner = serializers.StringRelatedField()

    class Meta:
        """
        Defines the model and fields to be serialized.
        """

        model = SessionMessage
        fields = ("id", "query", "answer", "created_date", "updated_date", "owner")


class SessionMessageWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing SessionMessage data, to be used by post/patch actions.
    """

    session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Defines the model and fields to be serialized.
        """

        model = SessionMessage
        fields = ("session", "query", "answer")

    def to_representation(self, instance):
        """
        Converts the SessionMessage instance into a serialized representation
        using the `SessionMessageReadSerializer`.
        """

        serializer = SessionMessageReadSerializer(instance, context=self.context)
        return serializer.data


class GenerateRequestSerializer(serializers.Serializer):
    query = serializers.CharField()
    files = serializers.ListField(child=serializers.JSONField(), required=False)
    parameters = serializers.JSONField(required=False)
    stream = serializers.BooleanField(default=True, required=False)

    def validate(self, data):
        parameters = data.get("parameters", None)
        if parameters is not None:
            model_bundle: LLMModelBundle = self.context.get("llm_model_bundle")
            provider_model_serializer = ProviderModelConfigWriteSerializer(
                data={
                    "provider_name": model_bundle.configuration.id,
                    "model_name": model_bundle.model_schema.id,
                    "config": {"parameters": parameters},
                },
                context=self.context,
            )
            provider_model_serializer.is_valid(raise_exception=True)
            data["related_model"] = provider_model_serializer.data
        return data
