# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Mapping

from httpx import Timeout
from openai import OpenAI


class OpenAIClient(OpenAI):
    """
    Provides a client for interacting
    with the OpenAI API. It initializes the client using the provided credentials and
    transforms them into the required keyword arguments.
    """

    def __init__(self, credentials: dict):
        """
        Initializes the OpenAIClient instance with the given credentials.
        """

        # transform credentials to kwargs for model instance
        credentials_kwargs = self._to_credential_kwargs(credentials)

        # init model client
        super().__init__(**credentials_kwargs)

    def _to_credential_kwargs(self, credentials: Mapping) -> dict:
        """
        Converts the provided credentials into a dictionary of keyword arguments
            required for initializing the OpenAI client. This includes API key, timeout
            settings, base URL (if provided), and organization (if provided).
        """

        credentials_kwargs = {
            "api_key": credentials["openai_api_key"],
            "timeout": Timeout(315.0, read=300.0, write=10.0, connect=5.0),
            "max_retries": 1,
        }

        if credentials.get("openai_api_base"):
            openai_api_base = credentials["openai_api_base"].rstrip("/")
            credentials_kwargs["base_url"] = openai_api_base + "/v1"

        if "openai_organization" in credentials:
            credentials_kwargs["organization"] = credentials["openai_organization"]

        return credentials_kwargs
