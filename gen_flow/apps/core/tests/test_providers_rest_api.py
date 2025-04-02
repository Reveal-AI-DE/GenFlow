# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import TeamRole
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users
from gen_flow.apps.core.tests.utils import enable_provider


class ProviderTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        import gen_flow.apps.ai.tests.register_providers # noqa
        super().setUpClass()
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)
        cls.data = {
            'provider_name': 'dummy',
            'encrypted_config': {
                'api_key': 'test'
            }
        }


class ProviderCreateTestCase(ProviderTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'provider_name': 'dummy',
            'credentials': {
                'api_key': 'test'
            }
        }
    def enable_provider(self, user, data, team_id=None) -> HTTPResponse:
        url = f'/api/providers?team={team_id}' if team_id else '/api/providers'
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format='json')
        return response

    def test_enable_provider_no_team(self):
        response = self.enable_provider(self.admin_user, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enable_provider_invalid_credentials(self):
        team_id = self.regular_users[0]['teams'][0]['team'].id
        data = self.data.copy()
        data['credentials'] = {}
        response = self.enable_provider(self.admin_user, data, team_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enable_provider_admin(self):
        team_id = self.regular_users[0]['teams'][0]['team'].id
        response = self.enable_provider(self.admin_user, self.data, team_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_enable_provider_user(self):
        user = self.regular_users[0]['user']
        team_id = self.regular_users[0]['teams'][0]['team'].id
        response = self.enable_provider(user, self.data, team_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_enable_provider_user_forbidden(self):
        user = self.regular_users[0]['user']
        team_id = self.regular_users[1]['teams'][0]['team'].id
        response = self.enable_provider(user, self.data, team_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_enable_provider_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.enable_provider(user, self.data, team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProviderRetrieveTestCase(ProviderTestCase):
    def get_provider(self, user, provider_id) -> HTTPResponse:
        url = f'/api/providers/{provider_id}'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_get_provider_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.get_provider(self.admin_user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_provider_user(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_provider(user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_provider_user_forbidden(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        provider = enable_provider(team=team, owner=user, data=self.data)
        response = self.get_provider(another_user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_provider_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.get_provider(user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProviderDestroyTestCase(ProviderTestCase):
    def delete_provider(self, user, provider_id) -> HTTPResponse:
        url = f'/api/providers/{provider_id}'
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_provider_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.delete_provider(self.admin_user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_provider_user(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=user, data=self.data)
        response = self.delete_provider(user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_provider_user_forbidden(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        provider = enable_provider(team=team, owner=user, data=self.data)
        response = self.delete_provider(another_user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_provider_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.delete_provider(user, provider.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProviderUpdateTestCase(ProviderTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.updated_data = {
            'provider_name': 'dummy',
            'credentials': {
                'api_key': 'updated_test'
            }
        }

    def update_provider(self, user, provider_id, data, team_id=None) -> HTTPResponse:
        url = f'/api/providers/{provider_id}?team={team_id}' if team_id else f'/api/providers/{provider_id}'
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format='json')
        return response

    def test_update_provider_no_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.update_provider(self.admin_user, provider.id, self.updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_provider_invalid_credentials(self):
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        self.updated_data = {
            'provider_name': 'dummy',
            'credentials': {}
        }
        response = self.update_provider(self.admin_user, provider.id, self.updated_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_provider_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.update_provider(self.admin_user, provider.id, self.updated_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_provider_user(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        provider = enable_provider(team=team, owner=user, data=self.data)
        response = self.update_provider(user, provider.id, self.updated_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_provider_user_forbidden(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        another_user = self.regular_users[1]['user']
        provider = enable_provider(team=team, owner=user, data=self.data)
        response = self.update_provider(another_user, provider.id, self.updated_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_provider_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        provider = enable_provider(team=team, owner=self.admin_user, data=self.data)
        response = self.update_provider(user, provider.id, self.updated_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProviderListTestCase(ProviderTestCase):
    def list_provider(self, user, team_id=None) -> HTTPResponse:
        url = f'/api/providers?team={team_id}' if team_id else f'/api/providers'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_list_provider_admin_no_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_provider(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(response.data['results'][0]['user_configuration']['active'])

    def test_list_provider_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_provider(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(response.data['results'][0]['user_configuration']['active'])

    def test_list_provider_admin_different_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        _ = enable_provider(team=team, owner=user, data=self.data)
        another_team = self.regular_users[1]['teams'][0]['team']
        response = self.list_provider(self.admin_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertFalse(response.data['results'][0]['user_configuration']['active'])

    def test_list_provider_user_no_team(self):
        user = team = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_provider(user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_provider_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_provider(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(response.data['results'][0]['user_configuration']['active'])

    def test_list_provider_user_different_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        _ = enable_provider(team=team, owner=user, data=self.data)
        another_team = self.regular_users[1]['teams'][0]['team']
        response = self.list_provider(user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list_provider_user_not_owner(self):
        user = self.regular_users[0]['user']
        team = self.regular_users[0]['teams'][0]['team']
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        _ = enable_provider(team=team, owner=user, data=self.data)
        response = self.list_provider(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
