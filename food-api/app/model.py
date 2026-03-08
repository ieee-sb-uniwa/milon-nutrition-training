from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageFilter

from app.utils.model_loader import load_vit_model


def _letterbox(
    image: Image.Image, target_size: Tuple[int, int], pad_color: int = 0
) -> Image.Image:
    """Resize image to fit within target_size while preserving aspect ratio, padding with pad_color."""
    target_w, target_h = target_size
    w, h = image.size
    if w == 0 or h == 0:
        raise ValueError("Empty image received in _letterbox")

    scale = min(target_w / w, target_h / h)
    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    resized = image.resize((new_w, new_h), Image.LANCZOS)

    padded = Image.new("RGB", (target_w, target_h), (pad_color, pad_color, pad_color))
    left = (target_w - new_w) // 2
    top = (target_h - new_h) // 2
    padded.paste(resized, (left, top))
    return padded


def _unsharp_mask(image: Image.Image, strength: float = 1.5) -> Image.Image:
    """Apply unsharp mask using PIL. strength maps roughly to the 'percent' parameter."""
    percent = int(strength * 100)
    return image.filter(ImageFilter.UnsharpMask(radius=2, percent=percent, threshold=3))


@dataclass
class Model:
    model_path: str
    class_names: Optional[List[str]] = None
    target_size: Tuple[int, int] = (224, 224)
    use_unsharp: bool = False
    unsharp_strength: float = 1.5

    def __post_init__(self) -> None:
        self.model = self._load_model(self.model_path)

        if self.class_names is not None and not isinstance(self.class_names, list):
            raise ValueError("class_names must be a list of strings or None")

    def _to_pil(self, image: Union[str, Image.Image, np.ndarray]) -> Image.Image:
        """Convert any supported input type to a PIL Image in RGB."""
        if isinstance(image, str):
            img = Image.open(image).convert("RGB")
            return img

        if isinstance(image, Image.Image):
            return image.convert("RGB")

        if isinstance(image, np.ndarray):
            if image.ndim == 2:
                # Grayscale
                return Image.fromarray(image, mode="L").convert("RGB")
            if image.shape[-1] == 4:
                # RGBA
                return Image.fromarray(image, mode="RGBA").convert("RGB")
            # BGR numpy array (e.g. from cv2) — flip channels
            if image.dtype != np.uint8:
                image = np.clip(image, 0, 255).astype(np.uint8)
            return Image.fromarray(image[..., ::-1], mode="RGB")

        raise TypeError("Input image must be a file path, PIL Image, or numpy ndarray.")

    def preprocess(self, image: Union[str, Image.Image, np.ndarray]) -> np.ndarray:
        img = self._to_pil(image)
        img = _letterbox(img, self.target_size)

        if self.use_unsharp:
            img = _unsharp_mask(img, strength=self.unsharp_strength)

        x = np.array(img, dtype=np.float32) / 255.0  # (H, W, 3)
        x = np.expand_dims(x, axis=0)  # (1, H, W, 3)
        return x

    def predict(self, image: Union[str, Image.Image, np.ndarray]) -> Dict[str, Any]:
        x = self.preprocess(image)

        if self.model is None:
            raise ValueError("Model is not loaded properly.")
        probs = self._forward(x)
        probs = np.asarray(probs, dtype=np.float32)
        pred_index = int(np.argmax(probs, axis=1)[0])
        confidence = float(np.max(probs, axis=1)[0])
        pred_label = None
        if self.class_names is not None:
            pred_label = self.class_names[pred_index]

        return {
            "predicted_index": pred_index,
            "predicted_label": pred_label,
            "confidence": confidence,
            "probabilities": probs[0].tolist(),
        }

    def _load_model(self, model_path: Optional[str]) -> Any:
        model, classes = load_vit_model(self.model_path, num_classes=70)
        if model is None:
            raise ValueError("Failed to load model from the specified path.")
        if self.class_names is None and classes is not None:
            self.class_names = list(classes)
        return model

    def _forward(self, x: np.ndarray) -> np.ndarray:
        import torch
        import torch.nn.functional as F

        xt = torch.from_numpy(x).permute(0, 3, 1, 2)  # (1, 3, H, W)

        with torch.no_grad():
            logits = self.model(xt)
            probs = F.softmax(logits, dim=1)

        return probs.cpu().numpy().astype(np.float32)
