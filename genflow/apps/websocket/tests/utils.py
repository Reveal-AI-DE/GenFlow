# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from genflow.apps.websocket.auth_middleware import TokenAuthMiddlewareStack
from genflow.apps.websocket.team_middleware import ContextMiddleware
from genflow.apps.websocket.urls import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "genflow.settings.testing")

# Initialize Django ASGI application early to ensure the app registry is ready
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "websocket": TokenAuthMiddlewareStack(ContextMiddleware(URLRouter(websocket_urlpatterns))),
    }
)
