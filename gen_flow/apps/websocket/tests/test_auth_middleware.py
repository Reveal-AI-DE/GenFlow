# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from asgiref.testing import ApplicationCommunicator
from django.test import TransactionTestCase

from gen_flow.apps.websocket.auth_middleware import TokenAuthMiddleware


class TokenAuthMiddlewareTestCase(TransactionTestCase):
    """
    Test the TokenAuthMiddleware to ensure it populates the scope correctly.
    """

    def setUp(self):
        async def dummy_app(scope, receive, send):
            # Dummy ASGI app to test middleware
            pass

        # Wrap the dummy app with the middleware
        self.middleware = TokenAuthMiddleware(dummy_app)

        # Create a fake ASGI scope
        self.scope = {
            "type": "websocket",
            "path": "/ws/some-endpoint/",
            "session": "",
            "query_string": b"",
        }

    async def test_populate_scope_no_subprotocols(self):
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        with self.assertRaises(Exception):
            # Call the middleware
            await communicator.send_input({"type": "websocket.connect"})
            await communicator.receive_output()

    async def test_populate_scope_subprotocols_invalid(self):
        # invalid type
        self.scope["subprotocols"] = "123"
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        with self.assertRaises(Exception):
            # Call the middleware
            await communicator.send_input({"type": "websocket.connect"})
            await communicator.receive_output()

        # invalid length
        self.scope["subprotocols"] = ["1", "2"]
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        with self.assertRaises(Exception):
            # Call the middleware
            await communicator.send_input({"type": "websocket.connect"})
            await communicator.receive_output()

        # invalid format
        self.scope["subprotocols"] = ["1", "2", "3"]
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        with self.assertRaises(Exception):
            # Call the middleware
            await communicator.send_input({"type": "websocket.connect"})
            await communicator.receive_output()

        # invalid type
        self.scope["subprotocols"] = ["json", 2, "3"]
        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        with self.assertRaises(Exception):
            # Call the middleware
            await communicator.send_input({"type": "websocket.connect"})
            await communicator.receive_output()

    async def test_resolve_scope(self):
        self.scope["subprotocols"] = ["json", "2", "3"]

        # Create an ApplicationCommunicator
        communicator = ApplicationCommunicator(self.middleware, self.scope)

        # Call the middleware
        await communicator.send_input({"type": "websocket.connect"})
        await communicator.receive_nothing()
