# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

from django.conf import settings
from django.db import models
from django.utils.text import get_valid_filename

from genflow.apps.common.models import TeamAssociatedModel, TimeAuditModel, UserOwnedModel
from genflow.apps.core.models import AIAssociatedEntity, CommonEntity


def get_prompt_media_path(instance: "Prompt", filename: str) -> str:
    """
    Generates a relative file path for storing media files associated with a Prompt instance.
    """

    filename = get_valid_filename(filename)
    absolute_path = osp.join(settings.PROMPTS_MEDIA_ROOT, str(instance.id), filename)
    relative_path = osp.relpath(absolute_path, settings.MEDIA_ROOT)
    return relative_path


class PromptType(models.TextChoices):
    """
    An enumeration of text choices representing different types of prompts.
    """

    SIMPLE = "simple"
    ADVANCED = "advanced"


class PromptStatus(models.TextChoices):
    """
    An enumeration of text choices representing prompt status.
    """

    DRAFTED = "drafted"
    PUBLISHED = "published"


class CommonPrompt(models.Model):
    """
    Abstract base model for prompts common fields.

    Attributes:
        pre_prompt (models.TextField): The text content of the pre-prompt.
        suggested_questions (models.JSONField): A JSON field to store suggested questions, can be null.
        prompt_type (models.CharField): The type of the prompt, with choices defined in `PromptType`
            and a default value of `PromptType.SIMPLE`.

    Meta:
        abstract (bool): Indicates that this is an abstract model and will not be used to create any database table.
    """

    pre_prompt = models.TextField()
    suggested_questions = models.JSONField(null=True)
    prompt_type = models.CharField(
        max_length=10, choices=PromptType.choices, default=PromptType.SIMPLE
    )

    class Meta:
        abstract = True


class Prompt(
    CommonEntity,
    CommonPrompt,
    AIAssociatedEntity,
    TimeAuditModel,
    UserOwnedModel,
    TeamAssociatedModel,
):
    """
    Represents a Prompt entity with various attributes and relationships.

    Attributes:
        prompt_status (str): The status of the prompt, with choices defined in `PromptStatus`. Defaults to `PromptStatus.DRAFTED`.
        avatar (ImageField, optional): An image associated with the prompt, uploaded to a specific media path. Can be null or blank.
        related_test_session (int, optional): An integer field representing a related test session. Can be null.
    """

    prompt_status = models.CharField(
        max_length=10, choices=PromptStatus.choices, default=PromptStatus.DRAFTED
    )
    avatar = models.ImageField(upload_to=get_prompt_media_path, null=True, blank=True)
    related_test_session = models.IntegerField(null=True)

    def media_dir(self) -> str:
        """
        Returns the directory path for storing media files related to the prompt.
        """

        return osp.join(settings.PROMPTS_MEDIA_ROOT, str(self.id))

    def __str__(self) -> str:
        """
        Returns the string representation of the prompt, which is its name.
        """

        return self.name
