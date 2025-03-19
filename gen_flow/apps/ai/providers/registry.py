# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
from os import path as osp
from typing import Optional, OrderedDict

from django.conf import settings
from pydantic import BaseModel, ConfigDict

from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.base.ai_provider import AIProvider


class AIProviderExtension(BaseModel):
    '''
    Represents an extension for an AI provider.
    '''

    ai_provider_instance: AIProvider
    name: str
    order: Optional[int] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

# An ordered dictionary that stores registered AI providers.
AI_PROVIDERS: OrderedDict[str, AIProviderExtension] = OrderedDict()


def register_ai_provider(name: str):
    def wrapper(cls):
        '''
        A decorator to register an AI provider.

        Raises:
            FileNotFoundError: If the configuration file for the AI provider is not found.
        Returns:
            function: A wrapper function that registers the AI provider.
        '''

        config_path = osp.join(settings.MODEL_CONFIG_ROOT, name)
        if osp.exists(config_path) and osp.exists(osp.join(config_path, f'{name}.yaml')):
            assert name not in AI_PROVIDERS, 'AI Provider \'%s\' already registered' % name
            ai_provider_instance = cls()
            ai_provider_instance.config_path = config_path
            ai_provider_extension = AIProviderExtension(
                name=name,
                ai_provider_instance=ai_provider_instance,
                order=len(AI_PROVIDERS) - 1
            )
            AI_PROVIDERS[name] = ai_provider_extension
        else:
            raise FileNotFoundError(f'AI Provider \'{name}\' config not found')

    return wrapper


def register_model_collection(ai_provider: str, model_type_str: str):
    def wrapper(cls):
        '''
        A decorator to register a model collection for a specific AI provider.

        Raises:
            AssertionError: If the AI provider is not registered or the model type is not supported.
        Returns:
            function: A wrapper function that registers the model collection.
        '''
        assert ai_provider in AI_PROVIDERS, 'AI Provider \'%s\' not registered' % ai_provider
        ai_provider_instance: AIProvider = AI_PROVIDERS[ai_provider].ai_provider_instance

        assert model_type_str in ModelType.values(), 'Model type \'%s\' not supported' % model_type_str

        model_type_name = model_type_str.replace('-', '_')
        config_path = osp.join(ai_provider_instance.config_path, model_type_name)
        if osp.exists(config_path):
            ai_provider_instance.add_model_collection_instance(config_path, model_cls=cls)

    return wrapper

if 'test' not in os.getenv('DJANGO_SETTINGS_MODULE', ''):
    # register AI providers
    pass
