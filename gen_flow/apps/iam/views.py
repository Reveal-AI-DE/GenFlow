# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from dj_rest_auth.app_settings import api_settings as dj_rest_auth_settings
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.utils import jwt_encode
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup


class RegisterViewEx(RegisterView):
    def get_response_data(self, user):
        serializer = self.get_serializer(user)
        return serializer.data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if allauth_settings.EMAIL_VERIFICATION != \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            if dj_rest_auth_settings.USE_JWT:
                self.access_token, self.refresh_token = jwt_encode(user)
            elif self.token_model:
                dj_rest_auth_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        complete_signup(
            self.request._request, user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )
        return user
