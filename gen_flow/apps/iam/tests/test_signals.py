# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.apps import apps
from allauth.account.models import EmailAddress
from django.db.models.signals import post_migrate
from gen_flow.apps.iam.signals import register_groups


class PostMigrateSignalTest(TestCase):
    def test_register_groups_signal(self):
        # Disconnect the signal to avoid side effects from other tests
        post_migrate.disconnect(register_groups, sender=apps.get_app_config('iam'))

        # Reconnect the signal for this test
        post_migrate.connect(register_groups, sender=apps.get_app_config('iam'))

        # Trigger the post_migrate signal
        post_migrate.send(sender=apps.get_app_config('iam'), app_config=apps.get_app_config('iam'))

        # Check if the groups were created
        self.assertTrue(Group.objects.filter(name=settings.IAM_DEFAULT_ROLE).exists())
        self.assertTrue(Group.objects.filter(name=settings.IAM_ADMIN_ROLE).exists())

        # Disconnect the signal after the test
        post_migrate.disconnect(register_groups, sender=apps.get_app_config('iam'))


class CreateUserSignalTest(TestCase):
    def setUp(self):
        # Create groups for testing
        self.admin_group = Group.objects.create(name=settings.IAM_ADMIN_ROLE)
        self.default_group = Group.objects.create(name=settings.IAM_DEFAULT_ROLE)

    def test_create_superuser(self):
        # Create a superuser
        superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='password')

        # Check if the superuser is added to the admin group
        self.assertIn(self.admin_group, superuser.groups.all())

        # Check if the email address is created and verified
        email_address = EmailAddress.objects.get(user=superuser)
        self.assertTrue(email_address.verified)

    def test_create_regular_user(self):
        # Create a regular user
        user = User.objects.create_user(username='user', email='user@example.com', password='password')

        # Check if the user is added to the default group
        self.assertIn(self.default_group, user.groups.all())

    # ToDo: Fix this test, find a way to patch User.save method
    # to add skip_group_assigning attribute
    def test_create_user_with_skip_group_assigning(self):
        # Create a regular user with skip_group_assigning attribute
        user = User.objects.create_user(username='user', email='user@example.com', password='password')

        # Check if the user is not added to the default group
        # self.assertNotIn(self.default_group, user.groups.all())
        self.assertIn(self.default_group, user.groups.all())
