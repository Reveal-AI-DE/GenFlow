# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import cast

from django.db.models.query import QuerySet
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

import genflow.apps.core.permissions as perms
from genflow.apps.ai.base.entities.shared import ModelType
from genflow.apps.core.config.entities import ModelWithProviderEntity
from genflow.apps.core.config.provider_service import AIProviderConfigurationService
from genflow.apps.core.models import AboutSystem, CommonEntity, Provider
from genflow.apps.core.serializers import (
    AIProviderConfigurationSerializer,
    ConfigurationEntitySerializer,
    ModelWithProviderEntitySerializer,
    ProviderReadSerializer,
    ProviderWriteSerializer,
)
from genflow.apps.team.middleware import HttpRequestWithIamContext


@extend_schema(tags=["system"])
@extend_schema_view(
    about=extend_schema(
        summary="Method provides information about the system",
        description="This method provides information about the system, "
        "including the name, version, description, and license.",
        responses={
            "200": AboutSystem,
        },
    )
)
class SystemViewSet(viewsets.ViewSet):
    """
    Provides actions related to the GenFlow platform.
    """

    serializer_class = None
    iam_team_field = None

    # To get nice documentation about SystemViewSet actions it is necessary
    # to implement the method. By default, ViewSet doesn't provide it.
    def get_serializer(self, *args, **kwargs):
        pass

    @action(detail=False, methods=["GET"], serializer_class=AboutSystem)
    def about(self, request):
        """
        Provides information about the GenFlow platform.
        """

        from genflow import __version__ as genflow_version

        about = AboutSystem(
            name={
                "en_US": "GenFlow Platform",
            },
            version=genflow_version,
            description={
                "en_US": "GenFlow is the next generation of digitalization in AI,  that helps you to develop your business uncase "
                "while significantly reduce the time and costs needed.\n"
                "The platform provides a comprehensive solution that supported you over the different model development and deployment phases.\n"
                "Using GenFlow, domain experts can develop start-of-the-art models without a single line of code.",
            },
            license={
                "en_US": "This software uses LGPL license",
            },
        )
        return Response(data=about.model_dump(mode="json"), status=status.HTTP_200_OK)


