# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import os

from django.db import transaction
from rest_framework import serializers

from genflow.apps.core.serializers import (
    EntityGroupReadSerializer,
    ProviderModelConfigReadSerializer,
    EntityBaseWriteSerializer,
    common_entity_read_fields,
    common_entity_write_fields,
)
from genflow.apps.prompt.models import CommonPrompt, Prompt

# Precompute the read and write fields for CommonPrompt
common_prompt_read_fields = [
    field.name for field in CommonPrompt._meta.get_fields()
]
common_prompt_write_fields = [
    field.name for field in CommonPrompt._meta.get_fields()
]

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
        # Dynamically includes fields from `CommonEntity` and `CommonPrompt` using precomputed lists.
        fields = common_entity_read_fields + common_prompt_read_fields + [
            "id",
            "prompt_status",
            "related_model",
            "group",
            "related_test_session",
        ]


class PromptWriteSerializer(EntityBaseWriteSerializer):
    """
    Serializer for writing Prompt data, to be used by post/patch actions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Prompt
        fields = common_entity_write_fields + common_prompt_write_fields + [
            "prompt_status",
            "related_model",
            "group_id",
        ]

    @transaction.atomic
    def create(self, validated_data: dict) -> Prompt:
        """
        Creates and returns a new Prompt instance along with its related model and media directory.
        """

        group, related_model = super().create(validated_data)
        prompt = Prompt.objects.create(related_model=related_model, group=group, **validated_data)
        # Ensures the media directory for the Prompt instance exists by creating it if necessary.
        os.makedirs(prompt.media_dir(), exist_ok=True)
        return prompt

    @transaction.atomic
    def update(self, instance: Prompt, validated_data: dict) -> Prompt:
        """
        Updates the instance with the provided validated data.
        """

        return super().update(instance, validated_data)

    def to_representation(self, instance: Prompt) -> dict:
        """
        Converts the given instance into its serialized representation.
        """

        serializer = PromptReadSerializer(instance, context=self.context)
        return serializer.data
