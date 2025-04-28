# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from collections.abc import Iterable

from django.db.models import Q
from django.db.models.query import QuerySet
from drf_spectacular.utils import OpenApiParameter
from rest_framework.filters import BaseFilterBackend

from genflow.apps.team.middleware import HttpRequestWithIamContext

TEAM_OPEN_API_PARAMETERS = [
    OpenApiParameter(
        name="team",
        type=int,
        required=False,
        location=OpenApiParameter.QUERY,
        description="Team identifier",
    ),
    OpenApiParameter(
        name="X-Team",
        type=str,
        required=False,
        location=OpenApiParameter.HEADER,
        description="Team identifier",
    ),
]


class TeamFilterBackend(BaseFilterBackend):
    """
    A filter backend that filters querysets based on team-related parameters.
    """

    def _parameter_is_provided(self, request):
        """
        Checks if any of the team-related parameters are provided in the request headers or query parameters.
        """

        for parameter in TEAM_OPEN_API_PARAMETERS:
            if parameter.location == "header" and parameter.name in request.headers:
                return True
            elif parameter.location == "query" and parameter.name in request.query_params:
                return True
        return False

    def _construct_filter_query(self, team_fields, team_id):
        """
        Constructs a filter query based on the provided team fields and team ID.
        """

        if isinstance(team_fields, str):
            return Q(**{team_fields: team_id})

        if isinstance(team_fields, Iterable):
            # we select all db records where AT LEAST ONE team field is equal team_id
            operation = Q.OR

            if team_id is None:
                # but to get all non-team objects we need select db records where ALL team fields are None
                operation = Q.AND

            filter_query = Q()
            for team_field in team_fields:
                filter_query.add(Q(**{team_field: team_id}), operation)

            return filter_query

        return Q()

    def filter_queryset(self, request: HttpRequestWithIamContext, queryset: QuerySet, view):
        """
        Filters the queryset based on the team context in the request.
        Returns only non-team objects if no team is specified.
        """

        if view.detail or not view.iam_team_field:
            return queryset

        visibility = None
        team = request.iam_context.team

        if team:
            visibility = {"team": team.id}

        elif not team and self._parameter_is_provided(request):
            visibility = {"team": None}

        if visibility:
            team_id = visibility.pop("team")
            query = self._construct_filter_query(view.iam_team_field, team_id)

            return queryset.filter(query).distinct()

        return queryset

    def get_schema_operation_parameters(self, view):
        """
        Returns the schema operation parameters for the team-related filters.
        """

        if not view.iam_team_field or view.detail:
            return []

        parameters = []
        for parameter in TEAM_OPEN_API_PARAMETERS:
            parameter_type = None

            if parameter.type == int:
                parameter_type = "integer"
            elif parameter.type == str:
                parameter_type = "string"

            parameters.append(
                {
                    "name": parameter.name,
                    "in": parameter.location,
                    "description": parameter.description,
                    "schema": {"type": parameter_type},
                }
            )

        return parameters
