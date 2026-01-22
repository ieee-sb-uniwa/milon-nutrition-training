from fastapi import FastAPI , UploadFile,File,Request,HTTPException
from fastapi.responses import JSONResponse
import io 
from typing import List,Dict,Any
from PIL import Image 
from app.utils.valid_image import validation_image_upload
from app.model import Model
from pathlib import Path 
app = FastAPI(title="Food Classifier",description="Image Classifier for a variety of different foods")

BASE_DIR = Path(__file__).resolve().parent.parent
WEIGHTS_PATH = BASE_DIR / "src" / "models" / "artifacts" / "weights" / "transfood101.pth"


#load model
try:
    model = Model(
        model_path=str(WEIGHTS_PATH),
        class_names=None,
        target_size=(224,224),
        use_unsharp=False
    )
except Exception as e:
    raise RuntimeError(f" Failed to load model from {WEIGHTS_PATH}: {e}")

@app.get("/health")
def health():
    return {
        "status":"ok",
        "weight_path":str(WEIGHTS_PATH),
        "num_classes": len(model.class_names) if model.class_names else None 
    }

@app.post('/predict')
async def predict(image:UploadFile=File(...)):
    validation_image_upload(image)

    content = await image.read()
    if not content:
        raise HTTPException(status_code=400,detail="Empty Filed upload")
    
    try:
        pil_image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code =400,detail="Invalid image file (could not decode)")
    
    try:
        results = model.predict(pil_image)
        probs = results.get("probabilities",[])
        if not probs:
            raise HTTPException(status_code=500,detail="Prediction Failed")
        
        if model.class_names is not None and len(probs) != len(model.class_names):
            raise HTTPException(status_code=500,detail=f"Prediction failed: probs={len(probs)}")
        
        return {
            "predicted_index": results['predicted_index'],
            "predicted_label": results["predicted_label"],
            "confidence": results["confidence"]
        }
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))