# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from distutils.util import strtobool

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from genflow.apps.common.security.rsa import generate_key_pair
from genflow.apps.iam.serializers import BasicUserSerializer
from genflow.apps.team import models as models


class TeamReadSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model, where all fields are read-only.
    To be used for GET requests.
    """

    owner = BasicUserSerializer(allow_null=True)
    user_role = serializers.SerializerMethodField()

    def get_user_role(self, obj) -> str | None:
        """
        Retrieve the role of the user in the given team.

        Args:
            obj: The team object for which the user's role is being retrieved.

        Returns:
            str: The role of the user in the team if the user is a member, otherwise None.
        """
        if "request" not in self.context:
            return None
        membership = models.Membership.objects.filter(
            team=obj, user=self.context["request"].user
        ).first()
        return membership.role if membership else None

    class Meta:
        model = models.Team
        fields = [
            "id",
            "name",
            "description",
            "created_date",
            "updated_date",
            "owner",
            "user_role",
            "is_personal",
        ]
        read_only_fields = fields


class TeamWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model, to be used for POST requests.
    It uses the TeamReadSerializer for the representation of the instance data.
    """

    class Meta:
        model = models.Team
        fields = ["id", "name", "description", "created_date", "updated_date", "owner"]

        # TODO: at the moment isn't possible to change the owner.
        read_only_fields = ["created_date", "updated_date", "owner"]

    def create(self, validated_data):
        """'
        Creates a new Team instance with the provided validated data.
            Generates a public key for the team and creates a Membership for the owner.'
        """

        team = super().create(validated_data)
        # generate public key
        team.encrypt_public_key = generate_key_pair(str(team.id))
        team.save()
        models.Membership.objects.create(
            user=team.owner,
            team=team,
            is_active=True,
            joined_date=team.created_date,
            role=models.TeamRole.OWNER,
        )

        return team

    def to_representation(self, instance):
        """
        Converts the instance to its representation using TeamReadSerializer.
        """

        serializer = TeamReadSerializer(instance, context=self.context)
        return serializer.data


class InvitationReadSerializer(serializers.ModelSerializer):
    """
    Serializer for Invitation model, where all fields are read-only.
    To be used for GET requests.
    """

    id = serializers.CharField(source="key")
    role = serializers.ChoiceField(models.Membership.role.field.choices, source="membership.role")
    user = BasicUserSerializer(source="membership.user")
    team = serializers.PrimaryKeyRelatedField(
        queryset=models.Team.objects.all(), source="membership.team"
    )
    owner = BasicUserSerializer(allow_null=True)

    class Meta:
        model = models.Invitation
        fields = ["id", "created_date", "owner", "role", "user", "team"]
        read_only_fields = fields


class InvitationWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Invitation model, to be used for POST requests.
    It uses the TeamReadSerializer for the representation of the instance data.
    """

    role = serializers.ChoiceField(models.Membership.role.field.choices, source="membership.role")
    email = serializers.EmailField(source="membership.user.email")

    class Meta:
        model = models.Invitation
        fields = ["key", "created_date", "owner", "role", "email"]
        read_only_fields = ["key", "created_date", "owner"]

    def create(self, validated_data):
        """
        Creates a new invitation and membership for a user.

        This method handles the creation of a new user if the user does not already exist,
        and associates the user with a team through a membership. If the user is already
        a member of the team, a validation error is raised.

        Raises:
            serializers.ValidationError: If the user is already a member of the team.
        """

        membership_data = validated_data.pop("membership")
        team = validated_data.pop("team")
        try:
            user = get_user_model().objects.get(email__iexact=membership_data["user"]["email"])
            del membership_data["user"]
        except ObjectDoesNotExist:
            user_email = membership_data["user"]["email"]
            user = get_user_model().objects.create_user(username=user_email, email=user_email)
            user.set_unusable_password()
            # User.objects.create_user(...) normalizes passed email and user.email can be different from original user_email
            email = EmailAddress.objects.create(
                user=user, email=user.email, primary=True, verified=False
            )
            user.save()
            email.save()
            del membership_data["user"]

        membership, created = models.Membership.objects.get_or_create(
            defaults=membership_data, user=user, team=team
        )
        if not created:
            raise serializers.ValidationError(
                {"message": "The user is a member of " "the team already."}
            )
        invitation = models.Invitation.objects.create(**validated_data, membership=membership)

        return invitation

    def update(self, instance, validated_data):
        """
        Updates the given instance with the validated data.
        """

        return super().update(instance, {})

    def save(self, **kwargs):
        """
        Save the invitation instance and handle its acceptance or sending based on settings.
        """

        invitation = super().save(**kwargs)
        request = self.context.get("request")
        if not strtobool(settings.TEAM_INVITATION_CONFIRM):
            invitation.accept(invitation.created_date)
        else:
            invitation.send(request)

        return invitation

    def to_representation(self, instance):
        """
        Returns the serialized data for the given instance using InvitationReadSerializer.
        """

        serializer = InvitationReadSerializer(instance, context=self.context)
        return serializer.data


class MembershipReadSerializer(serializers.ModelSerializer):
    """
    Serializer for Membership model, where all fields are read-only.
    To be used for GET requests.
    """

    user = BasicUserSerializer()

    class Meta:
        model = models.Membership
        fields = [
            "id",
            "user",
            "team",
            "is_active",
            "joined_date",
            "role",
            "invitation",
            "created_date",
            "updated_date",
        ]
        read_only_fields = fields
        extra_kwargs = {
            "invitation": {
                "allow_null": True,  # owner of a team does not have an invitation
            }
        }


class MembershipWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Membership model, to be used for POST requests.
    It uses the MembershipReadSerializer for the representation of the instance data.
    """

    class Meta:
        model = models.Membership
        fields = ["id", "user", "team", "is_active", "joined_date", "role"]
        read_only_fields = ["user", "team", "joined_date"]  # 'is_active'

    def to_representation(self, instance):
        serializer = MembershipReadSerializer(instance, context=self.context)
        return serializer.data
