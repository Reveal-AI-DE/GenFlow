# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Any, Callable, List, Mapping, Optional

from pydantic import BaseModel, ConfigDict

from gen_flow.apps.common.entities import FileEntity
from gen_flow.apps.core.config.llm_model_bundle import LLMModelBundle
from gen_flow.apps.session.models import Session
from gen_flow.apps.session.transform.base import PromptTemplateEntity


class GenerateRequest(BaseModel):
    """
    Represents a user request to call LLM model and generate text response.
    """

    query: str
    files: Optional[List[FileEntity]] = None
    parameters: Optional[Mapping[str, Any]] = None
    user_id: Optional[str] = None
    callback: Optional[Callable] = None
    stream: Optional[bool] = None


class GenerateEntity(BaseModel):
    """
    Represents an entity to handle user request to call LLM model.
    """

    db_session: Session
    llm_model_bundle: LLMModelBundle
    prompt_entity: Optional[PromptTemplateEntity] = None
    stream: bool

    # pydantic configs
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())
