# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import TeamRole, Membership
from gen_flow.apps.team.serializers import MembershipReadSerializer
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users, USERS


class MembershipAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True)

    def check_response(self, response, status_code, data=None):
        self.assertEqual(response.status_code, status_code)
        if data:
            self.assertEqual(response.data['user']['id'], data['user']['id'])
            self.assertEqual(response.data['team'], data['team'])
            self.assertEqual(response.data['role'], data['role'])
            self.assertEqual(response.data['is_active'], data['is_active'])
            if data['role'] == TeamRole.OWNER.value:
                self.assertIsNone(response.data['invitation'])


class MembershipListAPITestCase(MembershipAPITestCase):
    def setUp(self):
        super().setUp()
        self.created_memberships_count = sum([len(user['teams']) for user in self.regular_users])
        # each user also has a default team
        self.created_memberships_count += len(self.regular_users)

    def list_memberships(self, user):
        with ForceLogin(user, self.client):
            response = self.client.get('/api/memberships')
        return response

    def test_list_memberships_admin(self):
        response = self.list_memberships(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.created_memberships_count)


class MembershipRetrieveAPITestCase(MembershipAPITestCase):
    def retrieve_membership(self, user, membership_id):
        with ForceLogin(user, self.client):
            response = self.client.get(f'/api/memberships/{membership_id}')
        return response

    def test_retrieve_membership_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                membership = team_membership['membership']
                response = self.retrieve_membership(self.admin_user, membership.id)
                self.check_response(response, status.HTTP_200_OK, data=MembershipReadSerializer(membership).data)


class MembershipUpdateAPITestCase(MembershipAPITestCase):
    def update_membership(self, user, membership_id, data):
        with ForceLogin(user, self.client):
            response = self.client.patch(f'/api/memberships/{membership_id}', data, format='json')
        return response

    def test_update_membership_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                membership = team_membership['membership']
                updated_membership = MembershipReadSerializer(membership).data
                updated_membership['role'] = TeamRole.OWNER.value
                updated_membership['is_active'] = not membership.is_active
                response = self.update_membership(self.admin_user, membership.id, updated_membership)
                self.check_response(response, status.HTTP_200_OK, data=updated_membership)


class MembershipDeleteAPITestCase(MembershipAPITestCase):
    def delete_membership(self, user, membership_id):
        with ForceLogin(user, self.client):
            response = self.client.delete(f'/api/memberships/{membership_id}', format='json')
        return response

    def test_delete_membership_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                membership = team_membership['membership']
                response = self.delete_membership(self.admin_user, membership.id)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertFalse(Membership.objects.filter(id=membership.id).exists())

