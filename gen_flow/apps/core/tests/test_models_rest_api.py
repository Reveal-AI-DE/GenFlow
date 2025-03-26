# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import TeamRole
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users
from gen_flow.apps.core.tests.utils import enable_provider
from urllib.parse import urlencode

class AIModelTestCase(APITestCase):
    def setUp(self):
        import gen_flow.apps.ai.tests.register_providers # noqa
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)
        self.data = {
            'provider_name': 'dummy',
            'encrypted_config': {
                'api_key': 'test'
            }
        }

class AIModelListTestCase(AIModelTestCase):
    def list_model(self, user, enabled_only: bool=False, model_type: str=None, team_id=None) -> HTTPResponse:
        query_params = {}
        if team_id:
            query_params['team'] = team_id
        if enabled_only:
            query_params['enabled_only'] = enabled_only
        if model_type:
            query_params['model_type'] = model_type

        url = f'/api/models?{urlencode(query_params)}' if query_params else '/api/models'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_model_all_admin_no_team(self):
        response = self.list_model(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_model_enabled_only_admin(self):
        response = self.list_model(self.admin_user, enabled_only=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_list_model_llm_admin(self):
        response = self.list_model(self.admin_user, model_type='llm')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_model_incorrect_model_type_admin(self):
        response = self.list_model(self.admin_user, model_type='llm2')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_model_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_model(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_model_enabled_only_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        response = self.list_model(user, team_id=team.id, enabled_only=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_list_model_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_model(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AIModelRetrieveTestCase(AIModelTestCase):
    def get_model(self, user, model_id: str, provider_name: str=None, team_id=None) -> HTTPResponse:
        query_params = {}
        if provider_name:
            query_params['provider_name'] = provider_name
        if team_id:
            query_params['team'] = team_id

        url = f'/api/models/{model_id}?{urlencode(query_params)}' if query_params else f'/api/models/{model_id}'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_get_model_admin_not_enabled(self):
        response = self.get_model(self.admin_user, 'model1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_model_admin(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_model(self.admin_user, 'model1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_model_user__not_enabled(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        response = self.get_model(user, 'model1', team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_model_user(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_model(user, 'model1', team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_model_user_forbidden(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_model(user, 'model1') # no team_id
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_model_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_model(user, 'model1', team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AIModelParameterConfigTestCase(AIModelTestCase):
    def get_parameter_config(self, user, model_id: str, provider_name: str=None, team_id=None) -> HTTPResponse:
        query_params = {}
        if provider_name:
            query_params['provider_name'] = provider_name
        if team_id:
            query_params['team'] = team_id

        url = f'/api/models/{model_id}/parameter_config?{urlencode(query_params)}' if query_params \
            else f'/api/models/{model_id}/parameter_config'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_get_parameter_admin_not_enabled(self):
        response = self.get_parameter_config(self.admin_user, 'model1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_parameter_admin(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_parameter_config(self.admin_user, 'model1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_parameter_user__not_enabled(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        response = self.get_parameter_config(user, 'model1', team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_parameter_user(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_parameter_config(user, 'model1', team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_parameter_user_forbidden(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_parameter_config(user, 'model1') # no team_id
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_parameter_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_parameter_config(user, 'model1', team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
