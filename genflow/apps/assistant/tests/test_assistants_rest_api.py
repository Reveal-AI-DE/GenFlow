# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
from http.client import HTTPResponse
from os import path as osp
from pathlib import Path

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.assistant.tests.utils import (
    ASSISTANT_DATA,
    ASSISTANT_GROUP_DATA,
    create_dummy_assistant,
    create_dummy_assistant_group,
)
from genflow.apps.common.entities import FileEntity
from genflow.apps.core.tests.utils import enable_provider
from genflow.apps.prompt.tests.utils import PROVIDER_DATA
from genflow.apps.restriction.tests.utils import override_limit
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

    @classmethod
    def create_files(cls, files_count):
        os.makedirs(cls.assistant.dirname, exist_ok=True)
        cls.files = []
        for i in range(files_count):
            file = FileEntity(id=f"test_file_{i}.txt", path=cls.assistant.dirname)
            file.path = osp.join(cls.assistant.dirname, file.id)
            # create file
            with open(file.path, "w") as f:
                f.write("fake content")
            cls.files.append(file)


class AssistantCreateTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for item in cls.regular_users:
            user = item["user"]
            for team_membership in item["teams"]:
                team = team_membership["team"]
                group = create_dummy_assistant_group(
                    team=team, owner=user, data=ASSISTANT_GROUP_DATA
                )
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

    def test_create_assistant_user_user_check_global_limit(self):
        override_limit(
            key="ASSISTANT",
            value=0,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        group = self.regular_users[0]["teams"][0]["group"]

        data = ASSISTANT_DATA.copy()
        data["group_id"] = group.id
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        response = self.create_assistant(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_assistant_user_user_another_team_check_global_limit(self):
        override_limit(
            key="ASSISTANT",
            value=1,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]

        # create assistant to reach limit
        data = ASSISTANT_DATA.copy()
        del data["related_model"]
        create_dummy_assistant(team=team, owner=user, data=data)

        team = self.regular_users[1]["teams"][0]["team"]
        user = self.regular_users[1]["user"]
        group = self.regular_users[1]["teams"][0]["group"]

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
        url = (
            f"/api/assistants/{assistant_id}?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}"
        )
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
        response = self.retrieve_assistant(
            self.admin_user, assistant_id=self.assistant.id, team_id=team.id
        )
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
        response = self.retrieve_assistant(
            another_user, assistant_id=self.assistant.id, team_id=team.id
        )
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
        url = (
            f"/api/assistants/{assistant_id}?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_assistant_admin_no_team(self):
        response = self.delete_assistant(self.admin_user, assistant_id=self.assistant.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_assistant(
            self.admin_user, assistant_id=self.assistant.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_assistant(user, assistant_id=self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assistant_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_assistant(
            another_user, assistant_id=self.assistant.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_assistant_user_owner(self):
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
        url = (
            f"/api/assistants/{assistant_id}?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format="json")
        return response

    def test_update_assistant_admin_no_team(self):
        new_data = {
            "name": "new name",
        }
        response = self.update_assistant(
            self.admin_user, assistant_id=self.assistant.id, data=new_data
        )
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


class AssistantUploadAvatarTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()
        cls.avatar_path = osp.join(settings.BASE_DIR, "test_avatar.png")
        # create avatar
        with open(cls.avatar_path, "wb") as f:
            f.write(b"fake image content")

    def upload_avatar(self, user, assistant_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistants/{assistant_id}/upload_avatar?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}/upload_avatar"
        )
        with ForceLogin(user, self.client):
            with open(self.avatar_path, "rb") as avatar:
                response = self.client.post(url, {"avatar": avatar}, format="multipart")
        return response

    def test_upload_avatar_admin_no_team(self):
        response = self.upload_avatar(self.admin_user, self.assistant.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_avatar_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.upload_avatar(self.admin_user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_avatar_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_avatar(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_avatar_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.upload_avatar(user, self.assistant.id, team_id=team.id)
        # assistant owner
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_avatar_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.upload_avatar(another_user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(GF_LIMITS={"MAX_AVATAR_SIZE": 0, "AVATAR_SUPPORTED_TYPES": ["image/png"]})
    def test_upload_avatar_user_check_size(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_avatar(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(GF_LIMITS={"MAX_AVATAR_SIZE": 1, "AVATAR_SUPPORTED_TYPES": []})
    def test_upload_avatar_user_check_type(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_avatar(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(BASE_DIR=str(Path(__file__).parents[4]))
class AssistantListFilesTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()
        # create file
        cls.create_files(2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        for file in cls.files:
            if osp.exists(file.path):
                os.remove(file.path)

    def check_data(self, response):
        self.assertEqual(response.data["count"], 2)
        self.assertIn(response.data["results"][0]["id"], [file.id for file in self.files])
        self.assertIn(response.data["results"][0]["path"], [file.path for file in self.files])

    def list_files(self, user, assistant_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistants/{assistant_id}/files?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}/files"
        )
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_files_admin_no_team(self):
        response = self.list_files(self.admin_user, self.assistant.id)
        # assistant team
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_files(self.admin_user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_files(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_files(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_files(another_user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@override_settings(BASE_DIR=str(Path(__file__).parents[4]))
class AssistantUploadFileTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()
        cls.file = FileEntity(id=f"test_file.txt", path=cls.assistant.dirname)
        cls.file.path = osp.join(cls.assistant.dirname, cls.file.id)
        # create file
        cls.path = osp.join(settings.ASSISTANTS_ROOT, cls.file.id)
        with open(cls.path, "w") as f:
            f.write("fake content")

    def check_data(self, response):
        self.assertEqual(response.data["id"], self.file.id)
        self.assertEqual(response.data["path"], self.file.path)
        os.remove(self.file.path)

    def upload_file(self, user, assistant_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistants/{assistant_id}/upload_file?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}/upload_file"
        )
        with ForceLogin(user, self.client):
            with open(self.path, "rb") as file:
                response = self.client.post(url, {"file": file}, format="multipart")
        return response

    def test_upload_file_admin_no_team(self):
        response = self.upload_file(self.admin_user, self.assistant.id)
        # assistant team
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.upload_file(self.admin_user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.upload_file(user, self.assistant.id, team_id=team.id)
        # assistant owner
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.upload_file(another_user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_file_user_check_files_global_limit(self):
        override_limit(
            key="MAX_FILES_PER_ASSISTANT",
            value=0,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(GF_LIMITS={"MAX_FILE_SIZE": 0, "FILE_SUPPORTED_TYPES": ["text/plain"]})
    def test_upload_file_user_check_size(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(
        GF_LIMITS={"MAX_FILES_PER_ASSISTANT": 2, "MAX_FILE_SIZE": 1, "FILE_SUPPORTED_TYPES": []}
    )
    def test_upload_file_user_check_type(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.assistant.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(BASE_DIR=str(Path(__file__).parents[4]))
class AssistantDeleteFileTestCase(AssistantTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_assistants()

    def setUp(self):
        super().setUp()
        self.create_files(2)

    def delete_file(self, user, assistant_id, filename, team_id=None) -> HTTPResponse:
        url = (
            f"/api/assistants/{assistant_id}/files/{filename}?team={team_id}"
            if team_id
            else f"/api/assistants/{assistant_id}/files/{filename}"
        )
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_file_admin_no_team(self):
        response = self.delete_file(self.admin_user, self.assistant.id, self.files[0].id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))

    def test_delete_file_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_file(
            self.admin_user, self.assistant.id, self.files[0].id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))

    def test_delete_file_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_file(user, self.assistant.id, self.files[0].id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))

    def test_delete_file_user_invalid_filename(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_file(
            user, self.assistant.id, f"{self.files[0].id}-invalid", team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(osp.exists(self.files[0].path))

    def test_delete_file_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_file(
            another_user, self.assistant.id, self.files[0].id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(osp.exists(self.files[0].path))

    def test_delete_file_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_file(user, self.assistant.id, self.files[0].id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))
