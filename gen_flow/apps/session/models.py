# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

from django.db import models
from django.conf import settings

from gen_flow.apps.common.models import TimeAuditModel, UserOwnedModel, TeamAssociatedModel
from gen_flow.apps.core.models import ProviderModelConfig
from gen_flow.apps.prompt.models import Prompt


class SessionMode(models.TextChoices):
    '''
    An enumeration of text choices representing different modes of a session.
    '''

    CHAT = 'chat'
    COMPLETION = 'completion'


class SessionType(models.TextChoices):
    '''
    An enumeration of text choices representing different types of a session.
    '''

    LLM = 'llm'
    PROMPT = 'prompt'


class Session(TimeAuditModel, UserOwnedModel, TeamAssociatedModel):
    '''
    Represents a session entity with associated metadata and relationships.

    Attributes:
        name (str): The name of the session. This field is required and has a maximum length
            of 255 characters.
        type (str): The type of the session, chosen from predefined `SessionType` choices.
            Defaults to `SessionType.LLM`.
        mode (str): The mode of the session, chosen from predefined `SessionMode` choices.
            Defaults to `SessionMode.CHAT`.
        related_model (ProviderModelConfig): A one-to-one relationship with `ProviderModelConfig`.
            Can be null, and if deleted, the reference is set to null.
        related_prompt (Prompt): A foreign key relationship with `Prompt`. Can be null, and if
            deleted, the reference is set to null.
    '''

    name = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=10, choices=SessionType.choices, default=SessionType.LLM)
    mode = models.CharField(max_length=10, choices=SessionMode.choices, default=SessionMode.CHAT)
    related_model = models.OneToOneField(ProviderModelConfig, null=True, on_delete=models.SET_NULL)
    related_prompt = models.ForeignKey(Prompt, null=True, on_delete=models.SET_NULL)

    @property
    def dirname(self):
        '''
        The relative directory path for the session, constructed using the session's ID and settings.
        '''

        full_path = osp.join(settings.SESSIONS_ROOT, str(self.id))
        return osp.relpath(full_path, settings.BASE_DIR)
