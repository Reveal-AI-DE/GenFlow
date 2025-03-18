# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from abc import ABC
from enum import Enum

from pydantic import BaseModel, ConfigDict


class MessageRole(Enum):
    '''
    Represents different roles for messages.
    '''

    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'

    @classmethod
    def value_of(cls, value: str) -> 'MessageRole':
        '''
        Gets the corresponding MessageRole for a given string value.
        '''

        for mode in cls:
            if mode.value == value:
                return mode
        raise ValueError(f'invalid message type value {value}')


class MessageContentType(Enum):
    '''
    Represents the types of content that a message can have.
    '''

    TEXT = 'text'


class MessageContent(BaseModel):
    '''
    Represents the content of a message.
    '''

    type: MessageContentType
    data: str

    class Config:
        # use_enum_values=True not working when setting
        # the default value for enum field because the validation does not happen.
        # validate_default=True solves the problem.
        validate_default=True
        use_enum_values = True


class TextMessageContent(MessageContent):
    '''
    Represents the content of a text message.
    '''

    type: MessageContentType = MessageContentType.TEXT


class Message(ABC, BaseModel):
    '''
    Represents a message entity with a role, content, and optional name.
    '''

    role: MessageRole
    content: str | list[MessageContent]

    class Config:
        # use_enum_values=True not working when setting
        # the default value for enum field because the validation does not happen.
        # validate_default=True solves the problem.
        validate_default=True
        use_enum_values = True

class UserMessage(Message):
    '''
    Represents a user message.
    '''

    role: MessageRole = MessageRole.USER


class AssistantMessage(Message):
    '''
    Represents an assistant message.
    '''

    role: MessageRole = MessageRole.ASSISTANT


class SystemMessage(Message):
    '''
    Represents a system message.
    '''

    role: MessageRole = MessageRole.SYSTEM
