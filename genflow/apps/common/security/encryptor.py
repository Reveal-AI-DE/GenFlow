# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

import base64

from genflow.apps.common.security import rsa


def obfuscated_token(token: str):
    if not token:
        return token
    if len(token) <= 8:
        return "*" * 20
    return token[:6] + "*" * 12 + token[-2:]


def encrypt_token(team_id: str, token: str):
    from genflow.apps.team.models import Team

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise ValueError(f"Team with id {team_id} not found")

    encrypted_token = rsa.encrypt(token, team.encrypt_public_key)
    return base64.b64encode(encrypted_token).decode()


def decrypt_token(team_id: str, token: str):
    return rsa.decrypt(base64.b64decode(token), team_id)


def decrypt_token_with_decoding(token: str, rsa_key):
    return rsa.decrypt_token_with_decoding(base64.b64decode(token), rsa_key)
