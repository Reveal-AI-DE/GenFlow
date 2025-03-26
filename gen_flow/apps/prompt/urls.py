# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework.routers import DefaultRouter

from gen_flow.apps.prompt.views import PromptGroupViewSet, PromptViewSet

router = DefaultRouter(trailing_slash=False)
router.register('prompt-groups', PromptGroupViewSet, basename='prompt-group')
router.register('prompts', PromptViewSet)

urlpatterns = router.urls
