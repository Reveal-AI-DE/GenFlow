# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from enum import Enum
from typing import Any, Optional, List
from pydantic import BaseModel, Field, model_validator


class TranslationEntity(BaseModel):
    '''
    Represents a translation object with the following attributes:
    '''

    en_US: str = Field(..., description='Required key for English (US) translation')

    class Config:
        # Allows extra attributes to be included in the model.
        extra = 'allow'

    @model_validator(mode='before')
    def check_en_us(cls, values):
        '''
        Validates that the 'en_US' key is present in the input values.
        Raises:
            ValueError: If the 'en_US' key is not present.
        '''

        if 'en_US' not in values:
            raise ValueError('The \'en_US\' key is required.')
        return values

    @model_validator(mode='before')
    def ensure_extra_attributes_are_strings(cls, values):
        '''
        Ensures that all extra attributes (keys other than 'en_US') are strings.
        Raises:
            TypeError: If any extra attribute value is not a string.
        '''

        for key, value in values.items():
            if key != 'en_US' and not isinstance(value, str):
                raise TypeError(f'The value for \'{key}\' must be a string.')
        return values

    def __init__(self, **data):
        super().__init__(**data)


class BaseYamlEntity(BaseModel):
    '''
    Represents a base entity for YAML configuration with a label and an optional description.
    '''

    label: TranslationEntity
    description: Optional[TranslationEntity] = None


class BaseYamlEntityWithIcons(BaseYamlEntity):
    '''
    Subclass of BaseYamlEntity that includes additional attributes for small and large icons.
    '''

    icon_small: Optional[TranslationEntity] = None
    icon_large: Optional[TranslationEntity] = None


class HelpEntity(BaseModel):
    '''
    Model class for help.
    '''

    title: TranslationEntity
    url: Optional[TranslationEntity] = None


class SelectOptionType(Enum):
    '''
    Enum class representing the type of select options.
    '''

    STRING = 'string'
    OBJECT = 'object'


class SelectOption(BaseModel):
    '''
    Represents an option in a selection list.
    '''

    name: str
    label: TranslationEntity
    type: SelectOptionType
    help: Optional[TranslationEntity] = None
    parameters: Optional[List['ConfigurationEntity']] = None
    disabled: Optional[bool] = False


class ConfigurationType(Enum):
    '''
    Enum class for configuration parameter type.
    '''

    FLOAT = 'float'
    INT = 'int'
    STRING = 'string'
    BOOLEAN = 'boolean'
    TEXT = 'text'
    OBJECT = 'object'
    SECRET = 'secret'


class CommonConfigurationEntity(BaseModel):
    name: str
    label: TranslationEntity
    type: ConfigurationType
    required: Optional[bool] = False
    disabled: Optional[bool] = False
    advanced: Optional[bool] = False


class ConfigurationEntity(CommonConfigurationEntity):
    '''
    Represents a configuration parameter.
    '''

    use_template: Optional[str] = None
    help: Optional[TranslationEntity] = None
    placeholder: Optional[TranslationEntity] = None
    default: Optional[Any] = None
    min: Optional[float] = None
    max: Optional[float] = None
    precision: Optional[int] = None

    # options for selectors, it can also be used to generate forms
    # if it has parameters attribute
    options: Optional[list[SelectOption]] = None

    # used to generate nested forms
    parameters: Optional[List['ConfigurationEntity']] = None


class FileEntity(BaseModel):
    '''
    Represents an uploaded file.
    '''

    id: str
    path: str
