# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.contrib.auth.models import User

from gen_flow.apps.team.models import Team
from gen_flow.apps.core.models import ProviderModelConfig
from gen_flow.apps.prompt.models import Prompt
from gen_flow.apps.prompt.tests.utils import create_prompt, PROMPT_DATA
from gen_flow.apps.session.models import SessionType, SessionMode, Session, SessionMessage


SESSION_DATA = {
    'name': 'Test Session',
    'session_type': SessionType.LLM.value,
    'session_mode': SessionMode.CHAT.value,
    'related_model': {
        'provider_name': 'dummy',
        'model_name': 'model2',
    },
}


SESSION_MESSAGE_DATA = [
    {
        'query': 'Test Message 1',
    },
    {
        'query': 'Test Message 2',
    },
]


def create_dummy_prompt(team: Team, owner: User) -> Prompt:
    prompt_data = PROMPT_DATA.copy()
    del prompt_data['related_model']
    prompt = create_prompt(
        team=team,
        owner=owner,
        data=prompt_data
    )
    return prompt

def create_dummy_session(
        team: Team,
        owner: User,
        data: dict
    ) -> Session:
    session = None
    if data['session_type'] == SessionType.PROMPT.value:
        prompt = create_dummy_prompt(team=team, owner=owner)
        if 'related_model' in data:
            del data['related_model']
        session = Session.objects.create(
            team=team,
            owner=owner,
            related_prompt=prompt,
            **data
        )
    if data['session_type'] == SessionType.LLM.value:
        provider_model_config = ProviderModelConfig.objects.create(**data['related_model'])
        del data['related_model']
        session = Session.objects.create(
            team=team,
            owner=owner,
            related_model=provider_model_config,
            **data
        )
    return session

def create_dummy_session_message(
        team: Team,
        owner: User,
        session: Session,
        data: dict
    ) -> SessionMessage:
    session_message = SessionMessage.objects.create(
        team=team,
        owner=owner,
        session=session,
        **data
    )
    return session_message
