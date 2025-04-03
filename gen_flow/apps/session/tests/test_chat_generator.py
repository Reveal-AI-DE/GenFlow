# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.test import override_settings

from gen_flow.apps.team.tests.utils import create_dummy_users
from gen_flow.apps.core.tests.utils import enable_provider
from gen_flow.apps.prompt.tests.utils import PROVIDER_DATA
from gen_flow.apps.session.tests.utils import create_dummy_session, SESSION_DATA
from gen_flow.apps.websocket.tests.utils import application


@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
class ChatGenerateTestCase(TransactionTestCase):
    def setUp(self):
        self.tokens = []
        self.sessions = []
        @receiver(post_save, sender=settings.AUTH_USER_MODEL)
        def create_auth_token(sender, instance=None, created=False, **kwargs):
            if created and instance is not None and not instance.is_superuser:
                token = Token.objects.create(user=instance)
                self.tokens.append(token)
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)

        import gen_flow.apps.ai.tests.register_providers # noqa
        for item in self.regular_users:
            user = item['user']
            team = item['teams'][0]['team']
            _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
            data = SESSION_DATA.copy()
            session = create_dummy_session(team=team, owner=user, data=data)
            self.sessions.append(session)

    async def test_generate(self):
        team = self.regular_users[0]['teams'][0]['team']
        subprotocols = ['json', self.tokens[0].key, str(team.id)]
        communicator = WebsocketCommunicator(
            application,
            f'ws/sessions/{self.sessions[0].id}/generate',
            subprotocols=subprotocols
        )
        connected, subprotocols = await communicator.connect()
        self.assertTrue(connected)
        self.assertEqual(subprotocols, 'json')

        request = {'query': 'Hi!', 'stream': False}
        await communicator.send_json_to(data=request)
        response = await communicator.receive_json_from()
        self.assertEqual(response['data']['answer'], 'result')

        # Close
        await communicator.disconnect()
