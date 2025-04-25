# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework.routers import DefaultRouter

from genflow.apps.assistant.views import AssistantGroupViewSet, AssistantsViewSet

router = DefaultRouter(trailing_slash=False)
router.register("assistants", AssistantsViewSet)
router.register("assistant/groups", AssistantGroupViewSet, basename="assistant-group")

urlpatterns = router.urls
