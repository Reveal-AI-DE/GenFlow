#!/bin/bash

# Export GF_VERSION as latest
export GF_VERSION=latest

# Pull the required Docker images
echo "Pulling Docker images..."
docker pull public.ecr.aws/z5d7y3x3/genflow/server:$GF_VERSION
docker pull public.ecr.aws/z5d7y3x3/genflow/ui:$GF_VERSION

# Retag the images to remove the prefix
echo "Retagging Docker images..."
docker tag public.ecr.aws/z5d7y3x3/genflow/server:$GF_VERSION genflow/server:$GF_VERSION
docker tag public.ecr.aws/z5d7y3x3/genflow/ui:$GF_VERSION genflow/ui:$GF_VERSION

# Remove the previous tags
echo "Removing previous Docker image tags..."
docker rmi public.ecr.aws/z5d7y3x3/genflow/server:$GF_VERSION
docker rmi public.ecr.aws/z5d7y3x3/genflow/ui:$GF_VERSION

# Download the docker-compose.yml file
echo "Downloading docker-compose.yml..."
curl -o docker-compose.yml https://raw.githubusercontent.com/Reveal-AI-DE/GenFlow/develop/docker-compose.yml

# Start the services using docker-compose
echo "Starting services with docker-compose..."
docker compose up -d

echo "Setup complete."
