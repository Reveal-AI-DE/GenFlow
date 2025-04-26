# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT


from genflow.apps.restriction.models import Limit
from genflow.apps.restriction.registry import LIMIT_REGISTRY, LimitDefinition


def add_global_limits(app_name: str):
    """
    Adds global limits corresponding to app_name.
    """

    limits: LimitDefinition = LIMIT_REGISTRY.get(app_name, [])
    for limit in limits:
        if limit.default is not None:
            Limit.objects.get_or_create(
                key=limit.key,
                value=limit.default,
            )
