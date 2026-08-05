# Container Files Manifest
# This file tracks all Docker artifacts in the container/ directory

FILES:
  Dockerfile                 - Multi-stage Python image build
  docker-compose.yml        - Docker Compose orchestration
  .dockerignore             - Build context optimization
  entrypoint.sh             - Application startup script
  README.md                 - Container documentation
  build.sh                  - Local build script
  push.sh                   - Registry push script
  MANIFEST.md               - This file

REGISTRY PATHS:
  Build context:     . (project root)
  Dockerfile:        container/Dockerfile
  Compose file:      container/docker-compose.yml
  Entry point:       container/entrypoint.sh

COMMANDS:
  Local build:       bash container/build.sh
  Docker Compose:    docker compose -f container/docker-compose.yml up
  Push to registry:  bash container/push.sh [registry] [username] [image] [tag]

ENVIRONMENT:
  .env file location: Project root (./)
  Env file ref:      docker-compose.yml (env_file: - ../.env)