@extend_schema(tags=["providers"])
@extend_schema_view(
    create=extend_schema(
        summary="Enable an AI provider",
        description="Allows the user to configure an AI provider"
        " on the team level, to be available to the team members.",
        request=ProviderWriteSerializer,
        responses={
            201: ProviderReadSerializer,
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve an enabled AI provider",
        description="Allows the user to retrieve an enabled AI provider with its obfuscated credentials",
        responses={
            200: ProviderReadSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Disable an AI provider",
        description="Allows the user to disable an AI provider",
        responses={
            204: OpenApiResponse(description="Provider disabled successfully"),
        },
    ),
    partial_update=extend_schema(
        summary="Update an enabled AI provider",
        description="Allows the user to update an enabled AI provider credentials",
        request=ProviderWriteSerializer,
        responses={
            200: ProviderReadSerializer,
        },
    ),
    list=extend_schema(
        summary="List AI provider configurations",
        description="Allows the user to list all available (enabled/disabled) AI providers with their configurations",
        responses={
            200: AIProviderConfigurationSerializer(many=True),
        },
    ),
)
class ProviderViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.ListModelMixin,
):
    """
    ProviderViewSet is a view set for managing Provider instances. It supports
    creating, retrieving, updating, and destroying Provider objects.
    """

    queryset = Provider.objects.all()
    iam_team_field = "team"

    def get_serializer_class(self, *args, **kwargs) -> serializers.ModelSerializer:
        """
        Returns the appropriate serializer class based on the request method.
        Uses ProviderReadSerializer for safe methods (GET, HEAD, OPTIONS) and
            ProviderWriteSerializer for other methods (POST, PUT, PATCH, DELETE).
        """
        if self.request.method in SAFE_METHODS:
            return ProviderReadSerializer
        else:
            return ProviderWriteSerializer

    def get_queryset(self) -> QuerySet[Provider]:
        """
        Retrieves the queryset for the view, applying necessary filters based on the action.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.ProviderPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def perform_create(self, serializer) -> None:
        """
        Saves the serializer with additional context, including the owner
            (current user) and team (from IAM context).
        """
        request = cast(HttpRequestWithIamContext, self.request)
        extra_kwargs = {
            "owner": self.request.user,
            "team": request.iam_context.team,
        }
        serializer.save(**extra_kwargs)

    def list(self, request, *args, **kwargs) -> Response:
        """
        Retrieves a list of AI provider configurations.
        """

        queryset = self.filter_queryset(self.get_queryset())
        try:
            provider_configurations = AIProviderConfigurationService.get_configuration(
                queryset=queryset
            ).values()
        except Exception as e:
            return Response({"message": str(e)}, status=400)

        serializer = AIProviderConfigurationSerializer(provider_configurations, many=True)
        return Response({"results": serializer.data, "count": len(serializer.data)})


@extend_schema(tags=["models"])
@extend_schema_view(
    list=extend_schema(
        summary="List AI provider models",
        description="Allows the user to list all available AI provider models",
        parameters=[
            OpenApiParameter(
                name="enabled_only",
                description="If true, only enabled models will be returned",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.BOOL,
                required=False,
            ),
            OpenApiParameter(
                name="model_type",
                description="The type of the model to filter by",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                enum=[str(i) for i in ModelType],
                required=False,
            ),
        ],
        responses={
            200: ModelWithProviderEntitySerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve an AI provider model",
        description="Allows the user to retrieve an AI provider model",
        parameters=[
            OpenApiParameter(
                "provider_name",
                description="The name of the AI provider to filter by",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                required=False,
            ),
        ],
        responses={
            200: ModelWithProviderEntitySerializer,
        },
    ),
    parameter_config=extend_schema(
        summary="Retrieve parameter configurations for a model",
        description="Allows the user to retrieve the parameter configurations for a specific model",
        parameters=[
            OpenApiParameter(
                "provider_name",
                description="The name of the AI provider to filter by",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                required=False,
            ),
        ],
        responses={
            200: ConfigurationEntitySerializer(many=True),
        },
    ),
)
class AIModelViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    """
    AIModelViewSet is a view set for retrieving AI provider models.
    """

    queryset = Provider.objects.all()
    ordering_fields = ["id"]
    iam_team_field = "team"

    def get_queryset(self) -> QuerySet[Provider]:
        """
        Retrieves the queryset for the view, applying necessary filters based on the action.
        """

        queryset = super().get_queryset()

        if self.action == "list":
            perm = perms.AIModelPermission.create_scope_list(self.request)
            queryset = perm.filter(queryset)
        return queryset

    def list(self, request, *args, **kwargs) -> Response:
        """
        Retrieves a list of AI provider configurations.
        """

        enabled_only = request.query_params.get("enabled_only", False)
        model_type = request.query_params.get("model_type", None)

        queryset = self.filter_queryset(self.get_queryset())

        try:
            models = AIProviderConfigurationService.get_models(
                queryset=queryset, model_type=model_type, enabled_only=enabled_only
            )
        except Exception as e:
            return Response({"message": str(e)}, status=400)

        serializer = ModelWithProviderEntitySerializer(models, many=True)
        return Response({"results": serializer.data, "count": len(serializer.data)})

    def retrieve(self, request, pk=None, *args, **kwargs) -> Response:
        """
        Retrieves a model based on the provided model name and provider name.
        """

        model = self.get_model(request, model_name=pk)

        if model:
            serializer = ModelWithProviderEntitySerializer(model)
            return Response(serializer.data)
        else:
            return Response({"message": f"Model '{pk}' not found"}, status=404)

    @action(detail=True, methods=["GET"], serializer_class=ConfigurationEntitySerializer)
    def parameter_config(self, request, pk: str = None) -> Response:
        """
        Retrieves the parameter configurations for a specific model.
        """

        model = self.get_model(request, model_name=pk)
        if model:
            parameter_configs = AIProviderConfigurationService.get_model_parameter_configs(
                provider_name=model.provider.id, model_name=model.id
            )
            serializer = ConfigurationEntitySerializer(parameter_configs, many=True)
            return Response({"results": serializer.data, "count": len(serializer.data)})
        else:
            return Response({"message": f'Model "{pk}" not found'}, status=404)

    def get_model(self, request, model_name: str = None) -> ModelWithProviderEntity:
        """
        Retrieves a model based on the provided model name and provider name.
        """

        provider_name = request.query_params.get("provider_name", None)

        queryset = self.filter_queryset(self.get_queryset())

        model = AIProviderConfigurationService.get_model(
            model_name=model_name,
            provider_name=provider_name,
            queryset=queryset,
            enabled_only=True,
        )

        # May raise a permission denied
        self.check_object_permissions(request, model)

        return model


class EntityBaseViewSet(viewsets.ModelViewSet):
    """
    Base view set for managing entities. It provides common functionality.
    It must be inherited by other view sets that manage models that are
    subclassed from CommonEntity.
    """

    search_fields = ["name", "description"]
    filterset_fields = ["group__id", "is_pinned"]
    ordering_fields = ["name", "group__name"]
    iam_team_field = "team"

    def perform_create(self, serializer):
        """
        Saves a new instance, associating it with the current user and team.
        """

        request = cast(HttpRequestWithIamContext, self.request)
        serializer.save(
            owner=self.request.user,
            team=request.iam_context.team,
        )

    def perform_destroy(self, instance: CommonEntity):
        """
        Deletes the instance and removes its associated media directory if it exists.
        """

        instance.remove_media_dir()
        return super().perform_destroy(instance)

    @action(detail=True, methods=["post"])
    def upload_avatar(self, request, pk=None):
        """
        A custom action to upload an avatar for a specific instance.
        """

        entity: CommonEntity = self.get_object()
        entity.avatar = request.FILES.get("avatar", None)
        entity.save()
        return Response(status=status.HTTP_200_OK)
