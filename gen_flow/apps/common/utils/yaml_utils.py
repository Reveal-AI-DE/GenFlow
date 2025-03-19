# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Any

import yaml
from yaml import YAMLError

def load_yaml_file(file_path: str, ignore_error: bool = True, default_value: Any = {}) -> Any:
    '''
    Load and parse a YAML file.

    Args:
        file_path (str): The path to the YAML file to be loaded.
        ignore_error (bool, optional): If True, errors during loading will be ignored
            and the default_value will be returned. Defaults to True.
        default_value (Any, optional): The value to return if the file is empty or
            an error occurs and ignore_error is True. Defaults to an empty dictionary.

    Returns:
        Any: The parsed content of the YAML file, or the
            default_value if an error occurs and ignore_error is True.

    Raises:
        YAMLError: If there is an error loading the YAML file and ignore_error is False.
        Exception: If there is an error opening the file and ignore_error is False.
    '''

    try:
        with open(file_path, encoding='utf-8') as yaml_file:
            try:
                yaml_content = yaml.safe_load(yaml_file)
                return yaml_content or default_value
            except Exception as e:
                raise YAMLError(f'Failed to load YAML file {file_path}: {e}')
    except Exception as e:
        if ignore_error:
            return default_value
        else:
            raise e
