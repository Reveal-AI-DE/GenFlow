# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import os

from gen_flow.apps.ai.ai_provider_factory import AIProviderFactory

if 'test' not in os.getenv('DJANGO_SETTINGS_MODULE', ''):
    ai_provider_factory = AIProviderFactory()
