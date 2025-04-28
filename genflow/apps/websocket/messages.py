# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from enum import Enum
from typing import Any, Mapping

from pydantic import BaseModel


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
