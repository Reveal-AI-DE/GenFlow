# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional

from pydantic import BaseModel

class LimitDefinition(BaseModel):
    """
    Represents a limit definition for a specific app.
    """

    key: str
    description: str
    default: Optional[int] = None

LIMIT_REGISTRY = {}

def register_limit(app_name, key, description, default=None):
    """
    Register a limit definition for a specific app.
    """

    if app_name not in LIMIT_REGISTRY:
        LIMIT_REGISTRY[app_name] = []
    LIMIT_REGISTRY[app_name].append(LimitDefinition(key=key, description=description, default=default))

def get_limit_description(key):
    """
    Retrieve the description for a given key from the registry.
    """

    for app_limits in LIMIT_REGISTRY.values():
        for limit in app_limits:
            if limit.key == key:
                return limit.description
    return None
