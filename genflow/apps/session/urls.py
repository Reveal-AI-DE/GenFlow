# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework import routers

from genflow.apps.session.views import SessionMessageViewSet, SessionViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("sessions", SessionViewSet)
router.register("messages", SessionMessageViewSet, basename="message")

urlpatterns = router.urls
