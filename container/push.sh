#!/bin/bash
# Push image to container registry
# Usage: bash container/push.sh [registry] [username] [image] [tag]

REGISTRY=${1:-${DOCKER_REGISTRY:-docker.io}}
USERNAME=${2:-${DOCKER_USERNAME}}
IMAGE=${3:-${IMAGE_NAME:-blue_team_portal}}
TAG=${4:-${IMAGE_TAG:-latest}}

if [ -z "$USERNAME" ]; then
    echo "Error: DOCKER_USERNAME not set"
    echo "Usage: export DOCKER_USERNAME=your-username && bash container/push.sh"
    exit 1
fi

FULL_IMAGE="$REGISTRY/$USERNAME/$IMAGE:$TAG"

echo "Building image: $FULL_IMAGE"
docker build -f container/Dockerfile -t "$FULL_IMAGE" .

echo "Logging in to registry..."
docker login "$REGISTRY"

echo "Pushing image: $FULL_IMAGE"
docker push "$FULL_IMAGE"

echo "✓ Successfully pushed: $FULL_IMAGE"
