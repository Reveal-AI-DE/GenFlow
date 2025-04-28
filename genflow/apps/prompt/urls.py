# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework.routers import DefaultRouter

from genflow.apps.prompt.views import PromptGroupViewSet, PromptViewSet

router = DefaultRouter(trailing_slash=False)
router.register("prompts", PromptViewSet)
router.register("prompt/groups", PromptGroupViewSet, basename="prompt-group")

urlpatterns = router.urls
