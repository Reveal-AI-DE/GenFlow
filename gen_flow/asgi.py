"""
ASGI config for gen_flow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gen_flow.settings.development")

# Initialize Django ASGI application early to ensure the app registry is ready
django_asgi_app = get_asgi_application()

from gen_flow.apps.websocket.auth_middleware import TokenAuthMiddlewareStack
from gen_flow.apps.websocket.team_middleware import ContextMiddleware
from gen_flow.apps.websocket.urls import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddlewareStack(ContextMiddleware(URLRouter(websocket_urlpatterns))),
    }
)
