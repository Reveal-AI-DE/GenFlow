# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

from django.conf import settings
from django.db import models
from django.utils.functional import SimpleLazyObject
from django.utils.text import get_valid_filename
from llama_index.core import SimpleDirectoryReader

from genflow.apps.common.file_utils import get_files
from genflow.apps.common.models import TeamAssociatedModel, TimeAuditModel, UserOwnedModel
from genflow.apps.core.models import AIAssociatedEntity, CommonEntity
from genflow.apps.prompt.models import CommonPrompt


def get_assistant_media_path(instance: "Assistant", filename: str) -> str:
    """
    Generates a relative file path for storing media files associated with a Assistant instance.
    """

    filename = get_valid_filename(filename)
    absolute_path = osp.join(settings.ASSISTANT_MEDIA_ROOT, str(instance.id), filename)
    relative_path = osp.relpath(absolute_path, settings.MEDIA_ROOT)
    return relative_path


class AssistantStatus(models.TextChoices):
    """
    An enumeration of text choices representing assistant status.
    """

    DRAFTED = "drafted"
    PUBLISHED = "published"


class AssistantContextSource(models.TextChoices):
    """
    An enumeration of text choices representing context source of the assistant.
    """

    FILES = "files"
    COLLECTIONS = "collections"


class Assistant(
    CommonEntity,
    CommonPrompt,
    AIAssociatedEntity,
    TeamAssociatedModel,
    UserOwnedModel,
    TimeAuditModel,
):
    """
    Represents an AI assistant entity with various attributes and methods to manage its configuration.

    Attributes:
        opening_statement (TextField): An optional opening statement for the assistant.
        context_source (CharField): The source of context for the assistant, with choices
            defined in `AssistantContextSource`. Defaults to `AssistantContextSource.FILES`.
        collection_config (JSONField): An optional JSON field for storing assistant-specific
            configuration details.
        assistant_status (CharField): The current status of the assistant, with choices
            defined in `AssistantStatus`. Defaults to `AssistantStatus.DRAFTED`.
        avatar (ImageField): An optional image field for storing the assistant's avatar,
            uploaded to a specific media path.
    """

    opening_statement = models.TextField(null=True)
    context_source = models.CharField(
        max_length=25, choices=AssistantContextSource.choices, default=AssistantContextSource.FILES
    )
    collection_config = models.JSONField(null=True)
    assistant_status = models.CharField(
        max_length=10, choices=AssistantStatus.choices, default=AssistantStatus.DRAFTED
    )
    avatar = models.ImageField(upload_to=get_assistant_media_path, null=True, blank=True)

    @property
    def dirname(self):
        """
        Returns the directory path for storing files related to the assistant when the
        context source is `AssistantContextSource.FILES`.
        """

        full_path = osp.join(settings.ASSISTANTS_ROOT, str(self.id))
        return osp.relpath(full_path, settings.BASE_DIR)

    @property
    def files(self):
        """
        Lazily loads and returns the files associated with the
            assistant's directory.
        """

        return SimpleLazyObject(lambda: get_files(self.dirname))

    def get_files_context(self) -> str:
        """
        Retrieves the combined content of all files in a specified directory.

        it uses `SimpleDirectoryReader` to load all files in the
        directory and concatenates their content into a single string.
        """

        context = ""
        if osp.exists(self.dirname):
            documents = SimpleDirectoryReader(self.dirname).load_data()
            context = " ".join([document.get_content() for document in documents])
        return context

    def media_dir(self) -> str:
        """
        Returns the directory path for storing media files related to the assistant.
        """

        return osp.join(settings.ASSISTANT_MEDIA_ROOT, str(self.id))

    def __str__(self) -> str:
        """
        Returns the string representation of the assistant, which is its name.
        """

        return self.name
