# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from gen_flow.apps.core.models import Provider


def enable_provider(team, owner, data) -> Provider:
    try:
        provider = Provider.objects.get(
            provider_name=data["provider_name"],
            team=team,
        )
    except Provider.DoesNotExist:
        provider = Provider.objects.create(team=team, owner=owner, is_valid=True, **data)
    return provider
