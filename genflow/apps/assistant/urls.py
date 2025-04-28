# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework.routers import DefaultRouter

from genflow.apps.assistant.views import AssistantGroupViewSet, AssistantsViewSet

router = DefaultRouter(trailing_slash=False)
router.register("assistants", AssistantsViewSet)
router.register("assistant/groups", AssistantGroupViewSet, basename="assistant-group")

urlpatterns = router.urls
