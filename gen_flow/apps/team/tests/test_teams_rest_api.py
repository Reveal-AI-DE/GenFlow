# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from gen_flow.apps.team.models import Team, TeamRole
from gen_flow.apps.team.serializers import TeamReadSerializer
from gen_flow.apps.team.tests.utils import USERS, ForceLogin, create_dummy_users


class TeamAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users(create_teams=True)

    def check_response(self, response, status_code, data=None):
        self.assertEqual(response.status_code, status_code)
        if data:
            self.assertEqual(response.data["name"], data["name"])
            self.assertEqual(response.data["description"], data["description"])


class TeamListAPITestCase(TeamAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.created_teams_count = sum([len(user["teams"]) for user in cls.regular_users])
        # each user also has a default team
        cls.created_teams_count += len(cls.regular_users)

    def list_teams(self, user):
        with ForceLogin(user, self.client):
            response = self.client.get("/api/teams")
        return response

    def test_list_teams_admin(self):
        response = self.list_teams(self.admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], self.created_teams_count)

    def test_list_teams_user(self):
        for user in self.regular_users:
            response = self.list_teams(user["user"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # each user also has a default team
            self.assertEqual(response.data["count"], len(user["teams"]) + 1)


class TeamCreateAPITestCase(TeamAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.admin_user, cls.regular_users = create_dummy_users()

    def create_team(self, user, data):
        with ForceLogin(user, self.client):
            response = self.client.post("/api/teams", data, format="json")
        return response

    def test_create_team_admin(self):
        for user in USERS["users"]:
            for team in user["teams"]:
                response = self.create_team(self.admin_user, team)
                self.check_response(response, status.HTTP_201_CREATED, data=team)

    def test_create_team_user(self):
        for user in USERS["users"]:
            for team in user["teams"]:
                response = self.create_team(self.regular_users[0]["user"], team)
                self.check_response(response, status.HTTP_201_CREATED, data=team)


class TeamRetrieveAPITestCase(TeamAPITestCase):
    def retrieve_team(self, user, team_id):
        with ForceLogin(user, self.client):
            response = self.client.get(f"/api/teams/{team_id}")
        return response

    def test_retrieve_team_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                team = team_membership["team"]
                response = self.retrieve_team(self.admin_user, team.id)
                # no request in TeamReadSerializer context => team['user_role'] is None
                data = TeamReadSerializer(team).data
                self.check_response(response, status.HTTP_200_OK, data=data)

    def test_retrieve_team_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                response = self.retrieve_team(user["user"], team_membership["team"].id)
                data = TeamReadSerializer(team_membership["team"]).data
                if team_membership["membership"].is_active:
                    self.check_response(response, status.HTTP_200_OK, data=data)
                else:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_team_user_not_member(self):
        for user in self.regular_users:
            for other_user in self.regular_users:
                if user["user"].id != other_user["user"].id:
                    for team_membership in other_user["teams"]:
                        response = self.retrieve_team(user["user"], team_membership["team"].id)
                        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeamUpdateAPITestCase(TeamAPITestCase):
    def update_team(self, user, team_id, data):
        with ForceLogin(user, self.client):
            response = self.client.patch(f"/api/teams/{team_id}", data, format="json")
        return response

    def test_update_team_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                updated_team = {"name": "Updated name", "description": "Updated description"}
                response = self.update_team(
                    self.admin_user, team_membership["team"].id, updated_team
                )
                self.check_response(response, status.HTTP_200_OK, data=updated_team)

    def test_update_team_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                updated_team = {"name": "Updated name", "description": "Updated description"}
                response = self.update_team(user["user"], team_membership["team"].id, updated_team)
                if team_membership["membership"].is_active and team_membership[
                    "membership"
                ].role in [TeamRole.OWNER.value, TeamRole.ADMIN.value]:
                    self.check_response(response, status.HTTP_200_OK, data=updated_team)
                else:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_team_user_not_member(self):
        for user in self.regular_users:
            for other_user in self.regular_users:
                if user["user"].id != other_user["user"].id:
                    for team_membership in other_user["teams"]:
                        updated_team = {
                            "name": "Updated name",
                            "description": "Updated description",
                        }
                        response = self.update_team(
                            user["user"], team_membership["team"].id, updated_team
                        )
                        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_team_use_not_owner_or_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                if team_membership["membership"].is_active:
                    team_membership["membership"].role = TeamRole.MEMBER.value
                    team_membership["membership"].save()
                    updated_team = {"name": "Updated name", "description": "Updated description"}
                    response = self.update_team(
                        user["user"], team_membership["team"].id, updated_team
                    )
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeamDeleteAPITestCase(TeamAPITestCase):
    def delete_team(self, user, team_id):
        with ForceLogin(user, self.client):
            response = self.client.delete(f"/api/teams/{team_id}", format="json")
        return response

    def test_delete_team_admin(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                team = team_membership["team"]
                response = self.delete_team(self.admin_user, team.id)
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.assertFalse(Team.objects.filter(id=team.id).exists())

    def test_delete_team_user(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                response = self.delete_team(user["user"], team_membership["team"].id)
                if team_membership["membership"].is_active and team_membership[
                    "membership"
                ].role in [TeamRole.OWNER.value]:
                    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                    self.assertFalse(Team.objects.filter(id=team_membership["team"].id).exists())
                else:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team_user_not_member(self):
        for user in self.regular_users:
            for other_user in self.regular_users:
                if user["user"].id != other_user["user"].id:
                    for team_membership in other_user["teams"]:
                        response = self.delete_team(user["user"], team_membership["team"].id)
                        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team_use_not_owner(self):
        for user in self.regular_users:
            for team_membership in user["teams"]:
                if team_membership["membership"].is_active:
                    team_membership["membership"].role = TeamRole.MEMBER.value
                    team_membership["membership"].save()
                    response = self.delete_team(user["user"], team_membership["team"].id)
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                    self.assertTrue(Team.objects.filter(id=team_membership["team"].id).exists())
