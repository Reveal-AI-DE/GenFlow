# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_default_team(sender, instance, created, **kwargs):
    from gen_flow.apps.team.serializers import TeamWriteSerializer
    # create team and owner membership
    if created and not instance.is_superuser:
        data = {
            'name': settings.USER_DEFAULT_TEAM_NAME,
            'description': 'Personal team for user {}'.format(instance.username),
        }
        serializer = TeamWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        extra_kwargs = {'owner': instance}
        serializer.save(**extra_kwargs)

def register_signals(app_config):
    # Create default 'Personal' team and add user as owner
    post_save.connect(create_default_team, sender=User)
