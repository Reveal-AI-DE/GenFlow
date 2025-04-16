# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional
from urllib.parse import parse_qs

from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import LazyObject
from rest_framework.authtoken.models import Token

from gen_flow.apps.team.middleware import TeamContext


class TeamContextWithRole(TeamContext):
    team_role: Optional[str] = None


class WebSocketRequest:
    """
    A class to represent a WebSocket request. This call will be used
    to verify user permissions and IAM context.

    Attributes:
    -----------
    user : Any
        The user associated with the WebSocket connection.
    GET : dict
        The parsed query string parameters from the WebSocket connection.
    headers : dict
        The headers associated with the WebSocket connection.
    iam_context : TeamContextWithRole
        The IAM context for the WebSocket connection, initialized to None.
    """

    def __init__(self, scope):
        """
        Initializes the WebSocketRequest with the given scope.'
        """

        self.user = scope["user"]
        self.GET: dict = parse_qs(scope["query_string"].decode())
        self.headers: dict = {"X-Team": scope["subprotocols"][2]}
        self.iam_context: TeamContextWithRole = None


class WebSocketRequestLazyObject(LazyObject):
    """
    Throw a more useful error message when scope['request'] is accessed before
    it's resolved
    """

    def _setup(self):
        raise ValueError("Accessing scope request before it is ready.")


async def get_request(scope) -> WebSocketRequest:
    return WebSocketRequest(scope)


@database_sync_to_async
def get_user(scope):
    """
    Retrieve the user associated with the given scope.

    Args:
        scope (dict): A dictionary containing connection scope information,
        including subprotocols.

    Returns:
        User: The user associated with the provided token if valid and active.
        AnonymousUser: If the token is invalid, not provided, or the user is inactive.
    """

    token = scope["subprotocols"][1]
    if not token:
        return AnonymousUser()
    try:
        user = Token.objects.get(key=token).user

    except Exception:
        # TODO: Log the exception
        return AnonymousUser()
    if not user.is_active:
        return AnonymousUser()
    return user


class TokenAuthMiddleware(AuthMiddleware):
    """
    TokenAuthMiddleware is a custom middleware class that extends AuthMiddleware
    to handle token-based authentication for Websocket connections.
    """

    def populate_scope(self, scope):
        """
        Populates the scope with necessary information. Ensures that 'subprotocols' is a list of three strings and adds a 'request' to the scope if not present.
        Raises:
            ValueError: If 'subprotocols' is not found in scope or if it is not a list of three strings.
            scope['subprotocols'] is a list of strings [response format: 'json', user token, current team]
        """

        super().populate_scope(scope)

        # check scope['subprotocols']
        if "subprotocols" not in scope:
            raise ValueError("TokenAuthMiddleware cannot find subprotocols in scope.")
        elif not isinstance(scope["subprotocols"], list) or len(scope["subprotocols"]) != 3:
            raise ValueError("TokenAuthMiddleware requires subprotocols to be a list of 3 strings.")

        elif not all([isinstance(item, str) for item in scope["subprotocols"]]):
            raise ValueError("TokenAuthMiddleware requires subprotocols to be a list of 3 strings.")

        elif scope["subprotocols"][0] != "json":
            raise ValueError(
                f"Unsupported format specified in subprotocols '{scope['subprotocols'][0]}'"
            )

        scope["request"] = WebSocketRequestLazyObject()

    async def resolve_scope(self, scope):
        """
        Asynchronously resolves and sets the 'user' and 'request' in the scope by calling get_user and get_request respectively.
        """
        scope["user"]._wrapped = await get_user(scope)
        scope["request"]._wrapped = await get_request(scope)


def TokenAuthMiddlewareStack(inner):
    """
    Middleware stack that applies token authentication, session management, and cookie handling.
    """

    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))
