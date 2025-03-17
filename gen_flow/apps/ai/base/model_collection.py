# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import os
import decimal
from os import path as osp
from typing import Optional

from gen_flow.apps.common.utils.yaml_utils import load_yaml_file
from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.base.entities.model import (ConfigurationEntity, ModelEntity,
    DefaultParameterName, PricingConfig, PricingType, PricingDetails)


class ModelCollection:
    '''
    Represents a collection of models of the same type and same provider.
    '''

    DEFAULT_PARAMETERS_FILE_NAME = '_defaults.yaml'
    LISTING_FILE_NAME = '_listing.yaml'

    # .../provider/type/**schemas.yaml
    config_path: str = ''
    schemas: Optional[list[ModelEntity]] = None
    default_parameter_configs: Optional[dict] = None

    def get_models(self) -> list[ModelEntity]:
        '''
        Retrieves and returns a list of model schemas as ModelEntity objects.

        Returns:
            list[ModelEntity]: A list of ModelEntity objects representing the model schemas.

        Raises:
            Exception: If there is an error loading or processing a model schema YAML file.
        '''

        if self.schemas:
            return self.schemas

        schemas = []

        # get type
        model_type = self.config_path.split('/')[-1]

        # get provider name
        provider_name = self.config_path.split('/')[-2]

        # get all yaml files path under provider_model_type_path that do not start with _
        schema_yaml_paths = [
            osp.join(self.config_path, model_schema_yaml)
            for model_schema_yaml in os.listdir(self.config_path)
            if not model_schema_yaml.startswith('__')
            and not model_schema_yaml.startswith('_')
            and os.path.isfile(os.path.join(self.config_path, model_schema_yaml))
            and model_schema_yaml.endswith('.yaml')
        ]

        # get _order.yaml file path
        model_listing_order = self._get_listing()

        # traverse all model_schema_yaml_paths
        for schema_yaml_path in schema_yaml_paths:
            try:
                # read yaml data from yaml file
                yaml_data = load_yaml_file(file_path=schema_yaml_path, ignore_error=False)
            except Exception as e:
                # TODO: log error
                raise Exception(f'Failed to load model schema from {schema_yaml_path}: {str(e)}')

            new_parameter_configs = []
            for parameter_config in yaml_data.get('parameter_configs', []):
                if 'use_template' in parameter_config:
                    try:
                        default_parameter_name = DefaultParameterName.value_of(parameter_config['use_template'])
                        default_parameter_config = self._get_default_parameter_config(default_parameter_name)
                        copy_default_parameter_rule = default_parameter_config.copy()
                        copy_default_parameter_rule.update(parameter_config)
                        parameter_config = copy_default_parameter_rule
                    except ValueError:
                        pass

                if 'label' not in parameter_config:
                    parameter_config['label'] = {'en_US': parameter_config['name']}

                new_parameter_configs.append(parameter_config)

            yaml_data['parameter_configs'] = new_parameter_configs

            if 'label' not in yaml_data:
                yaml_data['label'] = {'en_US': yaml_data['model']}

            try:
                # yaml_data to entity
                model_schema = ModelEntity(**yaml_data)
            except Exception as e:
                model_schema_yaml_file_name = os.path.basename(schema_yaml_path).rstrip('.yaml')
                # TODO: log error
                raise Exception(
                    f'Invalid model schema for {provider_name}.{model_type}.{model_schema_yaml_file_name}: {str(e)}'
                )

            # cache model schema
            schemas.append(model_schema)

        # resort model schemas by position
        schemas = sorted(schemas, key=lambda x: model_listing_order.get(x.id, float('inf')))

        # cache model schemas
        self.schemas = schemas

        return schemas

    def get_model_schema(self, model: str) -> Optional[ModelEntity]:
        '''
        Get model schema by model name
        '''

        # get predefined models (predefined_models)
        models = self.get_models()

        model_map = {model.id: model for model in models}
        if model in model_map:
            return model_map[model]

        return None

    def get_price(self, model: str, price_type: PricingType, tokens: int) -> PricingDetails:
        # get model schema
        model_schema = self.get_model_schema(model)

        # get price info from model schema
        price_config: Optional[PricingConfig] = None
        if model_schema and model_schema.pricing:
            price_config = model_schema.pricing

        # get unit price
        unit_price = None
        if price_config:
            if price_type == PricingType.INPUT:
                unit_price = price_config.input
            elif price_type == PricingType.OUTPUT and price_config.output is not None:
                unit_price = price_config.output

        if unit_price is None:
            return PricingDetails(
                unit_price=decimal.Decimal('0.0'),
                unit=decimal.Decimal('0.0'),
                total_amount=decimal.Decimal('0.0'),
                currency='USD',
            )

        # calculate total amount
        total_amount = tokens * unit_price * price_config.unit
        total_amount = total_amount.quantize(decimal.Decimal('0.0000001'), rounding=decimal.ROUND_HALF_UP)

        return PricingDetails(
            unit_price=unit_price,
            unit=price_config.unit,
            total_amount=total_amount,
            currency=price_config.currency,
        )

    def _get_default_parameter_configs(self) -> dict:
        '''
        Retrieves the default parameter configurations.

        Returns:
            dict: A dictionary containing the default parameter configurations.

        Raises:
            Exception: If there is an error loading the YAML file or if the YAML data is invalid.
        '''

        if self.default_parameter_configs:
            return self.default_parameter_configs

        default_parameter_configs = {}
        default_parameters_file_path = osp.join(self.config_path, self.DEFAULT_PARAMETERS_FILE_NAME)

        try:
            # read yaml data from yaml file
            yaml_data = load_yaml_file(file_path=default_parameters_file_path, ignore_error=False)
        except Exception as e:
            # TODO: log error
            raise Exception(f'Failed to load default parameters from {default_parameters_file_path}: {str(e)}')

        try:
            for parameter, parameter_config in yaml_data.items():
                if 'label' not in parameter_config:
                    parameter_config['label'] = {'en_US': parameter_config['name']}

                ConfigurationEntity(name=parameter, **parameter_config)
                default_parameter_configs[parameter] = parameter_config
        except Exception as e:
            # TODO: log error
            raise Exception(f'Invalid default parameters in {default_parameters_file_path}: {str(e)}')

        # cache model schemas
        self.default_parameter_configs = default_parameter_configs

        return default_parameter_configs

    def _get_default_parameter_config(self, name: DefaultParameterName) -> dict:
        '''
        Retrieve the default parameter configuration for a given parameter name.

        Returns:
            dict: The default parameter configuration associated with the given name.

        Raises:
            Exception: If the parameter configuration name is invalid or not found.
        '''

        if not self.default_parameter_configs:
            self._get_default_parameter_configs()

        default_parameter_config = self.default_parameter_configs.get(name)

        if not default_parameter_config:
            # TODO: log error
            raise Exception(f'Invalid model parameter config name {name.value}')

        return default_parameter_config


    def _get_listing(self) -> dict[str, int]:
        '''
        Retrieves a dictionary mapping model names to their positions from a YAML listing file.

        Returns:
            dict[str, int]: A dictionary mapping model names to their positions.

        Raises:
            Exception: If there is an error reading or processing the YAML file.
        '''

        listing_file_path = osp.join(self.config_path, self.LISTING_FILE_NAME)

        try:
            # read yaml data from yaml file
            yaml_content = load_yaml_file(file_path=listing_file_path, ignore_error=False)
            positions = [item.strip() for item in yaml_content if item and isinstance(item, str) and item.strip()]
            return {name: index for index, name in enumerate(positions)}
        except Exception as e:
            # TODO: log error
            raise Exception(f'Failed to load models listing from {listing_file_path}: {str(e)}')
