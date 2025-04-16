# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.utils.functional import SimpleLazyObject

from gen_flow.apps.iam.permissions import get_membership
from gen_flow.apps.team.middleware import TeamContext, get_team
from gen_flow.apps.websocket.auth_middleware import TeamContextWithRole, WebSocketRequest


def build_iam_context(request: WebSocketRequest) -> TeamContextWithRole:
    """
    Constructs an IAM context for a WebSocket request.
    """

    initial_context: TeamContext = get_team(request)
    membership = get_membership(request, initial_context.team)
    iam_context = TeamContextWithRole(
        team=initial_context.team,
        privilege=initial_context.privilege,
        team_role=getattr(membership, "role", None),
    )
    return iam_context


@database_sync_to_async
def get_iam_context(scope) -> None:
    """
    Attach an IAM context to the request object within the given scope.
    """

    scope["request"].iam_context = SimpleLazyObject(lambda: build_iam_context(scope["request"]))


class ContextMiddleware(BaseMiddleware):
    """
    Injects and populate the ASGI scope with additional context.

    """

    def __init__(self, inner) -> None:
        super().__init__(inner)

    def populate_scope(self, scope):
        """
        Ensures the 'request' key exists in the scope and raises an error
            if it is missing. This method is intended to be overridden or
            extended for additional scope population logic.
        """

        if "request" not in scope:
            raise ValueError(
                "ContextMiddleware cannot find request in scope. "
                "TokenAuthMiddlewareStack must be above it."
            )

    async def __call__(self, scope, receive, send):
        """
        Asynchronously processes the ASGI scope, mutates it as needed,
            integrates IAM context, and passes it to the inner application.
        """

        scope = dict(scope)

        # Scope injection/mutation per this middleware's needs.
        self.populate_scope(scope)

        # Grab the finalized/resolved scope
        await get_iam_context(scope)

        return await super().__call__(scope, receive, send)
