# Model Deployment Wiki

A concise reference for building, testing, tagging, and pushing a Dockerized FastAPI model service to DigitalOcean Container Registry.

> **Convention used in examples**
>
> - Registry: `registry.digitalocean.com/aisg-registry`
> - Image name: `food-classifier`
> - Replace these with the values for your service.

---

## 1. Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed locally

```bash
# Authenticate Docker with the registry
docker login registry.digitalocean.com/aisg-registry
```

---

## 2. Project structure

Every model service should follow this layout:

```
my-model-api/
├── app/                  # application source code only
│   ├── __init__.py
│   ├── main.py           # FastAPI app + endpoints
│   ├── model.py          # inference logic
│   └── utils/
├── weights/              # model weights (not tracked in git)
│   └── model.pth
├── Dockerfile
├── requirements.txt      # full deps (GPU / local dev)
├── requirements-cpu.txt  # CPU-only deps (used by Docker)
├── .env.example          # documented env vars, no secrets
└── .dockerignore
```

Key rules:

- **Never bake weights into the image.** Mount them at runtime via `-v`.
- **Never commit `.env`** — only `.env.example`.
- Use `requirements-cpu.txt` in the Dockerfile to avoid the ~3.5 GB CUDA torch wheel.

---

## 3. Build

Run from the service directory (where the `Dockerfile` lives):

```bash
docker build -t food-classifier .
```

To build for a specific platform (required when building on Apple Silicon for a Linux droplet):

```bash
docker build --platform linux/amd64 -t food-classifier .
```

---

## 4. Run locally

```bash
cp .env.example .env   # once — then edit as needed

docker run -d \
  --name food-classifier-api \
  --env-file .env \
  -v ./models:/app/models:ro \
  -p 8000:8000 \
  food-classifier
```

| Flag                         | Purpose                                |
| ---------------------------- | -------------------------------------- |
| `--env-file .env`            | Inject environment variables from file |
| `-v ./models:/app/models:ro` | Mount model weights read-only          |
| `-p 8000:8000`               | Expose the API on localhost            |
| `-d`                         | Run detached (background)              |

---

## 5. Test

**Health check:**

```bash
curl http://localhost:8000/health
```

**Prediction:**

```bash
curl -X POST http://localhost:8000/predict \
  -F "image=@/path/to/food.jpg"
```

**Container logs:**

```bash
docker logs food-classifier-api
docker logs -f food-classifier-api   # follow
```

**Stop / remove:**

```bash
docker stop food-classifier-api
docker rm food-classifier-api
```

---

## 6. Tag

Tag the local image with the full registry path before pushing:

```bash
docker tag food-classifier \
  registry.digitalocean.com/aisg-registry/food-classifier:latest
```

For versioned releases (recommended alongside `latest`):

```bash
docker tag food-classifier \
  registry.digitalocean.com/aisg-registry/food-classifier:v1.0.0
```

---

## 7. Push

```bash
docker push registry.digitalocean.com/aisg-registry/food-classifier:latest

# also push the versioned tag if created
docker push registry.digitalocean.com/aisg-registry/food-classifier:v1.0.0
```

---

## 8. Deploy on a DigitalOcean Droplet

SSH into the droplet, then:

```bash
# 1. Authenticate Docker on the droplet
docker login registry.digitalocean.com/aisg-registry

# 2. Pull the image
docker pull registry.digitalocean.com/aisg-registry/food-classifier:latest

# 3. Upload your .env and weights to the droplet (from your local machine)
scp .env root@<droplet-ip>:~/food-classifier/
scp models/model.pth root@<droplet-ip>:~/food-classifier/models/

# 4. Run the container
docker run -d \
  --name food-classifier-api \
  --restart unless-stopped \
  --env-file ~/food-classifier/.env \
  -v ~/food-classifier/models:/app/models:ro \
  -p 8000:8000 \
  registry.digitalocean.com/aisg-registry/food-classifier:latest
```

---

## 9. Update a running deployment

```bash
# Pull the new image
docker pull registry.digitalocean.com/aisg-registry/food-classifier:latest

# Replace the running container
docker stop food-classifier-api && docker rm food-classifier-api

docker run -d \
  --name food-classifier-api \
  --restart unless-stopped \
  --env-file ~/food-classifier/.env \
  -v ~/food-classifier/models:/app/models:ro \
  -p 8000:8000 \
  registry.digitalocean.com/aisg-registry/food-classifier:latest
```

---

## 10. Full local-to-production cheatsheet

```bash
# Build
docker build --platform linux/amd64 -t food-classifier .

# Test locally
docker run -d --name food-classifier-api --env-file .env \
  -v ./models:/app/models:ro -p 8000:8000 food-classifier
curl http://localhost:8000/health

# Tag
docker tag food-classifier \
  registry.digitalocean.com/aisg-registry/food-classifier:latest

# Push
doctl registry login
docker push registry.digitalocean.com/aisg-registry/food-classifier:latest

# Deploy (on the droplet)
docker pull registry.digitalocean.com/aisg-registry/food-classifier:latest
docker stop food-classifier-api && docker rm food-classifier-api
docker run -d --name food-classifier-api --restart unless-stopped \
  --env-file ~/food-classifier/.env \
  -v ~/food-classifier/models:/app/models:ro -p 8000:8000 \
  registry.digitalocean.com/aisg-registry/food-classifier:latest
```
