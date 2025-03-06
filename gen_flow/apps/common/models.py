# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.db import models
from django.contrib.auth import get_user_model

class TimeAuditModel(models.Model):
    '''
    A Django abstract base class model that provides self-updating
    'created_date' and 'updated_date' fields to any model that inherits from it.

    Attributes:
        created_date (DateTimeField): The date and time when the object was created.
            Automatically set on object creation.
        updated_date (DateTimeField): The date and time when the object was last updated.
            Automatically updated on object save.
    '''

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def touch(self) -> None:
        '''
        Updates the 'updated_date' field to the current date and time.
        '''
        self.save(update_fields=['updated_date'])


class UserOwnedModel(models.Model):
    '''
    Abstract base model that includes a foreign key to the user model as the owner.

    Attributes:
        owner (ForeignKey): A foreign key to the user model, which can be null or blank.
            If the referenced user is deleted, the owner field is set to null.
            The related name for reverse lookup is dynamically set to the class name.
    '''

    owner = models.ForeignKey(get_user_model(), null=True,
        blank=True, on_delete=models.SET_NULL, related_name='%(class)s')

    class Meta:
        abstract = True


class TeamAssociatedModel(models.Model):
    '''
    Abstract base model that associates a model with a team.

    Attributes:
        team (ForeignKey): Foreign key to the 'team.Team' model. This field is required and
            uses a cascade delete strategy. The related name is dynamically
            set to the class name of the inheriting model.
    '''
    team = models.ForeignKey('team.Team', null=False,
        on_delete=models.CASCADE, related_name='%(class)s')

    class Meta:
        abstract = True