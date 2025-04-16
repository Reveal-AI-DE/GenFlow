# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.urls import re_path

from gen_flow.apps.websocket.consumer.chat import ChatGenerateConsumer

websocket_urlpatterns = [
    re_path(r"ws/sessions/(?P<session_id>\w+)/generate$", ChatGenerateConsumer.as_asgi()),
]
