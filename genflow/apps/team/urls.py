# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework.routers import DefaultRouter

import genflow.apps.team.views as views

router = DefaultRouter(trailing_slash=False)
router.register("teams", views.TeamViewSet)
router.register("memberships", views.MembershipViewSet)
router.register("invitations", views.InvitationViewSet)

urlpatterns = router.urls
