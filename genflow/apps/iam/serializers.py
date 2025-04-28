# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from typing import Optional, Union

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


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
