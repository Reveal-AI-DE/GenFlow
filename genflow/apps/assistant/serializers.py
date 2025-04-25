# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import os

from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from genflow.apps.assistant.models import Assistant
from genflow.apps.core.serializers import (
    EntityBaseWriteSerializer,
    EntityGroupReadSerializer,
    FileEntitySerializer,
    ProviderModelConfigReadSerializer,
    common_entity_read_fields,
    common_entity_write_fields,
)
from genflow.apps.prompt.serializers import common_prompt_read_fields, common_prompt_write_fields


class AssistantReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Assistant data, to be used by get actions.
    """

    related_model = ProviderModelConfigReadSerializer()
    group = EntityGroupReadSerializer()
    files = serializers.SerializerMethodField()

    @extend_schema_field(FileEntitySerializer(many=True))
    def get_files(self, instance: Assistant):
        """
        Returns a list of files associated with the Assistant instance.
        """

        if not instance.files:
            return []

        return [file.model_dump() for file in instance.files]

    class Meta:
        """
        Defines the model and fields to be serialized.
        """

        model = Assistant
        # Dynamically includes fields from `CommonEntity` and `CommonPrompt` using precomputed lists.
        fields = (
            common_entity_read_fields
            + common_prompt_read_fields
            + [
                "id",
                "opening_statement",
                "context_source",
                "collection_config",
                "assistant_status",
                "related_model",
                "group",
                "files",
            ]
        )


class AssistantWriteSerializer(EntityBaseWriteSerializer):
    """
    Serializer for writing Assistant data, to be used by post/patch actions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Assistant
        fields = (
            common_entity_write_fields
            + common_prompt_write_fields
            + [
                "opening_statement",
                "context_source",
                "collection_config",
                "assistant_status",
                "related_model",
                "group_id",
            ]
        )

    @transaction.atomic
    def create(self, validated_data: dict) -> Assistant:
        """
        Creates and returns a new Assistant instance along with its related model and media directory.
        """

        group, related_model = super().create(validated_data)
        # Creates a new Assistant instance with the provided data.
        assistant = Assistant.objects.create(
            related_model=related_model, group=group, **validated_data
        )
        # Ensures the media directory for the Assistant instance exists by creating it if necessary.
        os.makedirs(assistant.media_dir(), exist_ok=True)
        return assistant

    @transaction.atomic
    def update(self, instance: Assistant, validated_data: dict) -> Assistant:
        """
        Updates the instance with the provided validated data.
        """

        return super().update(instance, validated_data)

    def to_representation(self, instance: Assistant) -> dict:
        """
        Converts the given instance into its serialized representation.
        """

        serializer = AssistantReadSerializer(instance, context=self.context)
        return serializer.data
