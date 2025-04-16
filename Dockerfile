# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

ARG PIP_VERSION=24.0
ARG BASE_IMAGE=ubuntu:24.04

FROM ${BASE_IMAGE} AS build-image-base

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -yq \
    curl \
    git \
    pkg-config \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

ARG PIP_VERSION
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN --mount=type=cache,target=/root/.cache/pip/http \
    python3 -m pip install -U pip==${PIP_VERSION} --break-system-packages

FROM build-image-base AS build-image

COPY genflow/requirements/ /tmp/genflow/requirements/

ARG GF_CONFIGURATION="production"

RUN --mount=type=cache,target=/root/.cache/pip/http-v2 \
    python3 -m pip wheel --no-deps \
    -r /tmp/genflow/requirements/${GF_CONFIGURATION}.txt \
    -w /tmp/wheelhouse

FROM ${BASE_IMAGE}

ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG socks_proxy
ARG TZ="Etc/UTC"

ENV TERM=xterm \
    http_proxy=${http_proxy}   \
    https_proxy=${https_proxy} \
    no_proxy=${no_proxy} \
    socks_proxy=${socks_proxy} \
    LANG="C.UTF-8"  \
    LC_ALL="C.UTF-8" \
    TZ=${TZ}

ARG USER="django"
ARG GF_CONFIGURATION="production"
ENV DJANGO_SETTINGS_MODULE="genflow.settings.${GF_CONFIGURATION}"

# Install necessary apt packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -yq \
    adduser \
    bzip2 \
    ca-certificates \
    curl \
    git \
    libpython3.12 \
    nginx \
    p7zip-full \
    python3 \
    python3-setuptools \
    python3-venv \
    supervisor \
    tzdata \
    wait-for-it \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# Add a non-root user
ENV USER=${USER}
ENV HOME=/home/${USER}
RUN adduser --shell /bin/bash --disabled-password --gecos "" ${USER}

ARG CLAM_AV="no"
RUN if [ "$CLAM_AV" = "yes" ]; then \
        apt-get update && \
        apt-get --no-install-recommends install -yq \
            clamav \
            libclamunrar9 && \
        sed -i "s/ReceiveTimeout 30/ReceiveTimeout 300/g" /etc/clamav/freshclam.conf && \
        freshclam && \
        chown -R ${USER}:${USER} /var/lib/clamav && \
        rm -rf /var/lib/apt/lists/*; \
    fi

# Install wheels from the build image
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ARG PIP_VERSION
ARG PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m pip install -U pip==${PIP_VERSION}
RUN --mount=type=bind,from=build-image,source=/tmp/wheelhouse,target=/mnt/wheelhouse \
    python -m pip install --no-index /mnt/wheelhouse/*.whl

ENV NUMPROCS=1

# These variables are required for supervisord substitutions in files
# This library allows remote python debugging with VS Code
ARG GF_DEBUG_ENABLED
RUN if [ "${GF_DEBUG_ENABLED}" = "yes" ]; then \
    python3 -m pip install --no-cache-dir debugpy; \
    fi

# Install and initialize GF, copy all necessary files
COPY genflow/nginx.conf /etc/nginx/nginx.conf
COPY --chown=${USER} supervisord/ ${HOME}/supervisord
COPY --chown=${USER} manage.py backend_entrypoint.sh wait-for-deps.sh ${HOME}/
COPY --chown=${USER} genflow/ ${HOME}/genflow
COPY --chown=${USER} config/ ${HOME}/config

ARG COVERAGE_PROCESS_START
RUN if [ "${COVERAGE_PROCESS_START}" ]; then \
    echo "import coverage; coverage.process_startup()" > /opt/venv/lib/python3.12/site-packages/coverage_subprocess.pth; \
    fi

# RUN all commands below as "django" user
USER ${USER}
WORKDIR ${HOME}

RUN mkdir -p data keys logs /tmp/supervisord statics

EXPOSE 8080
ENTRYPOINT ["./backend_entrypoint.sh"]