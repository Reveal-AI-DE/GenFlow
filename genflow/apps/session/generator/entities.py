# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from enum import Enum
from typing import Any, Callable, List, Mapping, Optional

from pydantic import BaseModel, ConfigDict

from genflow.apps.common.entities import FileEntity
from genflow.apps.core.config.llm_model_bundle import LLMModelBundle
from genflow.apps.session.models import Session
from genflow.apps.session.transform.base import PromptTemplateEntity


class GenerateRequest(BaseModel):
    """
    Represents a user request to call LLM model and generate text response.
    """

    query: str
    files: Optional[List[FileEntity]] = None
    parameters: Optional[Mapping[str, Any]] = None
    user_id: Optional[str] = None
    callback: Optional[Callable] = None
    stream: Optional[bool] = None


class GenerateEntity(BaseModel):
    """
    Represents an entity to handle user request to call LLM model.
    """

    db_session: Session
    llm_model_bundle: LLMModelBundle
    prompt_entity: Optional[PromptTemplateEntity] = None
    stream: bool

    # pydantic configs
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())


class ChatResponseType(str, Enum):
    """
    Defines the types of chat response
    that can be generated in the application.

    Attributes:
        CHUNK (str): Represents a chunk of a larger message.
        MESSAGE (str): Represents a complete message.
        ERROR (str): Represents an error message.
    """

    CHUNK = "chunk"
    MESSAGE = "message"
    ERROR = "error"


class ChatResponse(BaseModel):
    """
    Represents a chat response with a specific type and associated data.

    Attributes:
        type (ChatMessageTypes): The type of the chat message.
        data (str | Mapping[str, Any]): The content of the message, which can either be a string
            or a mapping of key-value pairs containing additional information.
    """

    type: ChatResponseType
    data: str | Mapping[str, Any]
