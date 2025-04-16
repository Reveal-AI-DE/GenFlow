# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from enum import Enum


class AUTH_ROLE(Enum):
    ADMIN = "admin"
    USER = "user"

    def __str__(self):
        return self.value
