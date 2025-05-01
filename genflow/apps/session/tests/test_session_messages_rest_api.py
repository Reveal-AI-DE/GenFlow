# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from http.client import HTTPResponse
from urllib.parse import urlencode

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.core.tests.utils import enable_provider
from genflow.apps.prompt.tests.utils import PROVIDER_DATA
from genflow.apps.restriction.tests.utils import override_limit
from genflow.apps.session.tests.utils import (
    SESSION_DATA,
    SESSION_MESSAGE_DATA,
    create_dummy_session,
    create_dummy_session_message,
)
from genflow.apps.team.models import TeamRole
from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class SessionMessageTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # pylint: disable=unused-import
        import genflow.apps.ai.tests.register_providers  # noqa

        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    @classmethod
    def create_session_messages(cls):
        team = cls.regular_users[0]["teams"][0]["team"]
        user = cls.regular_users[0]["user"]
        # llm session
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        session_data = SESSION_DATA.copy()
        cls.session = create_dummy_session(team=team, owner=user, data=session_data)
        data = SESSION_MESSAGE_DATA.copy()
        cls.regular_users[0]["teams"][0]["messages"] = []
        for item in data:
            session_message = create_dummy_session_message(
                team=team, owner=user, session=cls.session, data=item
            )
            cls.regular_users[0]["teams"][0]["messages"].append(session_message)


class SessionMessageListTestCase(SessionMessageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_session_messages()

    def list_session_messages(self, user, session_id=None, team_id=None) -> HTTPResponse:
        query_params = {}
        if team_id:
            query_params["team"] = team_id
        if session_id:
            query_params["session"] = session_id

        url = f"/api/messages?{urlencode(query_params)}" if query_params else "/api/messages"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_session_messages_admin_query_parameters(self):
        response = self.list_session_messages(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_session_messages(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_session_messages_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        messages = self.regular_users[0]["teams"][0]["messages"]
        response = self.list_session_messages(
            self.admin_user, session_id=self.session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["query"], messages[0].query)
        self.assertEqual(response.data["results"][1]["query"], messages[1].query)

    def test_list_session_messages_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_session_messages(user, session_id=self.session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_session_messages_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_session_messages(user, session_id=self.session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_session_messages_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_session_messages(
            another_user, session_id=self.session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_session_messages_user_filtering(self):
        another_team = self.regular_users[1]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_session_messages(
            another_user, session_id=self.session.id, team_id=another_team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class SessionMessageGenerateTestCase(SessionMessageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_session_messages()
        cls.generate_request = {
            "query": "Test Message",
            "stream": False,
        }

    def generate_message(self, user, session_id, data, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}/generate?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}/generate"
        )
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format="json")
        return response

    def test_generate_message_admin_no_team(self):
        response = self.generate_message(
            self.admin_user, session_id=self.session.id, data=self.generate_request
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_message_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.generate_message(
            self.admin_user, session_id=self.session.id, data=self.generate_request, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["answer"], "result")

    def test_generate_message_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.generate_message(
            user, session_id=self.session.id, data=self.generate_request, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["answer"], "result")

    def test_generate_message_user_another_team(self):
        another_user = self.regular_users[1]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.generate_message(
            user, session_id=self.session.id, data=self.generate_request, team_id=another_user.id
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_message_user_team_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        # llm session
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.generate_message(
            user, session_id=self.session.id, data=self.generate_request, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["answer"], "result")

    def test_generate_message_user_check_global_limit(self):
        override_limit(
            key="MESSAGE",
            value=2,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.generate_message(
            user, session_id=self.session.id, data=self.generate_request, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_message_user_check_under_global_limit(self):
        override_limit(
            key="MESSAGE",
            value=3,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.generate_message(
            user, session_id=self.session.id, data=self.generate_request, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["answer"], "result")
