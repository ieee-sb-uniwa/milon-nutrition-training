# Docker Deployment Guide

## Overview

The FastAPI application is containerized with models mounted as volumes rather than bundled in the image. This approach:

- Keeps images lightweight
- Allows model updates without rebuilding
- Supports different model versions per deployment

## Quick Start

### Using Docker Compose (Recommended)

```bash
cd app/

# Start the service (models automatically mounted from ../src/models/artifacts/weights)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using Docker Directly

```bash
cd app/

# Build the image
docker build -t food-classifier:latest -f Dockerfile ..

# Run with model volume mount
docker run -p 8000:8000 \
  -v $(pwd)/../src/models/artifacts/weights:/app/models:ro \
  -e MODEL_PATH=/app/models/transfood101.pth \
  -e BASE_DIR=/app \
  food-classifier:latest
```

## Configuration

### Environment Variables

- **`BASE_DIR`**: Application base directory (default: `/app`)
- **`MODEL_PATH`**: Full path to model weights file (default: `/app/models/transfood101.pth`)
- **`HOST`**: Server host (default: `0.0.0.0`)
- **`PORT`**: Server port (default: `8000`)

### Volume Mounts

The models directory **must** be mounted as a volume:

```yaml
volumes:
  - ../src/models/artifacts/weights:/app/models:ro
```

This mounts your host model directory to `/app/models` in the container (read-only).

### Custom Model Location

```bash
# Mount from different host location
docker run -p 8000:8000 \
  -v /path/to/your/models:/app/models:ro \
  -e MODEL_PATH=/app/models/your_model.pth \
  food-classifier:latest
```

## Testing

```bash
# Check health endpoint
curl http://localhost:8000/health

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -F "image=@/path/to/food_image.jpg"
```

## Production Deployment

### 1. Update docker-compose.yml

Remove development volume mount:

```yaml
volumes:
  - ../src/models/artifacts/weights:/app/models:ro
  # Remove this line: - .:/app/app:ro
```

### 2. Add Resource Limits

```yaml
deploy:
  resources:
    limits:
      cpus: "2"
      memory: 4G
    reservations:
      cpus: "1"
      memory: 2G
```

### 3. Use Environment File

```bash
# Create .env file from template
cp .env.example .env

# Edit with your settings
nano .env

# Run with env file
docker-compose --env-file .env up -d
```

### 4. Production Considerations

- **Reverse Proxy**: Use nginx/Traefik for SSL and load balancing
- **Logging**: Configure logging driver for centralized logs
- **Monitoring**: Add health check endpoints to monitoring system
- **Secrets**: Use Docker secrets for sensitive configuration
- **Multi-stage Updates**: Test new models in staging before production

## Troubleshooting

### Container won't start

```bash
# Check if model file is accessible in container
docker exec food-classifier-api ls -la /app/models/

# View detailed logs
docker logs food-classifier-api

# Verify environment variables
docker exec food-classifier-api env | grep MODEL_PATH
```

### Model not found

- Verify host path exists: `ls -la ../src/models/artifacts/weights/`
- Check volume mount in docker-compose.yml
- Ensure MODEL_PATH matches the mounted location

### Out of memory

```bash
# Check container stats
docker stats food-classifier-api

# Increase Docker Desktop memory limit in settings
# Or add memory limits to docker-compose.yml
```

### Permission Issues

```bash
# Ensure model files are readable
chmod -R 644 ../src/models/artifacts/weights/*.pth

# Check container user
docker exec food-classifier-api whoami
```

## Directory Structure

```
app/
├── Dockerfile              # Multi-stage build definition
├── docker-compose.yml      # Orchestration configuration
├── .env.example           # Environment template
├── .dockerignore          # Build exclusions
├── README.Docker.md       # This file
├── main.py               # FastAPI application
└── ...

src/models/artifacts/weights/  # Models (mounted as volume)
└── transfood101.pth
```
