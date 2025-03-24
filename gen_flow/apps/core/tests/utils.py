# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from gen_flow.apps.core.models import Provider

def enable_provider(team, owner, data) -> Provider:
    provider = Provider.objects.create(
        team=team,
        owner=owner,
        **data
    )
    return provider