# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import shutil
from os import path as osp
from typing import cast

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.crypto import get_random_string
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

import genflow.apps.team.models as models
import genflow.apps.team.permissions as perms
import genflow.apps.team.serializers as serializers
from genflow.apps.team.middleware import HttpRequestWithIamContext


@extend_schema(tags=["teams"])
@extend_schema_view(
    list=extend_schema(
        summary="List teams",
        description="Retrieve a list of all teams. Supports "
        "filtering and searching by name and owner username.",
        responses={
            "200": serializers.TeamReadSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Get team details",
        description="Retrieve detailed information about a specific team by its ID.",
        responses={
            "200": serializers.TeamReadSerializer,
        },
    ),
    create=extend_schema(
        summary="Create a team",
        description="Create a new team with the provided details.",
        request=serializers.TeamWriteSerializer,
        responses={
            "201": serializers.TeamReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Updates a team",
        description="Partially update the details of a specific team."
        "Only the provided fields will be updated.",
        request=serializers.TeamWriteSerializer(partial=True),
        responses={
            "200": serializers.TeamReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete a team",
        description="Delete a specific team by its ID.",
        responses={
            "204": OpenApiResponse(description="The team has been deleted"),
        },
    ),
)
class TeamViewSet(viewsets.ModelViewSet):
    """
    TeamViewSet is a viewset for handling CRUD operations on the Team model.
    """

    queryset = models.Team.objects.select_related("owner").all()
    search_fields = ("name", "owner__username")
    filterset_fields = list(search_fields) + ["id"]
    ordering_fields = list(filterset_fields)
    ordering = "-id"
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    iam_team_field = None

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.'
        """

        if self.request.method in SAFE_METHODS:
            return serializers.TeamReadSerializer
        else:
            return serializers.TeamWriteSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for the view, applying necessary filters based on the action.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.TeamPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def perform_create(self, serializer):
        """
        Saves the serializer with additional keyword arguments.
        """

        extra_kwargs = {"owner": self.request.user}
        serializer.save(**extra_kwargs)

    def perform_destroy(self, instance: models.Team):
        """
        Deletes a Team instance and removes its associated directories if it exists.
        """

        key_dir = osp.join(settings.BASE_DIR, "keys", "teams", str(instance.id))
        if osp.exists(key_dir):
            shutil.rmtree(key_dir)
        return super().perform_destroy(instance)


@extend_schema(tags=["memberships"])
@extend_schema_view(
    list=extend_schema(
        summary="List memberships",
        description="Retrieve a list of all memberships."
        "Supports filtering and searching by user username and role.",
        responses={
            "200": serializers.MembershipReadSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Get membership details",
        description="Retrieve detailed information about a specific membership by its ID.",
        responses={
            "200": serializers.MembershipReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Update a membership",
        description="Partially update the details of a specific membership."
        "Only the provided fields will be updated.",
        request=serializers.MembershipWriteSerializer(partial=True),
        responses={
            "200": serializers.MembershipReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete a membership",
        description="Delete a specific membership by its ID.",
        responses={
            "204": OpenApiResponse(description="The membership has been deleted"),
        },
    ),
)
class MembershipViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    MembershipViewSet is a viewset for handling CRUD operations on the Membership model.
    """

    queryset = models.Membership.objects.select_related("invitation", "user").all()
    http_method_names = ["get", "patch", "delete", "head", "options"]
    search_fields = ("user__username", "role")
    filterset_fields = list(search_fields) + ["id"]
    ordering_fields = list(filterset_fields)
    ordering = "-joined_date"
    iam_team_field = "team"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.
        """

        if self.request.method in SAFE_METHODS:
            return serializers.MembershipReadSerializer
        else:
            return serializers.MembershipWriteSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for the view, applying necessary filters based on the action.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.MembershipPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset


@extend_schema(tags=["invitations"])
@extend_schema_view(
    list=extend_schema(
        summary="List invitations",
        description="Retrieve a list of all invitations. Supports filtering and "
        "searching by owner username, membership user ID, and membership active status.",
        responses={
            "200": serializers.InvitationReadSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Get invitation details",
        description="Retrieve detailed information about a specific invitation by its ID.",
        responses={
            "200": serializers.InvitationReadSerializer,
        },
    ),
    create=extend_schema(
        summary="Create an invitation",
        description="Create a new invitation with the provided details.",
        request=serializers.InvitationWriteSerializer(),
        responses={
            "201": serializers.InvitationReadSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Update an invitation",
        description="Partially update the details of a specific invitation. "
        "Only the provided fields will be updated.",
        request=serializers.InvitationWriteSerializer(partial=True),
        responses={
            "200": serializers.InvitationReadSerializer,
        },
    ),
)
class InvitationViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    """
    InvitationViewSet is a viewset for handling CRUD operations on the Invitation model.
    """

    queryset = models.Invitation.objects.select_related("owner").all()
    http_method_names = ["get", "post", "patch", "head", "options"]
    iam_team_field = "membership__team"

    search_fields = ("owner__username", "membership__user__id", "membership__is_active")
    filterset_fields = list(search_fields)
    ordering_fields = list(filterset_fields) + ["created_date"]
    ordering = "-created_date"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.
        """

        if self.request.method in SAFE_METHODS:
            return serializers.InvitationReadSerializer
        else:
            return serializers.InvitationWriteSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for the view, applying necessary filters based on the action.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.InvitationPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new invitation.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ImproperlyConfigured:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data="Email backend is not configured.",
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Saves the serializer with additional keyword arguments.
        """
        request = cast(HttpRequestWithIamContext, self.request)
        serializer.save(
            owner=self.request.user,
            key=get_random_string(length=64),
            team=request.iam_context.team,
        )

    def perform_update(self, serializer):
        """
        Updates the invitation instance.
        """

        if "accepted" in self.request.query_params:
            serializer.instance.accept()
        else:
            super().perform_update(serializer)
