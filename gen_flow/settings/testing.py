# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from .development import *  # noqa: F401, F403


import tempfile

_temp_dir = tempfile.TemporaryDirectory(dir=BASE_DIR, suffix="autonlp")
BASE_DIR = _temp_dir.name

CONFIG_ROOT = os.path.join(BASE_DIR, 'config')
MODEL_CONFIG_ROOT = os.path.join(CONFIG_ROOT, 'model')
