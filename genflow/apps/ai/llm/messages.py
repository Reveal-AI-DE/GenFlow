# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from abc import ABC
from enum import Enum
from typing import Optional, cast

from pydantic import BaseModel, field_serializer


class MessageRole(Enum):
    """
    Represents different roles for messages.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    @classmethod
    def value_of(cls, value: str) -> "MessageRole":
        """
        Gets the corresponding MessageRole for a given string value.
        """

        for mode in cls:
            if mode.value == value:
                return mode
        raise ValueError(f"invalid message type value {value}")


class MessageContentType(Enum):
    """
    Represents the types of content that a message can have.
    """

    TEXT = "text"


class MessageContent(BaseModel):
    """
    Represents the content of a message.
    """

    type: MessageContentType
    data: str

    @field_serializer("type")
    def get_type_value(
        self,
        _type: MessageContentType,
    ) -> str:
        return str(_type.value)


class TextMessageContent(MessageContent):
    """
    Represents the content of a text message.
    """

    type: MessageContentType = MessageContentType.TEXT


class Message(ABC, BaseModel):
    """
    Represents a message entity with a role, content, and optional name.
    """

    role: MessageRole
    content: str | list[MessageContent]
    name: Optional[str] = None

    @field_serializer("role")
    def get_type_value(
        self,
        role: MessageRole,
    ) -> str:
        return str(role.value)

    def to_dict(self) -> dict:
        """
        Dumps the model to a dictionary.
        """

        data = self.model_dump(exclude={"name"})

        if self.name:
            data["name"] = self.name

        return data


class UserMessage(Message):
    """
    Represents a user message.
    """

    role: MessageRole = MessageRole.USER

    @field_serializer("content")
    def get_content_value(
        self,
        content: str | list[MessageContent],
    ) -> str | list[dict]:
        if isinstance(content, str):
            return content
        else:
            data = []
            for item in content:
                if item.type == MessageContentType.TEXT:
                    item = cast(TextMessageContent, item)
                    data.append({"type": "text", "text": item.data})
                else:
                    # TODO: add support for other content types
                    raise ValueError(f"invalid content type {item.type}")
            return data


class AssistantMessage(Message):
    """
    Represents an assistant message.
    """

    role: MessageRole = MessageRole.ASSISTANT


class SystemMessage(Message):
    """
    Represents a system message.
    """

    role: MessageRole = MessageRole.SYSTEM
