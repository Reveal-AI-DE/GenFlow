# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework.routers import DefaultRouter

from genflow.apps.prompt.views import PromptGroupViewSet, PromptViewSet

router = DefaultRouter(trailing_slash=False)
router.register("prompts", PromptViewSet)
router.register("prompt/groups", PromptGroupViewSet, basename="prompt-group")

urlpatterns = router.urls
