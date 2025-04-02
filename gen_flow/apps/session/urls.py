# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import routers

from gen_flow.apps.session.views import (
     SessionViewSet, SessionMessageViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('sessions', SessionViewSet)
router.register('messages', SessionMessageViewSet, basename='message')

urlpatterns = router.urls
