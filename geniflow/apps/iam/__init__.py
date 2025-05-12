# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from enum import Enum


class AUTH_ROLE(Enum):
    ADMIN = "admin"
    USER = "user"

    def __str__(self):
        return self.value
