# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import os
from http.client import HTTPResponse
from os import path as osp
from pathlib import Path

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.common.entities import FileEntity
from genflow.apps.core.tests.utils import enable_provider
from genflow.apps.prompt.tests.utils import PROVIDER_DATA
from genflow.apps.restriction.tests.utils import override_limit
from genflow.apps.session.models import Session, SessionType
from genflow.apps.session.tests.utils import (
    SESSION_DATA,
    create_dummy_session,
    create_related_prompt,
)
from genflow.apps.team.models import TeamRole
from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class SessionTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # pylint: disable=unused-import
        import genflow.apps.ai.tests.register_providers  # noqa

        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    @classmethod
    def create_sessions(cls):
        team = cls.regular_users[0]["teams"][0]["team"]
        user = cls.regular_users[0]["user"]
        # llm session
        data = SESSION_DATA.copy()
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        cls.llm_session = create_dummy_session(team=team, owner=user, data=data)
        # prompt session
        data = SESSION_DATA.copy()
        data["session_type"] = SessionType.PROMPT.value
        cls.prompt_session = create_dummy_session(team=team, owner=user, data=data)

    @classmethod
    def create_files(cls, files_count):
        os.makedirs(cls.llm_session.dirname, exist_ok=True)
        cls.files = []
        for i in range(files_count):
            file = FileEntity(id=f"test_file_{i}.txt", path=cls.llm_session.dirname)
            file.path = osp.join(cls.llm_session.dirname, file.id)
            # create file
            with open(file.path, "w") as f:
                f.write("fake content")
            cls.files.append(file)


class SessionCreateTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for item in cls.regular_users:
            user = item["user"]
            for team_membership in item["teams"]:
                team = team_membership["team"]
                prompt = create_related_prompt(
                    team=team,
                    owner=user,
                )
                team_membership["prompt"] = prompt

    def create_session(self, user, data, team_id=None) -> HTTPResponse:
        url = f"/api/sessions?team={team_id}" if team_id else "/api/sessions"
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format="json")
        return response

    def test_create_session_admin_no_team(self):
        response = self.create_session(self.admin_user, SESSION_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_session_admin_validation_error(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_prompt = self.regular_users[1]["teams"][0]["prompt"]

        data = SESSION_DATA.copy()

        # type: llm but no related_model
        data["session_type"] = SessionType.LLM.value
        del data["related_model"]
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # type: prompt but no related_prompt
        data["session_type"] = SessionType.PROMPT.value
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # type: llm but provider not enabled
        response = self.create_session(self.admin_user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # type: prompt but prompt not in team
        data["related_prompt"] = another_prompt.id
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_session_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        prompt = self.regular_users[0]["teams"][0]["prompt"]
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        # type: llm
        response = self.create_session(self.admin_user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # type: prompt
        data = SESSION_DATA.copy()
        data["session_type"] = SessionType.PROMPT.value
        data["related_prompt"] = prompt.id
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        prompt = self.regular_users[0]["teams"][0]["prompt"]
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        # type: llm
        response = self.create_session(user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # type: prompt
        data = SESSION_DATA.copy()
        data["session_type"] = SessionType.PROMPT.value
        data["related_prompt"] = prompt.id
        response = self.create_session(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_user_forbidden(self):
        user = self.regular_users[0]["user"]
        # not team member
        another_team = self.regular_users[1]["teams"][0]["team"]
        response = self.create_session(user, SESSION_DATA, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_session_user_check_global_limit(self):
        override_limit(
            key="SESSION",
            value=0,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        response = self.create_session(user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_session_user_check_limit_global_another_team(self):
        override_limit(
            key="SESSION",
            value=1,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]

        # create session to reach limit
        data = SESSION_DATA.copy()
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        create_dummy_session(team=team, owner=user, data=data)

        team = self.regular_users[1]["teams"][0]["team"]
        user = self.regular_users[1]["user"]
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        response = self.create_session(user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SessionRetrieveTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()

    def retrieve_session(self, user, session_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_retrieve_session_admin_no_team(self):
        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.retrieve_session(self.admin_user, session_id=self.llm_session.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # prompt session
        response = self.retrieve_session(self.admin_user, session_id=self.prompt_session.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], SESSION_DATA["name"])
        self.assertIsNotNone(response.data["related_prompt"])

    def test_retrieve_session_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        # llm session
        response = self.retrieve_session(
            self.admin_user, session_id=self.llm_session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], SESSION_DATA["name"])
        self.assertIsNotNone(response.data["related_model"])

        # prompt session
        response = self.retrieve_session(
            self.admin_user, session_id=self.prompt_session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], SESSION_DATA["name"])
        self.assertIsNotNone(response.data["related_prompt"])

    def test_retrieve_session_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        # llm session
        response = self.retrieve_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], SESSION_DATA["name"])
        self.assertIsNotNone(response.data["related_model"])

    def test_retrieve_session_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        # llm session
        response = self.retrieve_session(
            another_user, session_id=self.llm_session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_session_user_team_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        # llm session
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.retrieve_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], SESSION_DATA["name"])
        self.assertIsNotNone(response.data["related_model"])


class SessionDeleteTestCase(SessionTestCase):
    def setUp(self):
        super().setUp()
        self.create_sessions()

    def delete_session(self, user, session_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_session_admin_no_team(self):
        response = self.delete_session(self.admin_user, session_id=self.llm_session.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.llm_session.id).exists())
        self.assertFalse(osp.exists(self.llm_session.dirname))

    def test_delete_session_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_session(
            self.admin_user, session_id=self.prompt_session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.prompt_session.id).exists())
        self.assertFalse(osp.exists(self.prompt_session.dirname))

    def test_delete_session_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.llm_session.id).exists())
        self.assertFalse(osp.exists(self.llm_session.dirname))

    def test_delete_session_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_session(
            another_user, session_id=self.prompt_session.id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_session_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.llm_session.id).exists())
        self.assertFalse(osp.exists(self.llm_session.dirname))


class SessionUpdateTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()

    def update_session(self, user, session_id, data, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}"
        )
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format="json")
        return response

    def test_update_session_admin_no_team(self):
        new_data = {"name": "Updated Session"}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(
            self.admin_user, session_id=self.llm_session.id, data=new_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # prompt session
        response = self.update_session(
            self.admin_user, session_id=self.prompt_session.id, data=new_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_session_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        new_data = {"name": "Updated Session"}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(
            self.admin_user, session_id=self.llm_session.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

        # prompt session
        response = self.update_session(
            self.admin_user, session_id=self.prompt_session.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_session_user(self):
        user = self.regular_users[0]["user"]
        team = self.regular_users[0]["teams"][0]["team"]
        new_data = {"name": "Updated Session"}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(
            user, session_id=self.llm_session.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

    def test_update_session_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        new_data = {"name": "Updated Session"}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(
            another_user, session_id=self.llm_session.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_session_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        new_data = {"name": "Updated Session"}
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(
            user, session_id=self.llm_session.id, data=new_data, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SessionListTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()

    def list_sessions(self, user, team_id=None) -> HTTPResponse:
        url = f"/api/sessions?team={team_id}" if team_id else "/api/sessions"
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_sessions_admin_no_team(self):
        response = self.list_sessions(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_sessions_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_sessions(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["name"], self.llm_session.name)
        self.assertEqual(response.data["results"][1]["name"], self.prompt_session.name)

        team = self.regular_users[1]["teams"][0]["team"]
        response = self.list_sessions(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_list_sessions_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_sessions(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_sessions_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_sessions(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_sessions_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_sessions(another_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_sessions_user_filtering(self):
        another_team = self.regular_users[1]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_sessions(another_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


@override_settings(BASE_DIR=str(Path(__file__).parents[4]))
class SessionListFilesTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()
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

    def list_files(self, user, session_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}/files?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}/files"
        )
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_files_admin_no_team(self):
        response = self.list_files(self.admin_user, self.llm_session.id)
        # session team
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.list_files(self.admin_user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.list_files(user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_files(user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_list_files_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.list_files(another_user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@override_settings(BASE_DIR=str(Path(__file__).parents[4]))
class SessionUploadFileTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()
        cls.file = FileEntity(id=f"test_file.txt", path=cls.llm_session.dirname)
        cls.file.path = osp.join(cls.llm_session.dirname, cls.file.id)
        # create file
        cls.path = osp.join(settings.SESSIONS_ROOT, cls.file.id)
        with open(cls.path, "w") as f:
            f.write("fake content")

    def check_data(self, response):
        self.assertEqual(response.data["id"], self.file.id)
        self.assertEqual(response.data["path"], self.file.path)
        os.remove(self.file.path)

    def upload_file(self, user, session_id, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}/upload_file?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}/upload_file"
        )
        with ForceLogin(user, self.client):
            with open(self.path, "rb") as file:
                response = self.client.post(url, {"file": file}, format="multipart")
        return response

    def test_upload_file_admin_no_team(self):
        response = self.upload_file(self.admin_user, self.llm_session.id)
        # session team
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.upload_file(self.admin_user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_user_member(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.upload_file(user, self.llm_session.id, team_id=team.id)
        # session owner
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_data(response)

    def test_upload_file_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.upload_file(another_user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_file_user_check_files_global_limit(self):
        override_limit(
            key="MAX_FILES_PER_SESSION",
            value=0,
        )
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(GF_LIMITS={"MAX_FILE_SIZE": 0, "FILE_SUPPORTED_TYPES": ["text/plain"]})
    def test_upload_file_user_check_size(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(
        GF_LIMITS={"MAX_FILES_PER_SESSION": 2, "MAX_FILE_SIZE": 1, "FILE_SUPPORTED_TYPES": []}
    )
    def test_upload_file_user_check_type(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.upload_file(user, self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(BASE_DIR=str(Path(__file__).parents[4]))
class SessionDeleteFileTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()

    def setUp(self):
        super().setUp()
        self.create_files(2)

    def delete_file(self, user, session_id, filename, team_id=None) -> HTTPResponse:
        url = (
            f"/api/sessions/{session_id}/files/{filename}?team={team_id}"
            if team_id
            else f"/api/sessions/{session_id}/files/{filename}"
        )
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_file_admin_no_team(self):
        response = self.delete_file(self.admin_user, self.llm_session.id, self.files[0].id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))

    def test_delete_file_admin(self):
        team = self.regular_users[0]["teams"][0]["team"]
        response = self.delete_file(
            self.admin_user, self.llm_session.id, self.files[0].id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))

    def test_delete_file_user(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_file(user, self.llm_session.id, self.files[0].id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))

    def test_delete_file_user_invalid_filename(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        response = self.delete_file(
            user, self.llm_session.id, f"{self.files[0].id}-invalid", team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(osp.exists(self.files[0].path))

    def test_delete_file_user_another_team(self):
        team = self.regular_users[0]["teams"][0]["team"]
        another_user = self.regular_users[1]["user"]
        response = self.delete_file(
            another_user, self.llm_session.id, self.files[0].id, team_id=team.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(osp.exists(self.files[0].path))

    def test_delete_file_user_owner(self):
        team = self.regular_users[0]["teams"][0]["team"]
        user = self.regular_users[0]["user"]
        membership = self.regular_users[0]["teams"][0]["membership"]
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_file(user, self.llm_session.id, self.files[0].id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not osp.exists(self.files[0].path))
