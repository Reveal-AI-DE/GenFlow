# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import Team
from gen_flow.apps.team.serializers import TeamReadSerializer
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users, USERS


class TeamAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)

    def check_response(self, response, status_code, data=None):
        self.assertEqual(response.status_code, status_code)
        if data:
            self.assertEqual(response.data['name'], data['name'])
            self.assertEqual(response.data['description'], data['description'])


class TeamListAPITestCase(TeamAPITestCase):
    def setUp(self):
        super().setUp()
        self.created_teams_count = sum([len(user['teams']) for user in self.regular_users])

    def list_teams(self, user):
        with ForceLogin(user, self.client):
            response = self.client.get('/api/teams')
        return response

    def test_list_teams_admin(self):
        response = self.list_teams(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.created_teams_count)


class TeamCreateAPITestCase(TeamAPITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users()

    def create_team(self, user, data):
        with ForceLogin(user, self.client):
            response = self.client.post('/api/teams', data, format='json')
        return response

    def test_create_team_admin(self):
        for user in USERS['users']:
            for team in user['teams']:
                response = self.create_team(self.admin_user, team)
                self.check_response(response, status.HTTP_201_CREATED, data=team)


class TeamRetrieveAPITestCase(TeamAPITestCase):
    def retrieve_team(self, user, team_id):
        with ForceLogin(user, self.client):
            response = self.client.get(f'/api/teams/{team_id}')
        return response

    def test_retrieve_team_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                team = team_membership['team']
                response = self.retrieve_team(self.admin_user, team.id)
                # no request in TeamReadSerializer context => team['user_role'] is None
                data = TeamReadSerializer(team).data
                self.check_response( response, status.HTTP_200_OK, data=data)


class TeamUpdateAPITestCase(TeamAPITestCase):
    def update_team(self, user, team_id, data):
        with ForceLogin(user, self.client):
            response = self.client.patch(f'/api/teams/{team_id}', data, format='json')
        return response

    def test_update_team_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                team = team_membership['team']
                updated_team = {
                    'name': 'Updated name',
                    'description': 'Updated description'
                }
                response = self.update_team(self.admin_user, team.id, updated_team)
                self.check_response(response, status.HTTP_200_OK, data=updated_team)


class TeamDeleteAPITestCase(TeamAPITestCase):
    def delete_team(self, user, team_id):
        with ForceLogin(user, self.client):
            response = self.client.delete(f'/api/teams/{team_id}', format='json')
        return response

    def test_delete_team_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                team = team_membership['team']
                response = self.delete_team(self.admin_user, team.id)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertFalse(Team.objects.filter(id=team.id).exists())
