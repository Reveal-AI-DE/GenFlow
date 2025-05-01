# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.db.models.signals import post_migrate, post_delete
from django.dispatch import receiver

from genflow.apps.restriction.signals import add_global_limits
from genflow.apps.assistant.models import Assistant


# post_migrate is different from other signals
@receiver(post_migrate)
def add_assistant_global_limits(sender, **kwargs):
    """
    The `post_migrate` signal handler to add global limits corresponding to assistant app.
    """

    add_global_limits("assistant")

@receiver(post_delete, sender=Assistant)
def delete_key_on_assistant_delete(sender, instance, **kwargs):
    instance.remove_media_dir()