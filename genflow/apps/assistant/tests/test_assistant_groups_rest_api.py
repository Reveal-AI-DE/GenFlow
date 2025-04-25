# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.assistant.tests.utils import ASSISTANT_GROUP_DATA, create_dummy_assistant_group
from genflow.apps.team.models import TeamRole
from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class AssistantGroupTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    @classmethod
    def create_dummy_assistant_groups(cls):
        team = cls.regular_users[0]["teams"][0]["team"]
        user = cls.regular_users[0]["user"]
        data = ASSISTANT_GROUP_DATA.copy()
        cls.assistant_group = create_dummy_assistant_group(team=team, owner=user, data=data)


class AssistantGroupCreateTestCase(AssistantGroupTestCase):
    def create_assistant_group(self, user, data, team_id=None) -> HTTPResponse:
        url = f"/api/assistant/groups?team={team_id}" if team_id else "/api/assistant/groups"
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format="json")
        return response

    def test_create_assistant_group_admin_no_team(self):
        response = self.create_assistant_group(self.admin_user, ASSISTANT_GROUP_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_assistant_group_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.create_assistant_group(
            self.admin_user, ASSISTANT_GROUP_DATA, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])

    def test_create_assistant_group_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.create_assistant_group(user, ASSISTANT_GROUP_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])

    def test_create_assistant_group_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[1]["user"]
        response = self.create_assistant_group(user, ASSISTANT_GROUP_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_assistant_group_team_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.create_assistant_group(user, ASSISTANT_GROUP_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])

    @override_settings(GF_LIMITS={"ASSISTANT-GROUP": 0})
    def test_create_assistant_group_user_user_check_limit(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.create_assistant_group(user, ASSISTANT_GROUP_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(GF_LIMITS={"ASSISTANT-GROUP": 1})
    def test_create_assistant_group_user_another_team_check_limit(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        # create assistant group to reach limit
        data = ASSISTANT_GROUP_DATA.copy()
        create_dummy_assistant_group(team=team, owner=user, data=data)
        team = self.regular_users[1]["teams"][0]["team"]
        user = self.regular_users[1]["user"]
        response = self.create_assistant_group(user, ASSISTANT_GROUP_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AssistantGroupRetrieveTestCase(AssistantGroupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_dummy_assistant_groups()

    def retrieve_assistant_group(self, user, group_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistant/groups/{group_id}?team={team_id}"
            if team_id
            else f"/api/assistant/groups/{group_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_retrieve_assistant_group_admin_no_team(self):
        response = self.retrieve_assistant_group(self.admin_user, group_id=self.assistant_group.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])

    def test_retrieve_assistant_group_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.retrieve_assistant_group(
            self.admin_user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])

    def test_retrieve_assistant_group_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.retrieve_assistant_group(
            user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])

    def test_retrieve_assistant_group_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.retrieve_assistant_group(
            another_user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_assistant_group_team_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.retrieve_assistant_group(
            user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], ASSISTANT_GROUP_DATA["name"])


class AssistantGroupDeleteTestCase(AssistantGroupTestCase):
    def setUp(self):
        super().setUp()
        self.create_dummy_assistant_groups()

    def delete_assistant_group(self, user, group_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistant/groups/{group_id}?team={team_id}"
            if team_id
            else f"/api/assistant/groups/{group_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_assistant_group_admin_no_team(self):
        response = self.delete_assistant_group(self.admin_user, group_id=self.assistant_group.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_group_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_assistant_group(
            self.admin_user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_group_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_assistant_group(
            user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_group_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_assistant_group(
            another_user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_assistant_group_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_assistant_group(
            user, group_id=self.assistant_group.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AssistantGroupUpdateTestCase(AssistantGroupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_dummy_assistant_groups()

    def update_assistant_group(self, user, group_id, data, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistant/groups/{group_id}?team={team_id}"
            if team_id
            else f"/api/assistant/groups/{group_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format="json")
        return response

    def test_update_assistant_group_admin_no_team(self):
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant_group(
            self.admin_user, group_id=self.assistant_group.id, data=new_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_assistant_group_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant_group(
            self.admin_user, group_id=self.assistant_group.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_assistant_group_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant_group(
            user, group_id=self.assistant_group.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_assistant_group_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant_group(
            another_user, group_id=self.assistant_group.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_assistant_group_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant_group(
            user, group_id=self.assistant_group.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])


class AssistantGroupListTestCase(AssistantGroupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_dummy_assistant_groups()

    def list_assistant_groups(self, user, team_id=None) -> HTTPResponse:
        url = f"/api/assistant/groups?team={team_id}" if team_id else "/api/assistant/groups"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_assistant_group_admin_no_team(self):
        response = self.list_assistant_groups(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_assistant_group_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_assistant_groups(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.assistant_group.name)

    def test_list_assistant_group_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_assistant_groups(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.assistant_group.name)

    def test_list_assistant_group_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_assistant_groups(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.assistant_group.name)

    def test_list_assistant_group_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_assistant_groups(another_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_assistant_group_team_filtering(self):
        another_user = self.regular_users[1]["user"]
        another_team = self.regular_users[1]["teams"][0]["team"]
        response = self.list_assistant_groups(another_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
