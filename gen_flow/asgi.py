'''
ASGI config for gen_flow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
'''

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gen_flow.settings.development')

# Initialize Django ASGI application early to ensure the app registry is ready
django_asgi_app = get_asgi_application()

application =  ProtocolTypeRouter({
    'http': get_asgi_application(),
})
