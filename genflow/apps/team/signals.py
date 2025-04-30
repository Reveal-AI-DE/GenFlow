# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from genflow.apps.restriction.signals import add_global_limits

# post_migrate is different from other signals
@receiver(post_migrate)
def add_team_global_limits(sender, **kwargs):
    """
    The `post_migrate` signal handler to add global limits corresponding to team app.
    """

    add_global_limits("team")


def create_default_team(sender, instance, created, **kwargs):
    from genflow.apps.team.serializers import TeamWriteSerializer

    # create team and owner membership
    if created and not instance.is_superuser:
        data = {
            "name": settings.USER_DEFAULT_TEAM_NAME,
            "description": "Personal team for user {}".format(instance.username),
        }
        serializer = TeamWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        extra_kwargs = {"owner": instance}
        serializer.save(**extra_kwargs)


def register_signals(app_config):
    # Create default 'Personal' team and add user as owner
    post_save.connect(create_default_team, sender=User)
