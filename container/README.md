# Container Configuration

This directory contains all Docker-related files for the Blue Team Portal application.

## Files

- **Dockerfile** — Multi-stage build with security hardening (non-root user, layer caching)
- **docker-compose.yml** — Production-ready composition with healthchecks and networking
- **.dockerignore** — Optimized build context exclusions
- **entrypoint.sh** — Application startup script (migrations + Gunicorn)

## Quick Start

### Build Image
```bash
docker compose -f container/docker-compose.yml build
```

### Run Container
```bash
docker compose -f container/docker-compose.yml up --pull always
```

### Push to Registry

Set environment variables first:
```bash
export DOCKER_REGISTRY=docker.io  # or your registry
export DOCKER_USERNAME=your-username
export IMAGE_NAME=blue_team_portal
export IMAGE_TAG=latest
```

Then push:
```bash
bash container/push.sh
```

## Environment Variables

Create a `.env` file in the project root:
```
SECRET_KEY=your-secure-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=sqlite:////app/database/db.sqlite3
```

## Production Deployment

1. Update `SECRET_KEY` with a secure value
2. Set `DEBUG=False`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use a persistent database (PostgreSQL recommended)
5. Run: `docker compose -f container/docker-compose.yml up --pull always`
