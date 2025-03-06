# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.urls import path
from django.conf import settings
from django.urls.conf import include
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from dj_rest_auth.registration.views import RegisterView

BASIC_LOGIN_PATH_NAME = 'rest_login'
BASIC_REGISTER_PATH_NAME = "rest_register"

urlpatterns = [
    path('login', LoginView.as_view(), name=BASIC_LOGIN_PATH_NAME),
    path('logout', LogoutView.as_view(), name='rest_logout'),
]

if settings.IAM_TYPE == 'BASIC':
    urlpatterns += [
        path('register', RegisterView.as_view(), name=BASIC_REGISTER_PATH_NAME),
        # password
        path('password/reset', PasswordResetView.as_view(),
            name='rest_password_reset'),
        path('password/reset/confirm', PasswordResetConfirmView.as_view(),
            name='rest_password_reset_confirm'),
        path('password/change', PasswordChangeView.as_view(),
            name='rest_password_change'),
    ]

urlpatterns = [path('auth/', include(urlpatterns))]