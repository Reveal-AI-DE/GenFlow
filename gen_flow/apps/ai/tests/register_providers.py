# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from gen_flow.apps.ai.providers.registry import register_ai_provider, register_model_collection
from gen_flow.apps.ai.tests.utils import create_dummy_model_config, DummyAIProvider, DummyLLMModelCollection


create_dummy_model_config()

@register_ai_provider('dummy_provider')
class RegisteredDummyAIProvider(DummyAIProvider):
    pass

@register_model_collection('dummy_provider', 'llm')
class RegisteredDummyLLMModelCollection(DummyLLMModelCollection):
    pass
