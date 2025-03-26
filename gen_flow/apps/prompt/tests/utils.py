# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.contrib.auth.models import User

from gen_flow.apps.team.models import Team
from gen_flow.apps.prompt.models import PromptGroup, Prompt

def create_prompt_group(team: Team, owner: User, data: dict) -> PromptGroup:
    prompt_group = PromptGroup.objects.create(
        team=team,
        owner=owner,
        **data
    )
    return prompt_group

def create_prompt(team: Team, owner: User, data: dict) -> Prompt:
    prompt = Prompt.objects.create(
        team=team,
        owner=owner,
        **data
    )
    return prompt
