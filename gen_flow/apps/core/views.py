# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    OpenApiResponse, PolymorphicProxySerializer, OpenApiTypes,
    extend_schema_view, extend_schema, OpenApiParameter
)
from rest_framework.permissions import SAFE_METHODS

from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.core.models import AboutSystem, Provider
from gen_flow.apps.core.serializers import ProviderReadSerializer, ProviderWriteSerializer
import gen_flow.apps.core.permissions as perms


@extend_schema(tags=['system'])
@extend_schema_view(
    about=extend_schema(
        summary='Method provides information about the system',
        description='This method provides information about the system, '
            'including the name, version, description, and license.',
        responses={
            '200': AboutSystem,
        },
    )
)
class SystemViewSet(viewsets.ViewSet):
    '''
    Provides actions related to the GenFlow platform.
    '''

    serializer_class = None
    iam_team_field = None

    # To get nice documentation about SystemViewSet actions it is necessary
    # to implement the method. By default, ViewSet doesn't provide it.
    def get_serializer(self, *args, **kwargs):
        pass

    @action(detail=False, methods=['GET'], serializer_class=AboutSystem)
    def about(self, request):
        '''
        Provides information about the GenFlow platform.
        '''

        from gen_flow import __version__ as gen_flow_version

        about = AboutSystem(
            name={
                'en_US': 'GenFlow Platform',
            },
            version=gen_flow_version,
            description={
                'en_US': 'GenFlow is the next generation of digitalization in AI,  that helps you to develop your business uncase '
                    'while significantly reduce the time and costs needed.\n'
                    'The platform provides a comprehensive solution that supported you over the different model development and deployment phases.\n'
                    'Using GenFlow, domain experts can develop start-of-the-art models without a single line of code.',
            },
            license={
                'en_US': 'This software uses LGPL license',
            }
        )
        return Response(data=about.model_dump(mode='json'), status=status.HTTP_200_OK)


@extend_schema(tags=['providers'])
@extend_schema_view(
    create=extend_schema(
        summary='Enable an AI provider',
        description='Allows the user to configure an AI provider'
            ' on the team level, to be available to the team members.',
        request=ProviderWriteSerializer,
        responses={
            201: ProviderReadSerializer,
        }
    ),
    retrieve=extend_schema(
        summary='Retrieve an enabled AI provider',
        description='Allows the user to retrieve an enabled AI provider with its obfuscated credentials',
        responses={
            200: ProviderReadSerializer,
        }
    ),
    destroy=extend_schema(
        summary='Disable an AI provider',
        description='Allows the user to disable an AI provider',
        responses={
            204: 'No Content',
        }
    ),
    partial_update=extend_schema(
        summary='Update an enabled AI provider',
        description='Allows the user to update an enabled AI provider credentials',
        request=ProviderWriteSerializer,
        responses={
            200: ProviderReadSerializer,
        }
    )
)
class ProviderViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.UpdateModelMixin,
):
    queryset = Provider.objects.all()
    iam_team_field = 'team'

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return ProviderReadSerializer
        else:
            return ProviderWriteSerializer

    def perform_create(self, serializer):
        extra_kwargs = {
            'owner': self.request.user,
            'team': self.request.iam_context['team']
        }
        serializer.save(**extra_kwargs)
