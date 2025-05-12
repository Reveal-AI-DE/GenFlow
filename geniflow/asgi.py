"""
ASGI config for geniflow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geniflow.settings.development")

# Initialize Django ASGI application early to ensure the app registry is ready
django_asgi_app = get_asgi_application()

from geniflow.apps.websocket.auth_middleware import TokenAuthMiddlewareStack
from geniflow.apps.websocket.team_middleware import IAMContextMiddleware
from geniflow.apps.websocket.urls import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddlewareStack(
            IAMContextMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
