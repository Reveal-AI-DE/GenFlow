# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from os import path as osp
import shutil

from django.conf import settings

from django.db.models.signals import post_migrate, post_delete
from django.dispatch import receiver

from genflow.apps.restriction.signals import add_global_limits
from genflow.apps.session.models import Session


# post_migrate is different from other signals
@receiver(post_migrate)
def add_session_global_limits(sender, **kwargs):
    """
    The `post_migrate` signal handler to add global limits corresponding to session app.
    """

    add_global_limits("session")

@receiver(post_delete, sender=Session)
def delete_dir_on_session_delete(sender, instance, **kwargs):
    if osp.exists(instance.dirname):
        shutil.rmtree(instance.dirname)
