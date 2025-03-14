# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.tests.utils import create_groups


class UserRegisterAPITestCase(APITestCase):

    user_data = {
        'first_name': 'test_first',
        'last_name': 'test_last',
        'username': 'test_username',
        'email': 'test_email@test.com',
        'password1': '$Test357Test%',
        'password2': '$Test357Test%',
        'confirmations': [],
    }

    def setUp(self):
        self.client = APIClient()
        # TODO: should be removed after fixing the issue with the post_migrate signal
        create_groups()

    def _run_api_user_register(self, data):
        url = reverse('rest_register')
        response = self.client.post(url, data, format='json')
        return response

    def _check_response(self, response, data):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
    def test_api_user_register_with_email_verification_none(self):
        '''
        Ensure we can register a user and get auth token key when email verification is none
        '''
        response = self._run_api_user_register(self.user_data)
        user_token = Token.objects.get(user__username=response.data['username'])
        self._check_response(
            response,
            {
                'first_name': 'test_first',
                'last_name': 'test_last',
                'username': 'test_username',
                'email': 'test_email@test.com',
                'email_verification_required': False,
                'key': user_token.key,
            },
        )
