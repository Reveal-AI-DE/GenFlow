#!/bin/sh

# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

# This is a wrapper script for running backend services. It waits for services
# the backend depends on to start before executing the backend itself.

wait-for-it "${GF_POSTGRES_HOST}:${GF_POSTGRES_PORT:-5432}" -t 10

exec "$@"
