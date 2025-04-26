# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from genflow.apps.restriction.models import Limit


def override_limit(key: str, value: int, user=None, team=None) -> None:
    """
    Override the default limit for testing purposes.
    """

    Limit.objects.filter(key=key, user=user, team=team).update(value=value)
