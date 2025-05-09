# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from asgiref.testing import ApplicationCommunicator
from django.test import TransactionTestCase

from genflow.apps.websocket.auth_middleware import TokenAuthMiddleware
from genflow.apps.websocket.team_middleware import IAMContextMiddleware


class IAMContextMiddlewareTestCase(TransactionTestCase):
    """
    Test the TeamMiddleware to ensure it populates the scope correctly.
    """

    def setUp(self):
        async def dummy_app(scope, receive, send):
            # Dummy ASGI app to test middleware
            pass

        # Wrap the dummy app with the middleware
        self.middleware = TokenAuthMiddleware(IAMContextMiddleware(dummy_app))

        # Create a fake ASGI scope
        self.scope = {
            "type": "websocket",
            "path": "/ws/some-endpoint/",
            "session": "",
            "query_string": b"",
            "subprotocols": ["json", "2", "3"],
        }

    async def test_call(self):
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        await communicator.send_input({"type": "websocket.connect"})
        await communicator.receive_nothing()
