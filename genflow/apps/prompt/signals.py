# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from django.db.models.signals import post_delete, post_migrate
from django.dispatch import receiver

from genflow.apps.prompt.models import Prompt
from genflow.apps.restriction.signals import add_global_limits


# post_migrate is different from other signals
@receiver(post_migrate)
def add_prompt_global_limits(sender, **kwargs):
    """
    The `post_migrate` signal handler to add global limits corresponding to prompt app.
    """

    add_global_limits("prompt")


@receiver(post_delete, sender=Prompt)
def delete_key_on_prompt_delete(sender, instance, **kwargs):
    instance.remove_media_dir()
