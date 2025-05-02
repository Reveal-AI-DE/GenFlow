# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import tempfile

# pylint: disable=wildcard-import
from .development import *  # noqa: F401, F403

_temp_dir = tempfile.TemporaryDirectory(dir=BASE_DIR, suffix="genflow")
BASE_DIR = _temp_dir.name

CONFIG_ROOT = os.path.join(BASE_DIR, "config")
MODEL_CONFIG_ROOT = os.path.join(CONFIG_ROOT, "model")

DATA_ROOT = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_ROOT, exist_ok=True)

ASSISTANTS_ROOT = os.path.join(DATA_ROOT, "assistants")
os.makedirs(ASSISTANTS_ROOT, exist_ok=True)

SESSIONS_ROOT = os.path.join(DATA_ROOT, "sessions")
os.makedirs(SESSIONS_ROOT, exist_ok=True)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(DATA_ROOT, "media")
os.makedirs(MEDIA_ROOT, exist_ok=True)

PROVIDERS_URL = "/media/providers"
PROVIDERS_ROOT = os.path.join(MEDIA_ROOT, "providers")
os.makedirs(PROVIDERS_ROOT, exist_ok=True)

USERS_MEDIA_URL = "/media/users"
USERS_MEDIA_ROOT = os.path.join(MEDIA_ROOT, "users")
os.makedirs(USERS_MEDIA_ROOT, exist_ok=True)

PROMPTS_MEDIA_ROOT = os.path.join(MEDIA_ROOT, "prompts")
os.makedirs(PROMPTS_MEDIA_ROOT, exist_ok=True)

ASSISTANT_MEDIA_ROOT = os.path.join(MEDIA_ROOT, "assistants")
os.makedirs(ASSISTANT_MEDIA_ROOT, exist_ok=True)

LOGS_ROOT = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_ROOT, exist_ok=True)

# Suppress all logs by default
for logger in LOGGING["loggers"].values():
    if isinstance(logger, dict) and "level" in logger:
        logger["level"] = "ERROR"

LOGGING["handlers"]["server_file"] = LOGGING["handlers"]["console"]
