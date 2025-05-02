# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from os import path as osp

from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.app_settings import api_settings as dj_rest_auth_settings
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.utils import jwt_encode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect
from drf_spectacular.utils import (
    OpenApiResponse,
    PolymorphicProxySerializer,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response

from genflow.apps.common.file_utils import check_avatar
from genflow.apps.common.storage import fs
from genflow.apps.iam import serializers


@extend_schema(tags=["users"])
@extend_schema_view(
    self=extend_schema(
        summary="Get current user",
        description="Retrieve the details of the currently authenticated user.",
        responses={
            "200": PolymorphicProxySerializer(
                component_name="MetaUser",
                serializers=[
                    serializers.UserSerializer,
                    serializers.BasicUserSerializer,
                ],
                resource_type_field_name=None,
            ),
        },
    ),
    upload_avatar=extend_schema(
        summary="Upload a user avatar",
        description="Upload a new avatar image for the user",
        responses={
            "200": OpenApiResponse(description="Avatar uploaded successfully"),
        },
    ),
    check=extend_schema(
        summary="Check user",
        description="Check if a user exists by username",
        request=serializers.UserCheckSerializer,
        responses={
            "200": OpenApiResponse(description="User exists"),
            "204": OpenApiResponse(description="User not found"),
        },
    ),
)
class UserViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = None

    def get_serializer_class(self):
        # Early exit for drf-spectacular compatibility
        if getattr(self, "swagger_fake_view", False):
            return serializers.UserSerializer

        user = self.request.user
        is_self = int(self.kwargs.get("pk", 0)) == user.id or self.action == "self"
        if user.is_staff:
            return serializers.UserSerializer if not is_self else serializers.UserSerializer
        else:
            if is_self and self.request.method in SAFE_METHODS:
                return serializers.UserSerializer
            else:
                return serializers.BasicUserSerializer

    def get_permissions(self):
        """
        Customize permissions for specific actions.
        """
        if self.action == "check":
            # Allow unauthenticated access to the 'check' action
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=["GET"])
    def self(self, request):
        """
        Method returns an instance of a user who is currently authorized
        """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def upload_avatar(self, request, pk=None):
        """
        A custom action to upload user's avatar.
        """

        user = self.get_object()
        uploaded_file = request.FILES.get("file", None)
        if uploaded_file:
            error = check_avatar(uploaded_file)
            if error is not None:
                return Response(data={"message": error}, status=status.HTTP_400_BAD_REQUEST)

        full_path = osp.join(settings.USERS_MEDIA_ROOT, str(user.id), "avatar.png")
        rel_path = osp.relpath(full_path, settings.BASE_DIR)
        fs.save(rel_path, uploaded_file)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], serializer_class=serializers.UserCheckSerializer)
    def check(self, request):
        """
        Method checks if a user exists by username, if not then check if user exists by email.
        """

        serializer = serializers.UserCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")

        if username and get_user_model().objects.filter(username=username).exists():
            return Response(status=status.HTTP_200_OK)

        if email and get_user_model().objects.filter(email=email).exists():
            return Response(status=status.HTTP_200_OK)

        # If neither username nor email exists, return 204
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterViewEx(RegisterView):
    """
    Extends the functionality of the RegisterView to handle
    user registration and response data customization.
    """

    def get_response_data(self, user):
        serializer = self.get_serializer(user)
        return serializer.data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if (
            allauth_settings.EMAIL_VERIFICATION
            != allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            if dj_rest_auth_settings.USE_JWT:
                self.access_token, self.refresh_token = jwt_encode(user)
            elif self.token_model:
                dj_rest_auth_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )

        return user


class ConfirmEmailViewEx(ConfirmEmailView):
    template_name = "account/email/email_confirmation_signup_message.html"

    def get(self, *args, **kwargs):
        try:
            if not allauth_settings.CONFIRM_EMAIL_ON_GET:
                return super().get(*args, **kwargs)
            return self.post(*args, **kwargs)
        except Http404:
            return HttpResponseRedirect(settings.INCORRECT_EMAIL_CONFIRMATION_URL)


class GoogleLogin(SocialLoginView):
    """
    Handles the OAuth2 login process for Google.
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        request = self.request
        return f"{request.scheme}://{request.get_host()}/"
