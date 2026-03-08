# Food Classifier API

FastAPI service that classifies food images using a Vision Transformer (ViT-B/16) trained on 101 food categories.

## Requirements

- Docker
- Model weights file `transfood101.pth` (~350 MB)

## Setup

### 1. Place the model weights

The container expects weights mounted at `/app/models/`. Place the weights file in the `weights/` directory:

```bash
mkdir -p weights
cp /path/to/transfood101.pth weights/
```

### 2. Configure environment variables

Copy the example env file and adjust values if needed:

```bash
cp .env.example .env
```

The defaults in `.env.example` work out of the box — only edit if you need a non-standard model path or port.

### 3. Build the image

Run from the `food-api/` directory:

```bash
docker build -t food-classifier .
```

### 4. Run the container

```bash
docker run -d \
  --name food-classifier-api \
  --env-file .env \
  -v ./models:/app/models:ro \
  -p 8000:8000 \
  food-classifier
```

The API will be available at `http://localhost:8000`.

#### Stop / remove the container

```bash
docker stop food-classifier-api
docker rm food-classifier-api
```

---

## Endpoints

| Method | Path       | Description                           |
| ------ | ---------- | ------------------------------------- |
| `GET`  | `/health`  | Liveness check — returns model status |
| `POST` | `/predict` | Classify a food image                 |

### `GET /health`

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "ok",
  "weight_path": "/app/models/transfood101.pth",
  "num_classes": 101
}
```

### `POST /predict`

Accepts a `multipart/form-data` upload with field name `image`. Supported formats: `.jpg`, `.jpeg`, `.png`.

```bash
curl -X POST http://localhost:8000/predict \
  -F "image=@/path/to/food.jpg"
```

```json
{
  "predicted_index": 47,
  "predicted_label": "pizza",
  "confidence": 0.934
}
```

---

## Testing locally (without Docker)

Run from the `food-api/` directory with your virtual environment active:

```bash
# CPU-only machine (avoids the ~3.5 GB CUDA torch wheel — same as the Docker image)
pip install -r requirements-cpu.txt

# GPU machine (full CUDA-enabled torch build)
# pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Set the model path via environment variable if it differs from the default:

```bash
MODEL_PATH=/path/to/transfood101.pth uvicorn app.main:app --reload
```

### Quick Python test

```python
from pathlib import Path
from PIL import Image
from app.model import Model

model = Model(
    model_path="weights/transfood101.pth",
    target_size=(224, 224),
)

img = Image.open("path/to/food.jpg")
result = model.predict(img)
print(result)
# {'predicted_index': 47, 'predicted_label': 'pizza', 'confidence': 0.934, 'probabilities': [...]}
```

### Interactive docs

Once the server is running, open `http://localhost:8000/docs` for the Swagger UI where you can upload images directly in the browser.

---

## Notes

- The model weight file is not tracked in git. Make sure it is in place under `weights/` before building or running the container.
