# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users


class TeamListAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)
        self.created_teams_count = sum([len(user['teams']) for user in self.regular_users])

    def test_list_teams(self):
        with ForceLogin(self.admin_user, self.client):
            response = self.client.get('/api/teams')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.created_teams_count)


# class TeamCreateAPITestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.users = create_dummy_users()

#     def test_create_team(self):
#         url = reverse('team-list')
#         data = {'name': 'New Team', 'description': 'A new team'}
#         with ForceLogin(self.users[0], self.client):
#             response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['name'], 'New Team')
#         self.assertEqual(response.data['description'], 'A new team')

# class TeamRetrieveAPITestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.users = create_dummy_users()
#         self.teams = create_dummy_teams(self.users)

#     def test_retrieve_team(self):
#         url = reverse('team-detail', args=[self.teams[0].id])
#         with ForceLogin(self.users[0], self.client):
#             response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Team 1')

# class TeamUpdateAPITestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.users = create_dummy_users()
#         self.teams = create_dummy_teams(self.users)

#     def test_update_team(self):
#         url = reverse('team-detail', args=[self.teams[0].id])
#         data = {'name': 'Updated Team', 'description': 'Updated description'}
#         with ForceLogin(self.users[0], self.client):
#             response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Updated Team')
#         self.assertEqual(response.data['description'], 'Updated description')

# class TeamDeleteAPITestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.users = create_dummy_users()
#         self.teams = create_dummy_teams(self.users)

#     def test_delete_team(self):
#         url = reverse('team-detail', args=[self.teams[0].id])
#         with ForceLogin(self.users[0], self.client):
#             response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Team.objects.filter(id=self.teams[0].id).exists())
