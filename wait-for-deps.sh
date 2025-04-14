#!/bin/sh

# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

# This is a wrapper script for running backend services. It waits for services
# the backend depends on to start before executing the backend itself.

wait-for-it "${GEN_FLOW_POSTGRES_HOST}:${GEN_FLOW_POSTGRES_PORT:-5432}" -t 10

exec "$@"
