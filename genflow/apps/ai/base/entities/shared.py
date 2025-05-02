# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from enum import Enum


class ModelType(Enum):
    """
    An enumeration representing different types of models.

    Attributes:
        LLM (str): Represents a large language model.
    """

    LLM = "llm"

    @classmethod
    def values(cls):
        """
        Returns a list of all model type values.
        """

        return [model_type.value for model_type in cls]
