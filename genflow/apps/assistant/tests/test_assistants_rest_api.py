# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.core.tests.utils import enable_provider
from genflow.apps.prompt.tests.utils import PROVIDER_DATA
from genflow.apps.assistant.tests.utils import (
    ASSISTANT_DATA,
    ASSISTANT_GROUP_DATA,
    create_dummy_assistant,
    create_dummy_assistant_group,
)
from genflow.apps.team.models import TeamRole
from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class AssistantTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # pylint: disable=unused-import
        import genflow.apps.ai.tests.register_providers  # noqa

        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    @classmethod
    def create_assistants(cls):
        team = cls.regular_users[0]["teams"][0]["team"]
        user = cls.regular_users[0]["user"]
        data = ASSISTANT_DATA.copy()
        del data["related_model"]
        cls.assistant = create_dummy_assistant(team=team, owner=user, data=data)


class AssistantCreateTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for item in cls.regular_users:
            user = item["user"]
            for team_membership in item["teams"]:
                team = team_membership["team"]
                group = create_dummy_assistant_group(team=team, owner=user, data=ASSISTANT_GROUP_DATA)
                team_membership["group"] = group

    def create_assistant(self, user, data, team_id=None) -> HTTPResponse:
        url = f"/api/assistants?team={team_id}" if team_id else "/api/assistants"
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format="json")
        return response

    def test_create_assistant_admin_no_team(self):
        response = self.create_assistant(self.admin_user, ASSISTANT_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_assistant_admin_validation_error(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]
        another_group = self.regular_users[1]["teams"][0]["group"]

        # no group, provider not enabled
        response = self.create_assistant(self.admin_user, ASSISTANT_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = ASSISTANT_DATA.copy()
        data["group_id"] = group.id
        # provider not enabled
        response = self.create_assistant(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        # group not in team
        data["group_id"] = another_group.id
        response = self.create_assistant(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_assistant_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]

        data = ASSISTANT_DATA.copy()
        data["group_id"] = group.id
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        response = self.create_assistant(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assistant_user_validation_error(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]
        another_group = self.regular_users[1]["teams"][0]["group"]

        # no group, provider not enabled
        response = self.create_assistant(user, ASSISTANT_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = ASSISTANT_DATA.copy()
        data["group_id"] = group.id
        # provider not enabled
        response = self.create_assistant(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        # group not in team
        data["group_id"] = another_group.id
        response = self.create_assistant(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_assistant_user_forbidden(self):
        user = self.regular_users[0]["user"]
        # not team member
        another_team = self.regular_users[1]["teams"][0]["team"]
        response = self.create_assistant(user, ASSISTANT_DATA, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_assistant_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]

        data = ASSISTANT_DATA.copy()
        data["group_id"] = group.id
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        response = self.create_assistant(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AssistantRetrieveTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()

    def retrieve_assistant(self, user, assistant_id, team_id=None) -> HTTPResponse:
        url = f"/api/assistants/{assistant_id}?team={team_id}" if team_id else f"/api/assistants/{assistant_id}"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_retrieve_assistant_admin_no_team(self):
        response = self.retrieve_assistant(self.admin_user, assistant_id=self.assistant.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], ASSISTANT_DATA["name"])
        self.assertFalse(response.data["is_pinned"])

    def test_retrieve_assistant_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.retrieve_assistant(self.admin_user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_pinned"])

    def test_retrieve_assistant_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.retrieve_assistant(user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_pinned"])

    def test_retrieve_assistant_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.retrieve_assistant(another_user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_assistant_team_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.retrieve_assistant(user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], ASSISTANT_DATA["name"])


class AssistantDeleteTestCase(AssistantTestCase):
    def setUp(self):
        super().setUp()
        self.create_assistants()

    def delete_assistant(self, user, assistant_id, team_id=None) -> HTTPResponse:
        url = f"/api/assistants/{assistant_id}?team={team_id}" if team_id else f"/api/assistants/{assistant_id}"
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_assistant_admin_no_team(self):
        response = self.delete_assistant(self.admin_user, assistant_id=self.assistant.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_assistant(self.admin_user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_assistant(user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_assistant(another_user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_assistant_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_assistant(user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AssistantUpdateTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()

    def update_assistant(self, user, assistant_id, data, team_id=None) -> HTTPResponse:
        url = f"/api/assistants/{assistant_id}?team={team_id}" if team_id else f"/api/assistants/{assistant_id}"
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format="json")
        return response

    def test_update_assistant_admin_no_team(self):
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant(self.admin_user, assistant_id=self.assistant.id, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_assistant_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant(
            self.admin_user, assistant_id=self.assistant.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_assistant_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant(
            user, assistant_id=self.assistant.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_assistant_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant(
            another_user, assistant_id=self.assistant.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_assistant_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant(
            user, assistant_id=self.assistant.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])


class AssistantListTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()

    def list_assistant(self, user, team_id=None) -> HTTPResponse:
        url = f"/api/assistants?team={team_id}" if team_id else "/api/assistants"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_assistant_admin_no_team(self):
        response = self.list_assistant(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_assistant_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_assistant(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.assistant.name)

    def test_list_assistant_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_assistant(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.assistant.name)

    def test_list_assistant_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_assistant(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.assistant.name)

    def test_list_assistant_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_assistant(another_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_assistant_team_filtering(self):
        another_user = self.regular_users[1]["user"]
        another_team = self.regular_users[1]["teams"][0]["team"]
        response = self.list_assistant(another_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
