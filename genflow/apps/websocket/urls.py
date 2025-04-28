# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.urls import re_path

from genflow.apps.websocket.consumer.chat import ChatGenerateConsumer

websocket_urlpatterns = [
    re_path(r"ws/sessions/(?P<session_id>\w+)/generate$", ChatGenerateConsumer.as_asgi()),
]
