# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.conf import settings
from django.urls import path
from django.urls.conf import include

from gen_flow.apps.iam.views import RegisterViewEx

BASIC_LOGIN_PATH_NAME = "rest_login"
BASIC_REGISTER_PATH_NAME = "rest_register"

urlpatterns = [
    path("login", LoginView.as_view(), name=BASIC_LOGIN_PATH_NAME),
    path("logout", LogoutView.as_view(), name="rest_logout"),
]

if settings.IAM_TYPE == "BASIC":
    urlpatterns += [
        path("register", RegisterViewEx.as_view(), name=BASIC_REGISTER_PATH_NAME),
        # password
        path("password/reset", PasswordResetView.as_view(), name="rest_password_reset"),
        path(
            "password/reset/confirm",
            PasswordResetConfirmView.as_view(),
            name="rest_password_reset_confirm",
        ),
        path("password/change", PasswordChangeView.as_view(), name="rest_password_change"),
    ]

urlpatterns = [path("auth/", include(urlpatterns))]
