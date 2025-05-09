# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from genflow.apps.common.security.rsa import generate_key_pair
from genflow.apps.team.models import Invitation, Membership, Team, TeamRole

USERS = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "password": "password",
    },
    "users": [
        {
            "username": "user1",
            "email": "user1@example.com",
            "password": "password1",
            "teams": [
                {
                    "name": "User1 Team",
                    "description": "User1 team description",
                },
            ],
        },
        {
            "username": "user2",
            "email": "user2@example.com",
            "password": "password2",
            "teams": [
                {
                    "name": "User2 Team",
                    "description": "User2 team description",
                },
            ],
        },
    ],
}


def create_dummy_users(create_teams: bool = False, team_role: TeamRole = TeamRole.OWNER):
    admin_user = User.objects.create_superuser(
        username=USERS["admin"]["username"],
        email=USERS["admin"]["email"],
        password=USERS["admin"]["password"],
    )

    regular_users = []
    for user in USERS["users"]:
        created_obj = {}
        created_obj["user"] = User.objects.create_user(
            username=user["username"], email=user["email"], password=user["password"]
        )
        if create_teams:
            created_obj["teams"] = []
            for team_data in user["teams"]:
                team, membership = create_dummy_team(created_obj["user"], team_data, team_role)
                created_obj["teams"].append({"team": team, "membership": membership})
        regular_users.append(created_obj)

    return admin_user, regular_users


def create_dummy_team(owner, team_data, team_role: TeamRole = TeamRole.OWNER):
    team = Team.objects.create(
        name=team_data["name"], description=team_data["description"], owner=owner
    )
    membership = Membership.objects.create(user=owner, team=team, role=team_role)
    if team_role != TeamRole.OWNER:
        create_dummy_invitation(membership, owner)
    else:
        membership.is_active = True
        membership.save()
    # generate public key
    team.encrypt_public_key = generate_key_pair(str(team.id))
    team.save()
    return team, membership


def create_dummy_invitation(membership, owner):
    invitation = Invitation.objects.create(
        key=get_random_string(64), membership=membership, owner=owner
    )
    return invitation


class ForceLogin:
    def __init__(self, user, client):
        self.user = user
        self.client = client

    def __enter__(self):
        if self.user:
            self.client.force_login(self.user, backend="django.contrib.auth.backends.ModelBackend")

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.user:
            self.client.logout()
