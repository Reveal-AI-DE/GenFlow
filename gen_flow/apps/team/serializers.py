# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework import serializers
from django.contrib.auth.models import User, Group

from gen_flow.apps.common.security.rsa import generate_key_pair
from gen_flow.apps.team import models as models


class BasicUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the User model tha returns a serialized representation
    of the User model with the basic fields, and validates the presence of
    unknown fields in the input data.
    '''

    class Meta:
        model = User
        # TODO: Adding 'url' cases exception => Could not resolve URL for hyperlinked relationship using view name 'user-detail'.
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        # default ordering by 'id' in descending order.
        ordering = ['-id']

    def validate(self, data):
        '''
        Checks for unknown fields in the input data and raises a ValidationError if any are found.
        '''

        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if unknown_keys:
                if set(['is_staff', 'is_superuser', 'groups']) & unknown_keys:
                    message = 'You do not have permissions to access some of' + \
                        ' these fields: {}'.format(unknown_keys)
                else:
                    message = 'Got unknown fields: {}'.format(unknown_keys)
                raise serializers.ValidationError(message)
        return data


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the User model tha returns a serialized representation
    of the User model with the all fields and their associated groups.

    Attributes:
        groups (SlugRelatedField): A field that represents the user's groups using the
            group's name as the slug field. It allows multiple groups to be associated
            with a user.
    '''
    groups = serializers.SlugRelatedField(many=True,
        slug_field='name', queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'groups', 'is_staff', 'is_superuser', 'is_active', 'last_login',
                  'date_joined')
        read_only_fields = ('last_login', 'date_joined')
        write_only_fields = ('password', )
        # default ordering by 'id' in descending order.
        ordering = ['-id']


class TeamReadSerializer(serializers.ModelSerializer):
    '''
    Serializer for Team model, where all fields are read-only.
    To be used for GET requests.
    '''

    owner = BasicUserSerializer(allow_null=True)
    user_role = serializers.SerializerMethodField()

    def get_user_role(self, obj):
        '''
        Retrieve the role of the user in the given team.

        Args:
            obj: The team object for which the user's role is being retrieved.

        Returns:
            str: The role of the user in the team if the user is a member, otherwise None.
        '''
        if 'request' not in self.context:
            return None
        membership = models.Membership.objects.filter(
            team=obj, user=self.context['request'].user).first()
        return membership.role if membership else None

    class Meta:
        model = models.Team
        fields = ['id', 'name', 'description', 'created_date',
            'updated_date', 'owner', 'user_role', 'is_personal']
        read_only_fields = fields

class TeamWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for Team model, to be used for POST requests.
    It uses the TeamReadSerializer for the representation of the instance data.
    '''

    class Meta:
        model = models.Team
        fields = ['id', 'name', 'description', 'created_date', 'updated_date', 'owner']

        # TODO: at the moment isn't possible to change the owner.
        read_only_fields = ['created_date', 'updated_date', 'owner']

    def create(self, validated_data):
        ''''
        Creates a new Team instance with the provided validated data.
            Generates a public key for the team and creates a Membership for the owner.'
        '''

        team = super().create(validated_data)
        # generate public key
        team.encrypt_public_key = generate_key_pair(team.id)
        team.save()
        models.Membership.objects.create(
            user=team.owner,
            team=team,
            is_active=True,
            joined_date=team.created_date,
            role=models.TeamRole.OWNER)

        return team

    def to_representation(self, instance):
        '''
        Converts the instance to its representation using TeamReadSerializer.
        '''

        serializer = TeamReadSerializer(instance, context=self.context)
        return serializer.data


class MembershipReadSerializer(serializers.ModelSerializer):
    '''
    Serializer for Membership model, where all fields are read-only.
    To be used for GET requests.
    '''
    user = BasicUserSerializer()

    class Meta:
        model = models.Membership
        fields = ['id', 'user', 'team', 'is_active', 'joined_date', 'role',
                  'invitation', 'created_date', 'updated_date']
        read_only_fields = fields
        extra_kwargs = {
            'invitation': {
                'allow_null': True, # owner of a team does not have an invitation
            }
        }

class MembershipWriteSerializer(serializers.ModelSerializer):
    '''
    Serializer for Membership model, to be used for POST requests.
    It uses the MembershipReadSerializer for the representation of the instance data.
    '''

    class Meta:
        model = models.Membership
        fields = ['id', 'user', 'team',
                  'is_active', 'joined_date', 'role']
        read_only_fields = ['user', 'team', 'joined_date'] # 'is_active'

    def to_representation(self, instance):
        serializer = MembershipReadSerializer(instance, context=self.context)
        return serializer.data