# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from asgiref.sync import sync_to_async

from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.test import override_settings

from gen_flow.apps.team.tests.utils import create_dummy_users
from gen_flow.apps.session.models import SessionType
from gen_flow.apps.session.tests.utils import create_dummy_session, SESSION_DATA
from gen_flow.apps.websocket.consumer import status
from gen_flow.apps.websocket.tests.utils import application


@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
class ChatGenerateConsumerConnectTestCase(TransactionTestCase):
    async def test_connect_invalid_subprotocols(self):
        subprotocols = ['json', 2, '3']
        communicator = WebsocketCommunicator(
            application,
            'ws/sessions/1/generate',
            subprotocols=subprotocols
        )
        with self.assertRaises(Exception):
            await communicator.connect()

    async def test_connect_anonymous_user(self):
        subprotocols = ['json', '2', '3']
        communicator = WebsocketCommunicator(
            application,
            'ws/sessions/1/generate',
            subprotocols=subprotocols
        )
        connected, subprotocols = await communicator.connect()
        self.assertFalse(connected)
        self.assertEqual(subprotocols, status.WS_401_UNAUTHORIZED)


@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
class ChatGenerateConsumerCheckPermissionTestCase(TransactionTestCase):
    def setUp(self):
        self.tokens = []
        @receiver(post_save, sender=settings.AUTH_USER_MODEL)
        def create_auth_token(sender, instance=None, created=False, **kwargs):
            if created and instance is not None and not instance.is_superuser:
                token = Token.objects.create(user=instance)
                self.tokens.append(token)
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)

    async def test_connect_invalid_team(self):
        subprotocols = ['json', self.tokens[0].key, '1000']
        communicator = WebsocketCommunicator(
            application,
            'ws/sessions/1/generate',
            subprotocols=subprotocols
        )
        connected, subprotocols = await communicator.connect()
        self.assertFalse(connected)
        self.assertEqual(subprotocols, status.WS_500_INTERNAL_SERVER_ERROR)

    async def test_connect_not_member(self):
        team = self.regular_users[1]['teams'][0]['team']
        subprotocols = ['json', self.tokens[0].key, str(team.id)]
        communicator = WebsocketCommunicator(
            application,
            'ws/sessions/1/generate',
            subprotocols=subprotocols
        )
        connected, subprotocols = await communicator.connect()
        self.assertFalse(connected)
        self.assertEqual(subprotocols, status.WS_403_FORBIDDEN)

    async def test_connect_session_not_in_team(self):
        user = self.regular_users[1]['user']
        team = self.regular_users[1]['teams'][0]['team']
        data = SESSION_DATA.copy()
        data['session_type'] = SessionType.PROMPT.value
        del data['related_model']
        session = await sync_to_async(create_dummy_session)(team=team, owner=user, data=data)

        subprotocols = ['json', self.tokens[0].key, str(team.id)]
        communicator = WebsocketCommunicator(
            application,
            f'ws/sessions/{session.id}/generate',
            subprotocols=subprotocols
        )
        connected, subprotocols = await communicator.connect()
        self.assertFalse(connected)
        self.assertEqual(subprotocols, status.WS_403_FORBIDDEN)

    async def test_connect_invalid_session(self):
        team = self.regular_users[0]['teams'][0]['team']
        subprotocols = ['json', self.tokens[0].key, str(team.id)]
        communicator = WebsocketCommunicator(
            application,
            f'ws/sessions/100/generate',
            subprotocols=subprotocols
        )
        connected, subprotocols = await communicator.connect()
        self.assertFalse(connected)
        self.assertEqual(subprotocols, status.WS_404_NOT_FOUND)
