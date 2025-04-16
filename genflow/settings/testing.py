# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

import tempfile

# pylint: disable=wildcard-import
from .development import *  # noqa: F401, F403

_temp_dir = tempfile.TemporaryDirectory(dir=BASE_DIR, suffix="genflow")
BASE_DIR = _temp_dir.name

CONFIG_ROOT = os.path.join(BASE_DIR, "config")
MODEL_CONFIG_ROOT = os.path.join(CONFIG_ROOT, "model")
