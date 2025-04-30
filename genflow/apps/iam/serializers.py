# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from os import path as osp
from typing import Optional, Union

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from genflow.apps.common.file_utils import is_image
from genflow.apps.iam.forms import ResetPasswordFormEx


class BasicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model tha returns a serialized representation
    of the User model with the basic fields, and validates the presence of
    unknown fields in the input data.
    """

    class Meta:
        model = get_user_model()
        # TODO: Adding 'url' cases exception => Could not resolve URL for hyperlinked relationship using view name 'user-detail'.
        fields = ("id", "username", "email", "first_name", "last_name")
        # default ordering by 'id' in descending order.
        ordering = ["-id"]

    def validate(self, data):
        """
        Checks for unknown fields in the input data and raises a ValidationError if any are found.
        """

        if hasattr(self, "initial_data"):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                if set(["is_staff", "is_superuser", "groups"]) & unknown_keys:
                    message = (
                        "You do not have permissions to access some of"
                        + " these fields: {}".format(unknown_keys)
                    )
                else:
                    message = "Got unknown fields: {}".format(unknown_keys)
                raise serializers.ValidationError(message)
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model tha returns a serialized representation
    of the User model with the all fields and their associated groups.

    Attributes:
        groups (SlugRelatedField): A field that represents the user's groups using the
            group's name as the slug field. It allows multiple groups to be associated
            with a user.
    """

    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj: Union[dict, User]) -> Optional[str]:
        """
        Dynamically generates the avatar URL based on the user's id.
        If the avatar file does not exist, return a default avatar URL.
        """

        avatar_path = osp.join(settings.USERS_MEDIA_URL, str(obj.id), "avatar.png")
        full_path = osp.join(settings.USERS_MEDIA_ROOT, str(obj.id), "avatar.png")

        if osp.exists(full_path) and is_image(full_path):
            return avatar_path
        return None

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "avatar",
            "is_staff",
            "is_superuser",
            "is_active",
            "last_login",
            "date_joined",
        )
        read_only_fields = ("last_login", "date_joined")
        write_only_fields = ("password",)
        # default ordering by 'id' in descending order.
        ordering = ["-id"]


class RegisterSerializerEx(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email_verification_required = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField)
    def get_email_verification_required(self, obj: Union[dict, User]) -> bool:
        return (
            allauth_settings.EMAIL_VERIFICATION
            == allauth_settings.EmailVerificationMethod.MANDATORY
        )

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_key(self, obj: Union[dict, User]) -> Optional[str]:
        key = None
        if (
            isinstance(obj, User)
            and allauth_settings.EMAIL_VERIFICATION
            != allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            key = obj.auth_token.key
        return key

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),
                "last_name": self.validated_data.get("last_name", ""),
            }
        )

        return data

    def validate_email(self, email):
        def email_address_exists(email) -> bool:
            if EmailAddress.objects.filter(email__iexact=email).exists():
                return True

            if email_field := allauth_settings.USER_MODEL_EMAIL_FIELD:
                users = get_user_model().objects
                return users.filter(**{email_field + "__iexact": email}).exists()
            return False

        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                user = self.get_dummy_user(email)
                if not user:
                    raise serializers.ValidationError(
                        ("A user is already registered with this e-mail address."),
                    )

        return email

    def save(self, request):
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()

        # Allow to overwrite data for dummy users
        dummy_user = self.get_dummy_user(self.cleaned_data["email"])
        user = dummy_user if dummy_user else adapter.new_user(request)

        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(detail=serializers.as_serializer_error(exc))
        user.save()
        self.custom_signup(request, user)

        if not dummy_user:
            setup_user_email(request, user, [])
        return user

    def get_dummy_user(self, email):
        from allauth.account.utils import filter_users_by_email

        users = filter_users_by_email(email)
        if not users or len(users) > 1:
            return None
        user = users[0]
        if user.has_usable_password():
            return None
        if (
            allauth_settings.EMAIL_VERIFICATION
            == allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            email = EmailAddress.objects.get_for_user(user, email)
            if email.verified:
                return None
        return user


class PasswordResetSerializerEx(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return ResetPasswordFormEx

    def get_email_options(self):
        domain = None
        if hasattr(settings, "UI_HOST") and settings.UI_HOST:
            domain = settings.UI_HOST
            if hasattr(settings, "UI_PORT") and settings.UI_PORT:
                domain += ":{}".format(settings.UI_PORT)
        return {"domain_override": domain}


class UserCheckSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
