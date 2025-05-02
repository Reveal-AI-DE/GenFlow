# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from genflow.apps.ai.llm.messages import AssistantMessage, Message


class Usage(BaseModel):
    input_tokens: int
    input_unit_price: Decimal
    input_price_unit: Decimal
    input_price: Decimal
    output_tokens: int
    output_unit_price: Decimal
    output_price_unit: Decimal
    output_price: Decimal
    total_tokens: int
    total_price: Decimal
    currency: str
    latency: float

    @classmethod
    def empty_usage(cls):
        return cls(
            input_tokens=0,
            input_unit_price=Decimal("0.0"),
            input_price_unit=Decimal("0.0"),
            input_price=Decimal("0.0"),
            output_tokens=0,
            output_unit_price=Decimal("0.0"),
            output_price_unit=Decimal("0.0"),
            output_price=Decimal("0.0"),
            total_tokens=0,
            total_price=Decimal("0.0"),
            currency="USD",
            latency=0.0,
        )


class Result(BaseModel):
    model: str
    messages: list[Message]
    message: AssistantMessage
    usage: Usage
    system_fingerprint: Optional[str] = None


class ResultChunkDelta(BaseModel):
    index: int
    message: AssistantMessage
    usage: Optional[Usage] = None
    finish_reason: Optional[str] = None


class ResultChunk(BaseModel):
    model: str
    messages: list[Message]
    system_fingerprint: Optional[str] = None
    delta: ResultChunkDelta
