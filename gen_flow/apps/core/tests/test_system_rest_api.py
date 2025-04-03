# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow import __version__ as gen_flow_version
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users


class ServerAboutTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users()

    def get_about(self, user=None) -> HTTPResponse:
        url = '/api/system/about'
        if user is None:
            response = self.client.get(url)
        else:
            with ForceLogin(user, self.client):
                response = self.client.get(url)
        return response

    def test_about_anonymous(self):
        response = self.client.get('/api/system/about')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_about_admin(self):
        response = self.get_about(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['version'], gen_flow_version)

    def test_about_user(self):
        response = self.get_about(self.regular_users[0]['user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['version'], gen_flow_version)
