# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.test import override_settings
from django.urls import re_path, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from genflow.apps.iam.urls import urlpatterns as iam_url_patterns
from genflow.apps.iam.views import ConfirmEmailViewEx

urlpatterns = iam_url_patterns + [
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailViewEx.as_view(),
        name="account_confirm_email",
    ),
]


class UserRegisterAPITestCase(APITestCase):
    user_data = {
        "first_name": "test_first",
        "last_name": "test_last",
        "username": "test_username",
        "email": "test_email@test.com",
        "password1": "$Test357Test%",
        "password2": "$Test357Test%",
        "confirmations": [],
    }

    def setUp(self):
        self.client = APIClient()

    def auth_register(self, data):
        url = reverse("rest_register")
        response = self.client.post(url, data, format="json")
        return response

    def check_response(self, response, data):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none")
    def test_auth_register_with_email_verification_none(self):
        """
        Ensure we can register a user and get auth token key when email verification is none
        """
        response = self.auth_register(self.user_data)
        user_token = Token.objects.get(user__username=response.data["username"])
        self.check_response(
            response,
            {
                "first_name": "test_first",
                "last_name": "test_last",
                "username": "test_username",
                "email": "test_email@test.com",
                "email_verification_required": False,
                "key": user_token.key,
            },
        )

    # Since URLConf is executed before running the tests, so we have to manually configure the url patterns for
    # the tests and pass it using ROOT_URLCONF in the override settings decorator
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional", ROOT_URLCONF=__name__)
    def test_auth_register_with_email_verification_optional(self):
        """
        Ensure we can register a user and get auth token key when email verification is optional
        """
        response = self.auth_register(self.user_data)
        user_token = Token.objects.get(user__username=response.data["username"])
        self.check_response(
            response,
            {
                "first_name": "test_first",
                "last_name": "test_last",
                "username": "test_username",
                "email": "test_email@test.com",
                "email_verification_required": False,
                "key": user_token.key,
            },
        )

    @override_settings(
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_EMAIL_VERIFICATION="mandatory",
        EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend",
        ROOT_URLCONF=__name__,
    )
    def test_auth_register_with_email_verification_mandatory(self):
        """
        Ensure we can register a user and it does not return auth token key when email verification is mandatory
        """
        response = self.auth_register(self.user_data)
        self.check_response(
            response,
            {
                "first_name": "test_first",
                "last_name": "test_last",
                "username": "test_username",
                "email": "test_email@test.com",
                "email_verification_required": True,
                "key": None,
            },
        )
