# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import time
from abc import abstractmethod
from typing import Optional, Union, Generator

from gen_flow.apps.common.entities import ConfigurationEntity
from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.base.entities.model import PricingType
from gen_flow.apps.ai.base.model_collection import ModelCollection
from gen_flow.apps.ai.llm.messages import Message
from gen_flow.apps.ai.llm.entities import Result, Usage


class LLMModelCollection(ModelCollection):
    '''
    Abstract base class that defines the interface for a collection of language models (LLMs).
    '''

    model_type: ModelType = ModelType.LLM

    @abstractmethod
    def get_tokens_counts(
        self,
        model: str,
        credentials: dict,
        messages: list[Message],
    ) -> int:
        '''
        Gets the token counts for a given model and messages.
        '''

        raise NotImplementedError


    @abstractmethod
    def _call(
        self,
        model: str,
        credentials: dict,
        messages: list[Message],
        parameters: dict,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[Result, Generator]:
        '''
        Calls the model with the given parameters and messages.
        '''

        raise NotImplementedError

    def get_parameter_configs(self, model: str) -> list[ConfigurationEntity]:
        ''''
        Retrieves the parameter configurations for a given model.
        '''

        schema = self.get_model_schema(model)

        if schema:
            return schema.parameter_configs

        return []

    def _process_model_parameters(self, model: str, model_parameters: dict) -> dict:
        '''
        Processes and validates the model parameters based on the parameter configurations.
        '''

        parameter_configs = self.get_parameter_configs(model)

        # validate model parameters
        processed_parameters = {}
        for parameter_config in parameter_configs:
            parameter_name = parameter_config.name
            parameter_value = model_parameters.get(parameter_name)
            if parameter_value is None:
                # use template value if available
                if parameter_config.use_template and parameter_config.use_template in model_parameters:
                    parameter_value = model_parameters[parameter_config.use_template]
                else:
                    if parameter_config.required:
                        if parameter_config.default is not None:
                            processed_parameters[parameter_name] = parameter_config.default
                            continue
                        else:
                            raise ValueError(f'Model {model} parameter {parameter_name} is required.')
                    else:
                        continue

            # validate value
            parameter_config.validate(parameter_value, prefix=f'Model {model} parameter')

            processed_parameters[parameter_name] = parameter_value

        return processed_parameters

    def _calculate_usage(
        self, model: str, input_tokens: int, output_tokens: int
    ) -> Usage:
        '''
        Calculates the usage and cost based on the input and output tokens.
        '''

        # get input price info
        input_price_info = self.get_price(
            model=model,
            price_type=PricingType.INPUT,
            tokens=input_tokens,
        )

        # get output price info
        output_price_info = self.get_price(
            model=model, price_type=PricingType.OUTPUT, tokens=output_tokens
        )

        # calculate usage
        usage = Usage(
            input_tokens=input_tokens,
            input_unit_price=input_price_info.unit_price,
            input_price_unit=input_price_info.unit,
            input_price=input_price_info.total_amount,
            output_tokens=output_tokens,
            output_unit_price=output_price_info.unit_price,
            output_price_unit=output_price_info.unit,
            output_price=output_price_info.total_amount,
            total_tokens=input_tokens + output_tokens,
            total_price=input_price_info.total_amount + output_price_info.total_amount,
            currency=input_price_info.currency,
            latency=time.perf_counter() - self.started_at,
        )
        return usage

    def call(
        self,
        model: str,
        credentials: dict,
        messages: list[Message],
        parameters: Optional[dict] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[Result, Generator]:
        '''
        Calls the model with the given parameters and messages, and returns the result.
        '''

        # process parameters
        if parameters is None:
            parameters = {}

        parameters = self._process_model_parameters(model, parameters)

        self.started_at = time.perf_counter()

        try:
            # ToDo: support response format
            result = self._call(model, credentials, messages, parameters, stop, stream, user)
        except Exception as e:
            # TODO: log error
            raise e

        return result
