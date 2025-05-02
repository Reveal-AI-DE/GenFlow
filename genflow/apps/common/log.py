# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import logging
import sys


class ServerLogManager:
    def __init__(self, logger_name: str) -> None:
        self.glob = logging.getLogger(logger_name)


def get_logger(logger_name, log_file):
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(logging.StreamHandler(sys.stderr))
    return logger
