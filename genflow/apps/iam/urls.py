# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from allauth.account import app_settings as allauth_settings
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.conf import settings
from django.urls import path, re_path
from django.urls.conf import include

from genflow.apps.iam.views import ConfirmEmailViewEx, GoogleLogin, RegisterViewEx

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

    if allauth_settings.EMAIL_VERIFICATION != allauth_settings.EmailVerificationMethod.NONE:
        # emails
        urlpatterns += [
            re_path(
                r"^confirm-email/(?P<key>[-:\w]+)/$",
                ConfirmEmailViewEx.as_view(),
                name="account_confirm_email",
            ),
        ]

    # add social auth urls
    if "google" in settings.SOCIALACCOUNT_PROVIDERS:
        urlpatterns += [
            path("google", GoogleLogin.as_view(), name="google_login"),
        ]

urlpatterns = [path("auth/", include(urlpatterns))]
