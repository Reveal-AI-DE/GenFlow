# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from abc import ABC, abstractmethod
from os import path as osp
from typing import Optional

from genflow.apps.ai.base.entities.model import ModelEntity
from genflow.apps.ai.base.entities.provider import AIProviderEntity
from genflow.apps.ai.base.entities.shared import ModelType
from genflow.apps.ai.base.model_collection import ModelCollection
from genflow.apps.common.log import ServerLogManager
from genflow.apps.common.utils.yaml_utils import load_yaml_file

slogger = ServerLogManager(__name__)


class AIProvider(ABC):

    def __init__(self) -> None:
        # .../provider/provider.yaml
        self.config_path: str = ""
        self.schema: Optional[AIProviderEntity] = None
        self.model_collections_map: dict[str, ModelCollection] = {}

    @abstractmethod
    def validate_credentials(self, credentials: dict) -> None:
        """
        Validate provider credentials
        """

        raise NotImplementedError

    def get_schema(self) -> AIProviderEntity:
        """
        Retrieves the AI provider schema.

        Returns:
            AIProviderEntity: The provider schema entity.

        Raises:
            Exception: If there is an error loading the YAML file or if the YAML
                data is invalid.
        """

        if self.schema:
            return self.schema

        provider_name = self.config_path.split("/")[-1]

        yaml_path = osp.join(self.config_path, f"{provider_name}.yaml")
        try:
            # read provider schema from yaml file
            yaml_data = load_yaml_file(file_path=yaml_path, ignore_error=False)
        except Exception as e:
            message = f"Error loading provider schema for {provider_name}: {str(e)}"
            slogger.glob.error(message)
            raise Exception(message)

        try:
            # yaml_data to entity
            schema = AIProviderEntity(**yaml_data)
        except Exception as e:
            message = f"Invalid provider schema for {provider_name}: {str(e)}"
            slogger.glob.error(message)
            raise Exception(message)

        # cache schema
        self.schema = schema

        return schema

    def get_models(self, model_type: str) -> list[ModelEntity]:
        """
        Retrieve a list of models based on the specified model type.

        Returns:
            list[ModelEntity]: A list of models corresponding to the specified model type.
            If the model type is not supported, an empty list is returned.
        """

        provider_schema = self.get_schema()
        if ModelType(model_type) not in provider_schema.supported_model_types:
            return []

        # get model collection instance of the model type
        model_collection = self.get_model_collection_instance(model_type)

        # get predefined models (predefined_models)
        models = model_collection.get_models()

        # return models
        return models

    def add_model_collection_instance(self, config_path: str, model_cls: ModelCollection) -> None:
        """
        Adds an instance of a model collection to the provider's model collections map.

        Raises:
            Exception: If the model type derived from the config_path is not supported by the provider.
            Exception: If the provided model_cls is not a subclass of ModelCollection.
        """

        model_type = config_path.split("/")[-1].replace("_", "-")
        if ModelType(model_type) not in self.get_schema().supported_model_types:
            raise Exception(f"Model type {model_type} is not supported by the provider")

        provider_name = config_path.split("/")[-2]

        if model_cls.__abstractmethods__ or not issubclass(model_cls, ModelCollection):
            raise Exception(
                f"Missing ModelCollection class for model type {model_type} in {provider_name}"
            )

        model_collection_instance = model_cls()
        model_collection_instance.config_path = config_path
        self.model_collections_map[f"{provider_name}.{model_type}"] = model_collection_instance

    def get_model_collection_instance(self, model_type: str) -> ModelCollection:
        """
        Retrieves an instance of ModelCollection based on the provided model type.

        Returns:
            ModelCollection: An instance of the ModelCollection corresponding to the given model type.

        Raises:
            Exception: If the provided model type is not supported by the provider.
            Exception: If the ModelCollection instance is not found for the given provider and model type.
        """

        if ModelType(model_type) not in self.get_schema().supported_model_types:
            raise Exception(f"Model type {model_type} is not supported by the provider")

        provider_name = self.config_path.split("/")[-1]

        if f"{provider_name}.{model_type}" in self.model_collections_map:
            return self.model_collections_map[f"{provider_name}.{model_type}"]
        else:
            raise Exception(f"ModelCollection instance not found for {provider_name}.{model_type}")
