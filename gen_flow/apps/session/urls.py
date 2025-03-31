# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import routers

from gen_flow.apps.session.views import (
     SessionViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('sessions', SessionViewSet)

urlpatterns = router.urls
