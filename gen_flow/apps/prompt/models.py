# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

from django.db import models
from django.conf import settings
from django.utils.text import get_valid_filename

from gen_flow.apps.common.models import TimeAuditModel, UserOwnedModel, TeamAssociatedModel
from gen_flow.apps.core.models import ProviderModelConfig


def get_prompt_media_path(instance: 'Prompt', filename: str) -> str:
    '''
    Generates a relative file path for storing media files associated with a Prompt instance.
    '''

    filename = get_valid_filename(filename)
    absolute_path = osp.join(settings.PROMPTS_MEDIA_ROOT, str(instance.id), filename)
    relative_path = osp.relpath(absolute_path, settings.MEDIA_ROOT)
    return relative_path


class PromptType(models.TextChoices):
    '''
    An enumeration of text choices representing different types of prompts.
    '''

    SIMPLE = 'simple'
    ADVANCED = 'advanced'


class PromptStatus(models.TextChoices):
    '''
    An enumeration of text choices representing prompt status.
    '''

    DRAFTED = 'drafted'
    PUBLISHED = 'published'


class PromptGroup(TimeAuditModel, UserOwnedModel, TeamAssociatedModel):
    '''
    Represents a group of prompts with associated metadata.

    Attributes:
        name (str): The name of the prompt group, limited to 255 characters.
        description (str): A detailed description of the prompt group.
        color (str): A color code associated with the prompt group, stored as a string with a maximum length of 9 characters.
    '''

    name = models.CharField(max_length=255)
    description = models.TextField()
    color = models.CharField(max_length=9)

    def __str__(self) -> str:
        '''
        Returns the name of the prompt group as its string representation.
        '''

        return self.name


class Prompt(TimeAuditModel, UserOwnedModel, TeamAssociatedModel):
    '''
    Represents a Prompt entity with various attributes and relationships.

    Attributes:
        name (str): The name of the prompt, limited to 255 characters.
        description (str): A detailed description of the prompt.
        pre_prompt (str): Text that serves as a pre-prompt for the main content.
        suggested_questions (dict, optional): JSON field containing suggested questions related to the prompt.
        type (str): The type of the prompt, with choices defined in `PromptType`. Defaults to `PromptType.SIMPLE`.
        status (str): The status of the prompt, with choices defined in `PromptStatus`. Defaults to `PromptStatus.DRAFTED`.
        avatar (ImageField, optional): An image associated with the prompt, uploaded to a specific media path. Can be null or blank.
        group (ForeignKey): A foreign key linking the prompt to a `PromptGroup`. Cannot be null.
        related_model (OneToOneField, optional): A one-to-one relationship with `ProviderModelConfig`. Can be null.
        related_test_session (int, optional): An integer field representing a related test session. Can be null.
        is_pinned (bool): A boolean indicating whether the prompt is pinned. Defaults to `False`.
    '''

    name = models.CharField(max_length=255)
    description = models.TextField()
    pre_prompt = models.TextField()
    suggested_questions = models.JSONField(null=True)
    type = models.CharField(max_length=10, choices=PromptType.choices, default=PromptType.SIMPLE)
    status = models.CharField(max_length=10, choices=PromptStatus.choices, default=PromptStatus.DRAFTED)
    avatar = models.ImageField(upload_to=get_prompt_media_path, null=True, blank=True)
    group = models.ForeignKey(PromptGroup, null=False, on_delete=models.CASCADE)
    related_model = models.OneToOneField(ProviderModelConfig, null=True, on_delete=models.CASCADE)
    related_test_session = models.IntegerField(null=True)
    is_pinned = models.BooleanField(default=False)

    def media_dir(self) -> str:
        '''
        Returns the directory path for storing media files related to the prompt.
        '''

        return osp.join(settings.PROMPTS_MEDIA_ROOT, str(self.id))

    def __str__(self) -> str:
        '''
        Returns the string representation of the prompt, which is its name.
        '''

        return self.name
