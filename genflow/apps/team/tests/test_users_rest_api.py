# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class UserAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)


class UserSelfAPITestCase(UserAPITestCase):
    def check_response(self, user, response, is_full=True):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(user, response.data, is_full)

    def check_data(self, user, data, is_full):
        self.assertEqual(data["id"], user.id)
        self.assertEqual(data["username"], user.username)
        self.assertEqual(data["first_name"], user.first_name)
        self.assertEqual(data["last_name"], user.last_name)
        extra_check = self.assertIn if is_full else self.assertNotIn
        extra_check("email", data)
        extra_check("groups", data)
        extra_check("is_staff", data)
        extra_check("is_superuser", data)
        extra_check("is_active", data)
        extra_check("last_login", data)
        extra_check("date_joined", data)

    def users_self(self, user):
        with ForceLogin(user, self.client):
            response = self.client.get("/api/users/self")
        return response

    def test_users_self_admin(self):
        response = self.users_self(self.admin_user)
        self.check_response(self.admin_user, response)

    def test_users_self_user(self):
        for user in self.regular_users:
            response = self.users_self(user["user"])
            self.check_response(user["user"], response)

    def test_users_self_no_auth(self):
        response = self.users_self(None)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCheckAPITestCase(UserAPITestCase):
    def users_check(self, data):
        return self.client.post("/api/users/check", data=data, format="json")

    def check_response(self, response, expected_status=status.HTTP_204_NO_CONTENT):
        self.assertEqual(response.status_code, expected_status)

    def test_users_check_username_only(self):
        user = self.regular_users[0]["user"]
        response = self.users_check({"username": user.username})
        self.check_response(response, expected_status=status.HTTP_200_OK)

    def test_users_check_email_only(self):
        user = self.regular_users[0]["user"]
        response = self.users_check({"email": user.email})
        self.check_response(response, expected_status=status.HTTP_200_OK)

    def test_users_check_username_email(self):
        user = self.regular_users[0]["user"]

        # both username and email are already taken
        response = self.users_check({"username": user.username, "email": user.email})
        self.check_response(response, expected_status=status.HTTP_200_OK)

        # username is already taken, email is not
        response = self.users_check({"username": user.username, "email": "dummy@dummy.com"})
        self.check_response(response, expected_status=status.HTTP_200_OK)

        # email is already taken, username is not
        response = self.users_check({"username": "dummy", "email": user.email})
        self.check_response(response, expected_status=status.HTTP_200_OK)

        # both username and email are not taken
        response = self.users_check({"username": "dummy", "email": "dummy@dummy.com"})
        self.check_response(response, expected_status=status.HTTP_204_NO_CONTENT)
