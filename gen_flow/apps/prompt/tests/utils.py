# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.contrib.auth.models import User

from gen_flow.apps.core.models import EntityGroup
from gen_flow.apps.prompt.models import Prompt
from gen_flow.apps.team.models import Team

PROMPT_GROUP_DATA = {
    "name": "dummy",
    "description": "dummy",
    "color": "dummy",
}


PROMPT_DATA = {
    "name": "dummy",
    "description": "dummy",
    "pre_prompt": "dummy",
    "related_model": {
        "provider_name": "dummy",
        "model_name": "model2",
    },
}


PROVIDER_DATA = {"provider_name": "dummy", "encrypted_config": {"api_key": "test"}}


def create_dummy_prompt_group(team: Team, owner: User, data: dict) -> EntityGroup:
    prompt_group = EntityGroup.objects.create(
        team=team, owner=owner, entity_type=Prompt.__name__.lower(), **data
    )
    return prompt_group


def create_dummy_prompt(team: Team, owner: User, data: dict) -> Prompt:
    prompt_group = create_dummy_prompt_group(team=team, owner=owner, data=PROMPT_GROUP_DATA)
    prompt = Prompt.objects.create(team=team, owner=owner, group=prompt_group, **data)
    return prompt
