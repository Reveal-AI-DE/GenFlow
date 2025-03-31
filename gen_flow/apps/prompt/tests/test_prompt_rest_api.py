# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from http.client import HTTPResponse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import TeamRole
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users
from gen_flow.apps.core.tests.utils import enable_provider
from gen_flow.apps.prompt.tests.utils import create_prompt_group, create_prompt


class PromptTestCase(APITestCase):
    def setUp(self):
        import gen_flow.apps.ai.tests.register_providers # noqa
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)
        self.data = {
            'name': 'dummy',
            'description': 'dummy',
            'pre_prompt': 'dummy',
            'related_model': {
                'provider_name': 'dummy',
                'model_name': 'model2',
            },
        }
        self.create_data = {
            'name': 'dummy',
            'description': 'dummy',
            'pre_prompt': 'dummy',
        }
        self.provider_data = {
            'provider_name': 'dummy',
            'encrypted_config': {
                'api_key': 'test'
            }
        }
        for item in self.regular_users:
            user = item['user']
            for team_membership in item['teams']:
                team = team_membership['team']
                group = create_prompt_group(
                    team=team,
                    owner=user,
                    data={
                        'name': 'dummy',
                        'description': 'dummy',
                        'color': 'dummy',
                    }
                )
                team_membership['group'] = group


class PromptCreateTestCase(PromptTestCase):
    def create_prompt(self, user, data, team_id=None) -> HTTPResponse:
        url = f'/api/prompts?team={team_id}' if team_id else '/api/prompts'
        with ForceLogin(user, self.client):
            response = self.client.post(url, data, format='json')
        return response

    def test_create_prompt_admin_no_team(self):
        response = self.create_prompt(self.admin_user, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_prompt_admin_validation_error(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        another_group = self.regular_users[1]['teams'][0]['group']

        # no group, provider not enabled
        response = self.create_prompt(self.admin_user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['group_id'] = group.id
        # provider not enabled
        response = self.create_prompt(self.admin_user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        _ = enable_provider(team=team, owner=user, data=self.provider_data)
        # group not in team
        self.data['group_id'] = another_group.id
        response = self.create_prompt(self.admin_user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_prompt_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']

        self.data['group_id'] = group.id
        _ = enable_provider(team=team, owner=user, data=self.provider_data)

        response = self.create_prompt(self.admin_user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_prompt_user_validation_error(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        another_group = self.regular_users[1]['teams'][0]['group']

        # no group, provider not enabled
        response = self.create_prompt(user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['group_id'] = group.id
        # provider not enabled
        response = self.create_prompt(user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        _ = enable_provider(team=team, owner=user, data=self.provider_data)
        # group not in team
        self.data['group_id'] = another_group.id
        response = self.create_prompt(user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_prompt_user_forbidden(self):
        user = self.regular_users[0]['user']
        # not team member
        another_team = self.regular_users[1]['teams'][0]['team']
        response = self.create_prompt(user, self.data, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_prompt_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']

        self.data['group_id'] = group.id
        _ = enable_provider(team=team, owner=user, data=self.provider_data)

        response = self.create_prompt(user, self.data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PromptRetrieveTestCase(PromptTestCase):
    def retrieve_prompt(self, user, prompt_id, team_id=None) -> HTTPResponse:
        url = f'/api/prompts/{prompt_id}?team={team_id}' if team_id else f'/api/prompts/{prompt_id}'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
        return response

    def test_retrieve_prompt_admin_no_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.retrieve_prompt(self.admin_user, prompt_id=prompt.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.create_data['name'])
        self.assertFalse(response.data['is_pinned'])

    def test_retrieve_prompt_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        _ = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=self.admin_user, data=self.create_data)
        response = self.retrieve_prompt(self.admin_user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_pinned'])

    def test_retrieve_prompt_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.retrieve_prompt(user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_pinned'])

    def test_retrieve_prompt_group_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        another_user = self.regular_users[1]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.retrieve_prompt(another_user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_prompt_group_team_member(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.retrieve_prompt(user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.data['name'])


class PromptDeleteTestCase(PromptTestCase):
    def delete_prompt(self, user, prompt_id, team_id=None) -> HTTPResponse:
        url = f'/api/prompts/{prompt_id}?team={team_id}' if team_id else f'/api/prompts/{prompt_id}'
        with ForceLogin(user, self.client):
            response = self.client.delete(url)
        return response

    def test_delete_prompt_admin_no_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.delete_prompt(self.admin_user, prompt_id=prompt.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_prompt_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.delete_prompt(self.admin_user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_prompt_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.delete_prompt(user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_prompt_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        another_user = self.regular_users[1]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.delete_prompt(another_user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_prompt_user_owner(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.delete_prompt(user, prompt_id=prompt.id, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PromptUpdateTestCase(PromptTestCase):
    def update_prompt(self, user, prompt_id, data, team_id=None) -> HTTPResponse:
        url = f'/api/prompts/{prompt_id}?team={team_id}' if team_id else f'/api/prompts/{prompt_id}'
        with ForceLogin(user, self.client):
            response = self.client.patch(url, data, format='json')
        return response

    def test_update_prompt_admin_no_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        new_data = {
            'name': 'new name',
        }
        response = self.update_prompt(self.admin_user, prompt_id=prompt.id, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_update_prompt_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        new_data = {
            'name': 'new name',
        }
        response = self.update_prompt(self.admin_user, prompt_id=prompt.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_update_prompt_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        new_data = {
            'name': 'new name',
        }
        response = self.update_prompt(user, prompt_id=prompt.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_update_prompt_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        another_user = self.regular_users[1]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        new_data = {
            'name': 'new name',
        }
        response = self.update_prompt(another_user, prompt_id=prompt.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_prompt_user_owner(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        new_data = {
            'name': 'new name',
        }
        response = self.update_prompt(user, prompt_id=prompt.id, data=new_data, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])


class PromptListTestCase(PromptTestCase):
    def list_prompt(self, user, team_id=None) -> HTTPResponse:
        url = f'/api/prompts?team={team_id}' if team_id else '/api/prompts'
        with ForceLogin(user, self.client):
            response = self.client.get(url)
            return response

    def test_list_prompt_admin_no_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        _ = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.list_prompt(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_prompt_admin(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.list_prompt(self.admin_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], prompt.name)

    def test_list_prompt_user(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.list_prompt(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], prompt.name)

    def test_list_prompt_user_member(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        prompt = create_prompt(team=team, owner=user, data=self.create_data)
        membership = self.regular_users[0]['teams'][0]['membership']
        membership.role = TeamRole.MEMBER.value
        membership.save()
        response = self.list_prompt(user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], prompt.name)

    def test_list_prompt_user_another_team(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        another_user = self.regular_users[1]['user']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        _ = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.list_prompt(another_user, team_id=team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_prompt_team_filtering(self):
        team = self.regular_users[0]['teams'][0]['team']
        user = self.regular_users[0]['user']
        another_user = self.regular_users[1]['user']
        another_team = self.regular_users[1]['teams'][0]['team']
        group = self.regular_users[0]['teams'][0]['group']
        self.create_data['group_id'] = group.id
        _ = create_prompt(team=team, owner=user, data=self.create_data)
        response = self.list_prompt(another_user, team_id=another_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
