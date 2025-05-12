# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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

import geniflow.apps.core.permissions as perms
from geniflow.apps.ai.base.entities.shared import ModelType
from geniflow.apps.common.file_utils import check_avatar
from geniflow.apps.common.log import ServerLogManager
from geniflow.apps.core.config.entities import ModelWithProviderEntity
from geniflow.apps.core.config.provider_service import AIProviderConfigurationService
from geniflow.apps.core.models import AboutSystem, CommonEntity, Provider
from geniflow.apps.core.serializers import (
    AIProviderConfigurationSerializer,
    ConfigurationEntitySerializer,
    ModelWithProviderEntitySerializer,
    ProviderReadSerializer,
    ProviderWriteSerializer,
)
from geniflow.apps.team.middleware import HttpRequestWithIamContext

slogger = ServerLogManager(__name__)


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
    Provides actions related to the GeniFlow platform.
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
        Provides information about the GeniFlow platform.
        """

        from geniflow import __version__ as geniflow_version

        about = AboutSystem(
            name={
                "en_US": "GeniFlow",
            },
            version=geniflow_version,
            description={
                "en_US": "<p>GeniFlow is an open-source, low-code GenAI platform that empowers organizations to build "
                "and manage Generative AI assistants that automate routine writing tasks and enhance access to internal knowledge.</p>"
                "Designed for flexibility and collaboration, GeniFlow enables teams to:"
                "<ul><li> Create and deploy custom AI assistants tailored to their workflows.</li>"
                "<li> Select and configure the language models best suited for their needs.</li>"
                "<li> Monitor usage patterns and performance through built-in analytics.</li>"
                "<li> Operate in a team-based environment where each team can maintain its own assistants and dedicated knowledge base.</li></ul>"
                "<p>Whether you're streamlining documentation, automating reports, or enabling internal support bots, "
                "GeniFlow helps you harness the power of GenAI — faster, smarter, and with minimal coding.</p>",
                "de_DE": "<p>GeniFlow ist eine Open-Source-Plattform für Low-Code-Generative-KI, die Organisationen dabei unterstützt, "
                "Generative KI-Assistenten zu erstellen und zu verwalten, die Routineaufgaben automatisieren und den Zugriff auf internes Wissen verbessern.</p>"
                "GeniFlow wurde für Flexibilität und Zusammenarbeit entwickelt und ermöglicht Teams:"
                "<ul><li> Individuelle KI-Assistenten zu erstellen und bereitzustellen, die auf ihre Arbeitsabläufe zugeschnitten sind.</li>"
                "<li> Die Sprachmodelle auszuwählen und zu konfigurieren, die am besten zu ihren Anforderungen passen.</li>"
                "<li> Nutzungsverhalten und Leistung durch integrierte Analysen zu überwachen.</li>"
                "<li> In einer teamorientierten Umgebung zu arbeiten, in der jedes Team seine eigenen Assistenten und dedizierten Wissensbasen verwalten kann.</li></ul>"
                "<p>Ob Sie Dokumentationen optimieren, Berichte automatisieren oder interne Support-Bots bereitstellen möchten, "
                "GeniFlow hilft Ihnen, die Kraft der Generativen KI schneller, intelligenter und mit minimalem Programmieraufwand zu nutzen.</p>",
            },
            license={
                "en_US": "This project is licensed under <a href='https://github.com/Reveal-AI-DE/GeniFlow/blob/develop/LICENSE.md' target='_blank'>GeniFlow LICENSE</a>.",
                "de_DE": "Dieses Projekt ist lizenziert unter der <a href='https://github.com/Reveal-AI-DE/GeniFlow/blob/develop/LICENSE.md' target='_blank'>GeniFlow-Lizenz</a>.",
            },
            welcome={
                "en_US": """
                    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                        <h1 style="text-align: center; color: #007fd6;">Welcome to GeniFlow!</h1>
                        <p style="text-align: center;">We are <strong>thrilled</strong> to have you on board! 🚀</p>
                        <p>Watch our <a href="https://www.youtube.com/watch?v=tP5Ox9R0naA&t=10s&ab_channel=RevealAI" target="_blank" style="color: #007BFF; text-decoration: none;">📺 YouTube video</a> to get started with GeniFlow and learn how to:</p>
                        <ul style="list-style-type: none; padding-left: 0;">
                            <li>🔧 <strong>Create an API Endpoint</strong> – Set up and configure a backend API for your GenAI integration.</li>
                            <li>✍️ <strong>Create a Prompt</strong> – Design and test custom prompts for specific writing or Q&A tasks.</li>
                            <li>🤖 <strong>Create an Assistant</strong> – Build a fully functional GenAI assistant powered by your prompt and knowledge base.</li>
                            <li>📊 <strong>View Usage Analytics</strong> – Monitor assistant activity, prompt performance, and user engagement by clicking on session properties.</li>
                        </ul>
                        <p>💻 Prefer a self-hosted solution? Follow the <a href="https://docs.geniflow.de/docs/administration/basic/installation/" target="_blank" style="color: #007BFF; text-decoration: none;">📖 Self-hosted Installation Guide</a>.</p>
                        <p>💼 We also offer <strong>enterprise support</strong> with premium features, training, and dedicated assistance with a 24-hour SLA. <a href="https://revealai.de/contact/" target="_blank" style="color: #007BFF; text-decoration: none;">📩 Contact us</a> to learn more.</p>
                    </div>
                """,
                "de_DE": """
                    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                        <h1 style="text-align: center; color: #007fd6;">Willkommen bei GeniFlow!</h1>
                        <p style="text-align: center;">Wir sind <strong>begeistert</strong>, Sie an Bord zu haben! 🚀</p>
                        <p>Sehen Sie sich unser <a href="https://www.youtube.com/watch?v=tP5Ox9R0naA&t=10s&ab_channel=RevealAI" target="_blank" style="color: #007BFF; text-decoration: none;">📺 YouTube-Video</a> an, um zu erfahren, wie Sie mit GeniFlow starten und Folgendes lernen können:</p>
                        <ul style="list-style-type: none; padding-left: 0;">
                            <li>🔧 <strong>Erstellen eines API-Endpunkts</strong> – Richten Sie eine Backend-API für Ihre GenAI-Integration ein und konfigurieren Sie sie.</li>
                            <li>✍️ <strong>Erstellen eines Prompts</strong> – Entwerfen und testen Sie benutzerdefinierte Prompts für spezifische Schreib- oder Q&A-Aufgaben.</li>
                            <li>🤖 <strong>Erstellen eines Assistenten</strong> – Erstellen Sie einen voll funktionsfähigen GenAI-Assistenten, der von Ihrem Prompt und Ihrer Wissensdatenbank unterstützt wird.</li>
                            <li>📊 <strong>Ansicht der Nutzungsanalysen</strong> – Überwachen Sie die Aktivitäten des Assistenten, die Leistung der Prompts und das Benutzerengagement, indem Sie auf Sitzungsdetails klicken.</li>
                        </ul>
                        <p>💻 Bevorzugen Sie eine selbst gehostete Lösung? Folgen Sie der <a href="https://docs.geniflow.de/docs/administration/basic/installation/" target="_blank" style="color: #007BFF; text-decoration: none;">📖 Anleitung zur Selbstinstallation</a>.</p>
                        <p>💼 Wir bieten auch <strong>Unterstützung für Unternehmen</strong> mit Premium-Funktionen, Schulungen und dedizierter Unterstützung mit einer SLA von 24 Stunden. <a href="https://revealai.de/contact/" target="_blank" style="color: #007BFF; text-decoration: none;">📩 Kontaktieren Sie uns</a>, um mehr zu erfahren.</p>
                    </div>
                """,
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
            slogger.glob.error(f"Error while retrieving AI provider configurations: {str(e)}")
            return Response("Something went wrong!", status=400)

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
            slogger.glob.error(f"Error while retrieving AI models: {str(e)}")
            return Response("Something went wrong!", status=400)

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
        if entity.avatar:
            error = check_avatar(entity.avatar.file)
            if error is not None:
                return Response(data={"message": error}, status=status.HTTP_400_BAD_REQUEST)

        entity.save()
        return Response(status=status.HTTP_200_OK)
