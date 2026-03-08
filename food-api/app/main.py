import io
import os
from pathlib import Path
from typing import List, Dict, Any

from PIL import Image
from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.utils.valid_image import validate_image_upload
from app.model import Model

app = FastAPI(
    title="Food Classifier",
    description="Image Classifier for a variety of different foods",
)

# Configuration from environment variables
BASE_DIR = os.getenv("BASE_DIR", "/app")
MODEL_PATH = os.getenv("MODEL_PATH", f"{BASE_DIR}/models/transfood101.pth")
WEIGHTS_PATH = Path(MODEL_PATH)


# load model
try:
    model = Model(
        model_path=str(WEIGHTS_PATH),
        class_names=None,
        target_size=(224, 224),
        use_unsharp=False,
    )
except Exception as e:
    raise RuntimeError(f" Failed to load model from {WEIGHTS_PATH}: {e}")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "weight_path": str(WEIGHTS_PATH),
        "num_classes": len(model.class_names) if model.class_names else None,
    }


@app.post("/predict")
async def predict(image: UploadFile = Depends(validate_image_upload)):
    content = await image.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file upload")

    try:
        pil_image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400, detail="Invalid image file (could not decode)"
        )

    results = model.predict(pil_image)
    probs = results.get("probabilities", [])
    if not probs:
        raise HTTPException(status_code=500, detail="Prediction failed")

    if model.class_names is not None and len(probs) != len(model.class_names):
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: probs={len(probs)}"
        )

    top5 = sorted(
        enumerate(probs),
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    return {
        "top5": [
            {
                "index": idx,
                "label": model.class_names[idx] if model.class_names else None,
                "confidence": float(prob),
            }
            for idx, prob in top5
        ]
    }
