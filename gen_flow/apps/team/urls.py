# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework.routers import DefaultRouter

import gen_flow.apps.team.views as views

router = DefaultRouter(trailing_slash=False)
router.register('teams', views.TeamViewSet)

urlpatterns = router.urls