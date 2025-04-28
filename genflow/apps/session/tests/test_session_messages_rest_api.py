# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from http.client import HTTPResponse
from urllib.parse import urlencode

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.core.tests.utils import enable_provider
from genflow.apps.prompt.tests.utils import PROVIDER_DATA
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
        session = create_dummy_session(team=team, owner=user, data=session_data)
        data = SESSION_MESSAGE_DATA.copy()
        cls.regular_users[0]["teams"][0]["messages"] = []
        for item in data:
            session_message = create_dummy_session_message(
                team=team, owner=user, session=session, data=item
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
        session = messages[0].session
        response = self.list_session_messages(
            self.admin_user, session_id=session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["query"], messages[0].query)
        self.assertEqual(response.data["results"][1]["query"], messages[1].query)

    def test_list_session_messages_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        messages = self.regular_users[0]["teams"][0]["messages"]
        session = messages[0].session
        response = self.list_session_messages(user, session_id=session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_session_messages_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        messages = self.regular_users[0]["teams"][0]["messages"]
        session = messages[0].session
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_session_messages(user, session_id=session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_session_messages_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        messages = self.regular_users[0]["teams"][0]["messages"]
        session = messages[0].session
        response = self.list_session_messages(another_user, session_id=session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_session_messages_user_filtering(self):
        another_team = self.regular_users[1]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        messages = self.regular_users[0]["teams"][0]["messages"]
        session = messages[0].session
        response = self.list_session_messages(
            another_user, session_id=session.id, team_id=another_team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
