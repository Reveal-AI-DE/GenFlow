# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

from http.client import HTTPResponse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import TeamRole
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users
from gen_flow.apps.core.tests.utils import enable_provider
from gen_flow.apps.session.models import Session, SessionType
from gen_flow.apps.session.tests.utils import (create_dummy_prompt, create_dummy_session,
    SESSION_DATA, PROVIDER_DATA)


class SessionTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        import gen_flow.apps.ai.tests.register_providers # noqa
        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    @classmethod
    def create_sessions(cls):
        team = cls.regular_users[0]['teams'][0]['team']
        user = cls.regular_users[0]['user']
        # llm session
        data = SESSION_DATA.copy()
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)
        cls.llm_session = create_dummy_session(
            team=team,
            owner=user,
            data=data
        )
        # prompt session
        data = SESSION_DATA.copy()
        data['session_type'] = SessionType.PROMPT.value
        cls.prompt_session = create_dummy_session(
            team=team,
            owner=user,
            data=data
        )


class SessionCreateTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for item in cls.regular_users:
            user = item['user']
            for team_membership in item['teams']:
                team = team_membership['team']
                prompt = create_dummy_prompt(
                    team=team,
                    owner=user,
                )
                team_membership['prompt'] = prompt

    def create_session(self, user, data, team_id=None) -> HTTPResponse:
        url = f'/api/sessions?team={team_id}' if team_id else '/api/sessions'
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format='json')
        return response

    def test_create_session_admin_no_team(self):
        response = self.create_session(self.admin_user, SESSION_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_session_admin_validation_error(self):
        team = self.regular_users[0]['teams'][0]['team']
        another_prompt = self.regular_users[1]['teams'][0]['prompt']

        data = SESSION_DATA.copy()

        # type: llm but no related_model
        data['session_type'] = SessionType.LLM.value
        del data['related_model']
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # type: prompt but no related_prompt
        data['session_type'] = SessionType.PROMPT.value
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # type: llm but provider not enabled
        response = self.create_session(self.admin_user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # type: prompt but prompt not in team
        data['related_prompt'] = another_prompt.id
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_session_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        prompt = self.regular_users[0]['teams'][0]['prompt']
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        # type: llm
        response = self.create_session(self.admin_user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # type: prompt
        data = SESSION_DATA.copy()
        data['session_type'] = SessionType.PROMPT.value
        data['related_prompt'] = prompt.id
        response = self.create_session(self.admin_user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        prompt = self.regular_users[0]['teams'][0]['prompt']
        _ = enable_provider(team=team, owner=user, data=PROVIDER_DATA)

        # type: llm
        response = self.create_session(user, SESSION_DATA, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # type: prompt
        data = SESSION_DATA.copy()
        data['session_type'] = SessionType.PROMPT.value
        data['related_prompt'] = prompt.id
        response = self.create_session(user, data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_user_forbidden(self):
        user = self.regular_users[0]['user']
        # not team member
        another_team = self.regular_users[1]['teams'][0]['team']
        response = self.create_session(user, SESSION_DATA, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SessionRetrieveTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()

    def retrieve_session(self, user, session_id, team_id=None) -> HTTPResponse:
        url = f'/api/sessions/{session_id}?team={team_id}' if team_id else f'/api/sessions/{session_id}'
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
        self.assertEqual(response.data['name'], SESSION_DATA['name'])
        self.assertIsNotNone(response.data['related_prompt'])

    def test_retrieve_session_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        # llm session
        response = self.retrieve_session(self.admin_user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], SESSION_DATA['name'])
        self.assertIsNotNone(response.data['related_model'])

        # prompt session
        response = self.retrieve_session(self.admin_user, session_id=self.prompt_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], SESSION_DATA['name'])
        self.assertIsNotNone(response.data['related_prompt'])

    def test_retrieve_session_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        # llm session
        response = self.retrieve_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], SESSION_DATA['name'])
        self.assertIsNotNone(response.data['related_model'])

    def test_retrieve_session_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        # llm session
        response = self.retrieve_session(another_user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_session_user_team_member(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        # llm session
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.retrieve_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], SESSION_DATA['name'])
        self.assertIsNotNone(response.data['related_model'])


class SessionDeleteTestCase(SessionTestCase):
    def setUp(self):
        super().setUp()
        self.create_sessions()

    def delete_session(self, user, session_id, team_id=None) -> HTTPResponse:
        url = f'/api/sessions/{session_id}?team={team_id}' if team_id else f'/api/sessions/{session_id}'
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_session_admin_no_team(self):
        response = self.delete_session(self.admin_user, session_id=self.llm_session.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.llm_session.id).exists())
        self.assertFalse(osp.exists(self.llm_session.dirname))

    def test_delete_session_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        response = self.delete_session(self.admin_user, session_id=self.prompt_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.prompt_session.id).exists())
        self.assertFalse(osp.exists(self.prompt_session.dirname))

    def test_delete_session_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        response = self.delete_session(user, session_id=self.llm_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Session.objects.filter(id=self.llm_session.id).exists())
        self.assertFalse(osp.exists(self.llm_session.dirname))

    def test_delete_session_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        response = self.delete_session(another_user, session_id=self.prompt_session.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_session_user_owner(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        membership = self.regular_users[0]['teams'][0]['membership']
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
        url = f'/api/sessions/{session_id}?team={team_id}' if team_id else f'/api/sessions/{session_id}'
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format='json')
        return response

    def test_update_session_admin_no_team(self):
        new_data = {'name': 'Updated Session'}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(self.admin_user, session_id=self.llm_session.id, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # prompt session
        response = self.update_session(self.admin_user, session_id=self.prompt_session.id, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_update_session_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        new_data = {'name': 'Updated Session'}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(self.admin_user, session_id=self.llm_session.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

        # prompt session
        response = self.update_session(self.admin_user, session_id=self.prompt_session.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_update_session_user(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        new_data = {'name': 'Updated Session'}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(user, session_id=self.llm_session.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_update_session_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        new_data = {'name': 'Updated Session'}

        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(another_user, session_id=self.llm_session.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_session_user_owner(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        new_data = {'name': 'Updated Session'}
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        # llm session
        # will fail because team is not provided to get the enabled provider
        response = self.update_session(user, session_id=self.llm_session.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SessionListTestCase(SessionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_sessions()

    def list_sessions(self, user, team_id=None) -> HTTPResponse:
        url = f'/api/sessions?team={team_id}' if team_id else '/api/sessions'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_sessions_admin_no_team(self):
        response = self.list_sessions(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_sessions_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        response = self.list_sessions(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], self.llm_session.name)
        self.assertEqual(response.data['results'][1]['name'], self.prompt_session.name)

        team = self.regular_users[1]['teams'][0]['team']
        response = self.list_sessions(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_list_sessions_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        response = self.list_sessions(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_sessions_user_member(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_sessions(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_sessions_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        response = self.list_sessions(another_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_sessions_user_filtering(self):
        another_team = self.regular_users[1]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        response = self.list_sessions(another_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
