# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional


class WebSocketError(Exception):
    """Base class for all websocket exceptions."""

    description: Optional[str] = None

    def __init__(self, description: Optional[str] = None) -> None:
        self.description = description

    def __str__(self):
        return self.description or self.__class__.__name__


class BadRequestError(WebSocketError):
    """Raised when the request contains invalid data."""

    description = "Bad Request"


class ForbiddenError(WebSocketError):
    """Raised when the request contains invalid data."""

    description = "Request not allowed"


class NotFoundError(WebSocketError):
    """Raised when the request contains invalid data."""

    description = "Requested resource not found"
