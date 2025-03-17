# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
from os import path as osp

from django.conf import settings

from gen_flow.apps.ai.base.ai_provider import AIProvider
from gen_flow.apps.ai.base.model_collection import ModelCollection

class DummyAIProvider(AIProvider):
    '''
    Dummy AI provider class.
    '''

    PROVIDER_FOLDER = 'dummy_provider'

    def validate_credentials(self, credentials: dict) -> None:
        '''
        Validate provider credentials
        '''
        pass

class DummyModelCollection(ModelCollection):
    '''
    Dummy Model Collection class.
    '''


def create_dummy_model_config():
    src_path = osp.join(osp.dirname(__file__), 'assets')
    dist_path = settings.MODEL_CONFIG_ROOT
    os.makedirs(dist_path, exist_ok=True)
    os.system(f'cp -r {src_path}/* {dist_path}')
