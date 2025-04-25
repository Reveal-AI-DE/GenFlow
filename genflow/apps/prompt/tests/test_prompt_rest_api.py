# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.core.tests.utils import enable_provider
from genflow.apps.prompt.tests.utils import (
    PROMPT_DATA,
    PROMPT_GROUP_DATA,
    PROVIDER_DATA,
    create_dummy_prompt,
    create_dummy_prompt_group,
)
from genflow.apps.team.models import TeamRole
from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class PromptTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # pylint: disable=unused-import
        import genflow.apps.ai.tests.register_providers  # noqa

        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    @classmethod
    def create_prompts(cls):
        team = cls.regular_users[0]["teams"][0]["team"]
        user = cls.regular_users[0]["user"]
        data = PROMPT_DATA.copy()
        del data["related_model"]
        cls.prompt = create_dummy_prompt(team=team, owner=user, data=data)


class PromptCreateTestCase(PromptTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for item in cls.regular_users:
            user = item["user"]
            for team_membership in item["teams"]:
                team = team_membership["team"]
                group = create_dummy_prompt_group(team=team, owner=user, data=PROMPT_GROUP_DATA)
                team_membership["group"] = group

    def create_prompt(self, user, data, team_id=None) -> HTTPResponse:
        url = f"/api/prompts?team={team_id}" if team_id else "/api/prompts"
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format="json")
        return response

    def test_create_prompt_admin_no_team(self):
        response = self.create_prompt(self.admin_user, PROMPT_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_prompt_admin_validation_error(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]
        another_group = self.regular_users[1]["teams"][0]["group"]

        # no group, provider not enabled
        response = self.create_prompt(self.admin_user, PROMPT_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = PROMPT_DATA.copy()
        data["group_id"] = group.id
        # provider not enabled
        response = self.create_prompt(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        # group not in team
        data["group_id"] = another_group.id
        response = self.create_prompt(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_prompt_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]

        data = PROMPT_DATA.copy()
        data["group_id"] = group.id
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        response = self.create_prompt(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_prompt_user_validation_error(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]
        another_group = self.regular_users[1]["teams"][0]["group"]

        # no group, provider not enabled
        response = self.create_prompt(user, PROMPT_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = PROMPT_DATA.copy()
        data["group_id"] = group.id
        # provider not enabled
        response = self.create_prompt(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        # group not in team
        data["group_id"] = another_group.id
        response = self.create_prompt(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_prompt_user_forbidden(self):
        user = self.regular_users[0]["user"]
        # not team member
        another_team = self.regular_users[1]["teams"][0]["team"]
        response = self.create_prompt(user, PROMPT_DATA, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_prompt_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]

        data = PROMPT_DATA.copy()
        data["group_id"] = group.id
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        response = self.create_prompt(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(GF_LIMITS={"PROMPT": 0})
    def test_create_prompt_user_user_check_limit(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.create_prompt(user, PROMPT_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(GF_LIMITS={"PROMPT": 1})
    def test_create_prompt_user_user_another_team_check_limit(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]

        # create prompt to reach limit
        data = PROMPT_DATA.copy()
        del data["related_model"]
        create_dummy_prompt(team=team, owner=user, data=data)

        team = self.regular_users[1]["teams"][0]["team"]
        user = self.regular_users[1]["user"]
        group = self.regular_users[1]["teams"][0]["group"]

        data = PROMPT_DATA.copy()
        data["group_id"] = group.id
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        response = self.create_prompt(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PromptRetrieveTestCase(PromptTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_prompts()

    def retrieve_prompt(self, user, prompt_id, team_id=None) -> HTTPResponse:
        url = f"/api/prompts/{prompt_id}?team={team_id}" if team_id else f"/api/prompts/{prompt_id}"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_retrieve_prompt_admin_no_team(self):
        response = self.retrieve_prompt(self.admin_user, prompt_id=self.prompt.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], PROMPT_DATA["name"])
        self.assertFalse(response.data["is_pinned"])

    def test_retrieve_prompt_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.retrieve_prompt(self.admin_user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_pinned"])

    def test_retrieve_prompt_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.retrieve_prompt(user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_pinned"])

    def test_retrieve_prompt_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.retrieve_prompt(another_user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_prompt_team_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.retrieve_prompt(user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], PROMPT_DATA["name"])


class PromptDeleteTestCase(PromptTestCase):
    def setUp(self):
        super().setUp()
        self.create_prompts()

    def delete_prompt(self, user, prompt_id, team_id=None) -> HTTPResponse:
        url = f"/api/prompts/{prompt_id}?team={team_id}" if team_id else f"/api/prompts/{prompt_id}"
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_prompt_admin_no_team(self):
        response = self.delete_prompt(self.admin_user, prompt_id=self.prompt.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_prompt_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_prompt(self.admin_user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_prompt_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_prompt(user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_prompt_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_prompt(another_user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_prompt_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_prompt(user, prompt_id=self.prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PromptUpdateTestCase(PromptTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_prompts()

    def update_prompt(self, user, prompt_id, data, team_id=None) -> HTTPResponse:
        url = f"/api/prompts/{prompt_id}?team={team_id}" if team_id else f"/api/prompts/{prompt_id}"
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format="json")
        return response

    def test_update_prompt_admin_no_team(self):
        new_data = {
            "name": "new name",
        }
        response = self.update_prompt(self.admin_user, prompt_id=self.prompt.id, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_prompt_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        new_data = {
            "name": "new name",
        }
        response = self.update_prompt(
            self.admin_user, prompt_id=self.prompt.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_prompt_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        new_data = {
            "name": "new name",
        }
        response = self.update_prompt(
            user, prompt_id=self.prompt.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_prompt_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        new_data = {
            "name": "new name",
        }
        response = self.update_prompt(
            another_user, prompt_id=self.prompt.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_prompt_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        new_data = {
            "name": "new name",
        }
        response = self.update_prompt(
            user, prompt_id=self.prompt.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])


class PromptListTestCase(PromptTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_prompts()

    def list_prompt(self, user, team_id=None) -> HTTPResponse:
        url = f"/api/prompts?team={team_id}" if team_id else "/api/prompts"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_prompt_admin_no_team(self):
        response = self.list_prompt(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_prompt_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_prompt(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.prompt.name)

    def test_list_prompt_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_prompt(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.prompt.name)

    def test_list_prompt_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_prompt(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.prompt.name)

    def test_list_prompt_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_prompt(another_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_prompt_team_filtering(self):
        another_user = self.regular_users[1]["user"]
        another_team = self.regular_users[1]["teams"][0]["team"]
        response = self.list_prompt(another_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
