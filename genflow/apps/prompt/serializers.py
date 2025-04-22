# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import os

from django.db import transaction
from rest_framework import serializers

from genflow.apps.core.models import EntityGroup, ProviderModelConfig
from genflow.apps.core.serializers import (
    EntityGroupReadSerializer,
    ProviderModelConfigReadSerializer,
    ProviderModelConfigWriteSerializer,
)
from genflow.apps.prompt.models import Prompt


class PromptReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Prompt data, to be used by get actions.
    """

    related_model = ProviderModelConfigReadSerializer()
    group = EntityGroupReadSerializer()
    related_test_session = serializers.SerializerMethodField()

    def get_related_test_session(self, obj: Prompt) -> int:
        """
        Returns the related test session for the given Prompt instance.
        """

        if hasattr(obj, "related_test_session"):
            return obj.related_test_session
        return None

    class Meta:
        """
        Defines the model and fields to be serialized.
        """

        model = Prompt
        fields = [
            "id",
            "name",
            "description",
            "pre_prompt",
            "is_pinned",
            "suggested_questions",
            "prompt_type",
            "prompt_status",
            "related_model",
            "group",
            "group_id",
            "avatar",
            "related_test_session",
        ]


class PromptWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing Prompt data, to be used by post/patch actions.
    """

    related_model = ProviderModelConfigWriteSerializer()
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=EntityGroup.objects.none(), source="group"  # Default to none
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "iam_context"):
            team = request.iam_context.team
            if team:
                # Filter queryset based on the iam_context
                self.fields["group_id"].queryset = EntityGroup.objects.filter(
                    entity_type=self.Meta.model.__name__.lower(), team=team
                )

    class Meta:
        model = Prompt
        fields = [
            "name",
            "description",
            "pre_prompt",
            "suggested_questions",
            "is_pinned",
            "prompt_type",
            "prompt_status",
            "related_model",
            "group_id",
        ]

    @transaction.atomic
    def create(self, validated_data: dict) -> Prompt:
        """
        Creates and returns a new Prompt instance along with its related model and media directory.
        """

        related_model = validated_data.pop("related_model")
        group = validated_data.pop("group")
        # Creates a new ProviderModelConfig instance using the 'related_model' data.
        related_model = ProviderModelConfig.objects.create(**related_model)
        # Creates a new Prompt instance with the provided data.
        prompt = Prompt.objects.create(related_model=related_model, group=group, **validated_data)
        # Ensures the media directory for the Prompt instance exists by creating it if necessary.
        os.makedirs(prompt.media_dir(), exist_ok=True)
        return prompt

    @transaction.atomic
    def update(self, instance: Prompt, validated_data: dict) -> Prompt:
        """
        Updates the instance with the provided validated data.

        If the `related_model` key is present in the validated data, it updates
        the related model using the `ProviderModelConfigWriteSerializer`.
        """

        related_model = validated_data.pop("related_model", None)
        if related_model:
            related_model_serializer = ProviderModelConfigWriteSerializer(
                instance=instance.related_model, context=self.context
            )
            related_model_serializer.update(instance.related_model, related_model)
        return super().update(instance, validated_data)

    def to_representation(self, instance: Prompt) -> dict:
        """
        Converts the given instance into its serialized representation.
        """

        serializer = PromptReadSerializer(instance, context=self.context)
        return serializer.data
