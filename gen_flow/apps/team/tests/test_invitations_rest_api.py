# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import Invitation, TeamRole
from gen_flow.apps.team.serializers import InvitationReadSerializer
from gen_flow.apps.team.tests.utils import ForceLogin, create_dummy_users


class InvitationAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user, self.regular_users = create_dummy_users(create_teams=True, team_role=TeamRole.MEMBER)

    def check_response(self, response, status_code, data=None):
        self.assertEqual(response.status_code, status_code)
        if data:
            self.assertEqual(response.data['id'], data['id'])
            self.assertEqual(response.data['role'], data['role'])
            self.assertEqual(response.data['user']['email'], data['user']['email'])
            self.assertEqual(response.data['team'], data['team'])


class InvitationListAPITestCase(InvitationAPITestCase):
    def setUp(self):
        super().setUp()
        self.created_invitations_count = sum([len(user['teams']) for user in self.regular_users])

    def list_invitations(self, user):
        with ForceLogin(user, self.client):
            response = self.client.get('/api/invitations')
        return response

    def test_list_invitations_admin(self):
        response = self.list_invitations(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.created_invitations_count)


class InvitationRetrieveAPITestCase(InvitationAPITestCase):
    def retrieve_invitation(self, user, invitation_id):
        with ForceLogin(user, self.client):
            response = self.client.get(f'/api/invitations/{invitation_id}')
        return response

    def test_retrieve_invitation_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                invitation = team_membership['membership'].invitation
                response = self.retrieve_invitation(self.admin_user, invitation.key)
                self.check_response(response, status.HTTP_200_OK, data=InvitationReadSerializer(invitation).data)


class InvitationUpdateAPITestCase(InvitationAPITestCase):
    def accept_invitation(self, user, invitation_id):
        with ForceLogin(user, self.client):
            response = self.client.patch(f'/api/invitations/{invitation_id}?accepted', None, format='json')
        return response

    def test_update_invitation_admin(self):
        for user in self.regular_users:
            for team_membership in user['teams']:
                invitation = team_membership['membership'].invitation
                self.assertFalse(invitation.accepted)
                response = self.accept_invitation(self.admin_user, invitation.key)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                updated_invitation = Invitation.objects.get(key=invitation.key)
                self.assertTrue(updated_invitation.accepted)
