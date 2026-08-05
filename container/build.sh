#!/bin/bash
# Build image locally
# Usage: bash container/build.sh [tag]

TAG=${1:-latest}
IMAGE_NAME=${IMAGE_NAME:-blue_team_portal}

echo "Building image: $IMAGE_NAME:$TAG"
docker build -f container/Dockerfile -t "$IMAGE_NAME:$TAG" .

if [ $? -eq 0 ]; then
    echo "✓ Build successful: $IMAGE_NAME:$TAG"
    docker images | grep "$IMAGE_NAME"
else
    echo "✗ Build failed"
    exit 1
fi
