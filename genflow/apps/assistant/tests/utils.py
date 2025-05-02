# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.contrib.auth.models import User

from genflow.apps.assistant.models import Assistant
from genflow.apps.core.models import EntityGroup
from genflow.apps.team.models import Team

ASSISTANT_GROUP_DATA = {
    "name": "dummy",
    "description": "dummy",
    "color": "dummy",
}


ASSISTANT_DATA = {
    "name": "dummy",
    "description": "dummy",
    "pre_prompt": "dummy",
    "related_model": {
        "provider_name": "dummy",
        "model_name": "model2",
    },
}


def create_dummy_assistant_group(team: Team, owner: User, data: dict) -> EntityGroup:
    prompt_group = EntityGroup.objects.create(
        team=team, owner=owner, entity_type=Assistant.__name__.lower(), **data
    )
    return prompt_group


def create_dummy_assistant(team: Team, owner: User, data: dict) -> Assistant:
    prompt_group = create_dummy_assistant_group(team=team, owner=owner, data=ASSISTANT_GROUP_DATA)
    prompt = Assistant.objects.create(team=team, owner=owner, group=prompt_group, **data)
    return prompt
