# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from geniflow.apps.ai.providers.registry import register_ai_provider, register_model_collection
from geniflow.apps.ai.tests.utils import (
    DummyAIProvider,
    DummyLLMModelCollection,
    create_dummy_model_config,
)

create_dummy_model_config()


@register_ai_provider("dummy")
class RegisteredDummyAIProvider(DummyAIProvider):
    pass


@register_model_collection("dummy", "llm")
class RegisteredDummyLLMModelCollection(DummyLLMModelCollection):
    pass
