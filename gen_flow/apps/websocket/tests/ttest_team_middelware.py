# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from asgiref.testing import ApplicationCommunicator
from django.test import TransactionTestCase

from gen_flow.apps.websocket.auth_middleware import TokenAuthMiddleware
from gen_flow.apps.websocket.team_middleware import ContextMiddleware


class TeamMiddlewareTestCase(TransactionTestCase):
    '''
    Test the TeamMiddleware to ensure it populates the scope correctly.
    '''

    def setUp(self):
        async def dummy_app(scope, receive, send):
            # Dummy ASGI app to test middleware
            pass

        # Wrap the dummy app with the middleware
        self.middleware = TokenAuthMiddleware(ContextMiddleware(dummy_app))

        # Create a fake ASGI scope
        self.scope = {
            'type': 'websocket',
            'path': '/ws/some-endpoint/',
            'session': '',
            'query_string': b'',
            'subprotocols': ['json', '2', '3']
        }

    async def test_call(self):
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        await communicator.send_input({'type': 'websocket.connect'})
        await communicator.receive_nothing()
