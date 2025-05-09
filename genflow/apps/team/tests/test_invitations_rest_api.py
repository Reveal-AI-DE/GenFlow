# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from genflow.apps.restriction.tests.utils import override_limit
from genflow.apps.team.models import Invitation, TeamRole
from genflow.apps.team.serializers import InvitationReadSerializer
from genflow.apps.team.tests.utils import ForceLogin, create_dummy_users


class InvitationAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(
            create_teams=True, team_role=TeamRole.MEMBER
        )

    def check_response(self, response, status_code, data=None):
        self.assertEqual(response.status_code, status_code)
        if data:
            self.assertEqual(response.data["id"], data["id"])
            self.assertEqual(response.data["role"], data["role"])
            self.assertEqual(response.data["user"]["email"], data["user"]["email"])
            self.assertEqual(response.data["team"], data["team"])


class InvitationListAPITestCase(InvitationAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.created_invitations_count = sum([len(user["teams"]) for user in cls.regular_users])

    def list_invitations(self, user, team_id: int = None):
        with ForceLogin(user, self.client):
            url = "/api/invitations" if not team_id else f"/api/invitations?team={team_id}"
            response = self.client.get(url)
        return response

    def test_list_invitations_admin(self):
        response = self.list_invitations(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], self.created_invitations_count)

    def test_list_invitations_by_team_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                team_id = team_membership["team"].id
                response = self.list_invitations(self.admin_user, team_id)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                # we have one membership per team, for team member
                self.assertEqual(response.data["count"], 1)

    def test_list_invitations_user(self):
        for user in self.regular_users:
            response = self.list_invitations(user["user"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # each user also has a default team
            self.assertEqual(response.data["count"], len(user["teams"]))

    def test_list_invitations_by_team_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                response = self.list_invitations(user["user"], team_id=team_membership["team"].id)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                # we have one membership per team, for team member
                self.assertEqual(response.data["count"], 1)


class InvitationRetrieveAPITestCase(InvitationAPITestCase):
    def retrieve_invitation(self, user, invitation_id):
        with ForceLogin(user, self.client):
            response = self.client.get(f"/api/invitations/{invitation_id}")
        return response

    def test_retrieve_invitation_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                invitation = team_membership["membership"].invitation
                response = self.retrieve_invitation(self.admin_user, invitation.key)
                self.check_response(
                    response, status.HTTP_200_OK, data=InvitationReadSerializer(invitation).data
                )

    def test_retrieve_invitation_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                invitation = team_membership["membership"].invitation
                response = self.retrieve_invitation(user["user"], invitation.key)
                self.check_response(
                    response, status.HTTP_200_OK, data=InvitationReadSerializer(invitation).data
                )

    def test_retrieve_invitation_user_not_member(self):
        for user in self.regular_users:
            for other_user in self.regular_users:
                if user["user"].id != other_user["user"].id:
                    for team_membership in other_user["teams"]:
                        invitation = team_membership["membership"].invitation
                        response = self.retrieve_invitation(user["user"], invitation.key)
                        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InvitationCreateAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    def create_invitation(self, user, data, team_id):
        with ForceLogin(user, self.client):
            response = self.client.post(f"/api/invitations?team={team_id}", data, format="json")
        return response

    def test_create_invitation_with_existent_membership(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                data = {
                    "email": user["user"].email,
                    "role": TeamRole.MEMBER,
                }
                response = self.create_invitation(self.admin_user, data, team_membership["team"].id)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invitation_new_user_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                email = f'new_user_{team_membership["team"].id}@example.com'
                data = {
                    "email": email,
                    "role": TeamRole.MEMBER,
                }
                response = self.create_invitation(self.admin_user, data, team_membership["team"].id)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data["user"]["email"], email)

    def test_create_invitation_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                email = f'new_user_{team_membership["team"].id}@example.com'
                data = {
                    "email": email,
                    "role": TeamRole.MEMBER,
                }
                response = self.create_invitation(user["user"], data, team_membership["team"].id)
                if team_membership["membership"].is_active and team_membership[
                    "membership"
                ].role in [TeamRole.OWNER.value, TeamRole.ADMIN.value]:
                    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                    self.assertEqual(response.data["user"]["email"], email)
                else:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invitation_user_not_member(self):
        for user in self.regular_users:
            for other_user in self.regular_users:
                if user["user"].id != other_user["user"].id:
                    for team_membership in other_user["teams"]:
                        email = f'new_user_{team_membership["team"].id}@example.com'
                        data = {
                            "email": email,
                            "role": TeamRole.MEMBER,
                        }
                        response = self.create_invitation(
                            user["user"], data, team_membership["team"].id
                        )
                        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invitation_user_check_global_limit(self):
        override_limit(
            key="MAX_INVITATION_PER_TEAM",
            value=0,
        )
        user = self.regular_users[0]["user"]
        team_membership = self.regular_users[0]["teams"][0]
        email = f'new_user_{team_membership["team"].id}@example.com'
        data = {
            "email": email,
            "role": TeamRole.MEMBER,
        }
        response = self.create_invitation(user, data, team_membership["team"].id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invitation_user_check_under_global_limit(self):
        override_limit(
            key="MAX_INVITATION_PER_TEAM",
            value=2,
        )
        user = self.regular_users[0]["user"]
        team_membership = self.regular_users[0]["teams"][0]
        email = f'new_user_{team_membership["team"].id}@example.com'
        data = {
            "email": email,
            "role": TeamRole.MEMBER,
        }
        response = self.create_invitation(user, data, team_membership["team"].id)
        if team_membership["membership"].is_active and team_membership["membership"].role in [
            TeamRole.OWNER.value,
            TeamRole.ADMIN.value,
        ]:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["user"]["email"], email)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InvitationUpdateAPITestCase(InvitationAPITestCase):
    def accept_invitation(self, user, invitation_id):
        with ForceLogin(user, self.client):
            response = self.client.patch(
                f"/api/invitations/{invitation_id}?accepted", None, format="json"
            )
        return response

    def test_update_invitation_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                invitation = team_membership["membership"].invitation
                self.assertFalse(invitation.accepted)
                response = self.accept_invitation(self.admin_user, invitation.key)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                updated_invitation = Invitation.objects.get(key=invitation.key)
                self.assertTrue(updated_invitation.accepted)

    def test_update_invitation_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                invitation = team_membership["membership"].invitation
                self.assertFalse(invitation.accepted)
                response = self.accept_invitation(user["user"], invitation.key)
                if team_membership["membership"].is_active:
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    updated_invitation = Invitation.objects.get(key=invitation.key)
                    self.assertTrue(updated_invitation.accepted)
                else:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_invitation_user_not_member(self):
        for user in self.regular_users:
            for other_user in self.regular_users:
                if user["user"].id != other_user["user"].id:
                    for team_membership in other_user["teams"]:
                        invitation = team_membership["membership"].invitation
                        response = self.accept_invitation(user["user"], invitation.key)
                        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
