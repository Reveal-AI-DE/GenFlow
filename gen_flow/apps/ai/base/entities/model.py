# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from decimal import Decimal
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.common.entities import BaseYamlEntity, ConfigurationEntity


class Feature(Enum):
    """
    Represents different model features.
    """

    TOOL_CALL = "tool-call"
    MULTI_TOOL_CALL = "multi-tool-call"
    AGENT_THOUGHT = "agent-thought"
    VISION = "vision"
    STREAM_TOOL_CALL = "stream-tool-call"


class PropertyKey(Enum):
    """
    Represents keys for model properties.
    """

    MODE = "mode"
    CONTEXT_SIZE = "context_size"


class CommonModelEntity(BaseYamlEntity):
    """
    Represents a model entity with common attributes.
    """

    id: str
    type: ModelType
    features: Optional[list[Feature]] = None
    properties: dict[PropertyKey, Any]
    deprecated: bool = False


class DefaultParameterName(str, Enum):
    TEMPERATURE = "temperature"
    TOP_P = "top_p"
    TOP_K = "top_k"
    PRESENCE_PENALTY = "presence_penalty"
    FREQUENCY_PENALTY = "frequency_penalty"
    MAX_TOKENS = "max_tokens"

    @classmethod
    def value_of(cls, value: Any) -> "DefaultParameterName":
        """
        Get parameter name from value.

        :param value: parameter value
        :return: parameter name
        """
        for name in cls:
            if name.value == value:
                return name
        raise ValueError(f"invalid parameter name {value}")


class PricingConfig(BaseModel):
    """
    Represents the configuration for pricing.
    """

    input: Decimal
    output: Optional[Decimal] = None
    unit: Decimal
    currency: str


class ModelEntity(CommonModelEntity):
    """
    Extends CommonModelEntity by adding parameter configs and pricing.
    """

    parameter_configs: list[ConfigurationEntity] = []
    pricing: Optional[PricingConfig] = None


class PricingType(Enum):
    """
    Represents different types of pricing.
    """

    INPUT = "input"
    OUTPUT = "output"


class PricingDetails(BaseModel):
    """
    Represents pricing details.
    """

    unit_price: Decimal
    unit: Decimal
    total_amount: Decimal
    currency: str
