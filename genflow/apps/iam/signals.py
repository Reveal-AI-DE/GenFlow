# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver


# post_migrate is different from other signals
@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """
    The `post_migrate` signal handler to create groups corresponding to system roles.

    Args:
        sender (Any): The sender of the signal.
        **kwargs: Additional keyword arguments passed by the signal.
    """

    # Create all groups which corresponds system roles
    for role in settings.IAM_ROLES:
        Group.objects.get_or_create(name=role)


if settings.IAM_TYPE == "BASIC":

    def add_group(sender, instance, created, **kwargs):
        """
        Signal receiver that handles the creation of a user.

        - If the user is a superuser and staff, it adds the user to the IAM_ADMIN_ROLE group and creates
          and verifies an email address for the superuser account if email verification is required.
        - If the user is not a superuser and the user instance is newly created, it adds the user to the
          IAM_DEFAULT_ROLE group unless the 'skip_group_assigning' attribute is set on the instance.

        Args:
            sender (Model): The model class that sent the signal.
            instance (User): The instance of the user being created.
            created (bool): A boolean indicating whether the user instance was created.
            **kwargs: Additional keyword arguments.
        """
        from allauth.account import app_settings as allauth_settings
        from allauth.account.models import EmailAddress

        if instance.is_superuser and instance.is_staff:
            db_group = Group.objects.get(name=settings.IAM_ADMIN_ROLE)
            instance.groups.add(db_group)

            # create and verify EmailAddress for superuser accounts
            if allauth_settings.EMAIL_REQUIRED:
                EmailAddress.objects.get_or_create(
                    user=instance, email=instance.email, primary=True, verified=True
                )
        else:  # don't need to add default groups for superuser
            if created and not getattr(instance, "skip_group_assigning", None):
                db_group = Group.objects.get(name=settings.IAM_DEFAULT_ROLE)
                instance.groups.add(db_group)


def register_signals():
    """
    Registers Django signals for the IAM app.
    """

    if settings.IAM_TYPE == "BASIC":
        # Add default groups and add admin rights to super users.
        post_save.connect(add_group, sender=User)
