from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict , List , Optional, Tuple,Union
import numpy as np 
import cv2 
from PIL import Image
from src.utils.preprocessing import *
from app.utils.model_loader import load_vit_model

@dataclass
class Model:
    model_path:str
    class_names: Optional[List[str]] = None 
    target_size: Tuple[int,int]=(224,224)
    use_unsharp: bool = False
    unsharp_strength: float = 1.5

    def __post_init__(self)->None: 
        self.model = self._load_model(self.model_path)
        
        if self.class_names is not None and not isinstance(self.class_names, list):
            raise ValueError("class_names must be a list of strings or None")

    def preprocess(self,image:Union[str,Image.Image,np.ndarray])-> np.ndarray:
        img_bgr = self._to_bgr_(image)
        img_bgr = normalize_img(img_bgr,TARGET_SIZE=self.target_size)
        
        if self.use_unsharp:
            img_bgr = unsharp_mask(img_bgr,strength=self.unsharp_strength)
        
        img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
        x = img_rgb.astype(np.float32)/255.0
        x = np.expand_dims(x,axis=0)
        return x

    def _to_bgr_(self,image:Union[str,Image.Image,np.ndarray])->np.ndarray:
        if isinstance(image,str):
            img = cv2.imread(image)
            if img is None:
                raise ValueError(f"Image at path {image} could not be loaded.")
            return img 
        
        if isinstance(image,Image.Image):
            arr = np.array(image.convert("RGB"))
            return cv2.cvtColor(arr,cv2.COLOR_RGB2BGR)
        
        if isinstance(image,np.ndarray):
            if image.ndim ==2:
                return cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
            if image.shape[-1] == 4:
                return cv2.cvtColor(image,cv2.COLOR_BGRA2BGR)
            return image
        
        raise TypeError("Input image must be a file path, PIL Image, or numpy ndarray.")


    def predict(self,image:Union[str,Image.Image,np.ndarray])-> Dict[str,Any]:
        x = self.preprocess(image)
        
        if self.model is None:
            raise ValueError("Model is not loaded properly.")
        probs = self._forward(x)
        probs = np.asarray(probs,dtype=np.float32)
        pred_index = int(np.argmax(probs,axis=1)[0])
        confidenc = float(np.max(probs,axis=1)[0])
        pred_label =  None 
        if self.class_names is not None:
            pred_label = self.class_names[pred_index]
        
        return {
            "predicted_index":pred_index,
            "predicted_label":pred_label,
            "confidence":confidenc,
            "probabilities":probs[0].tolist()
        }

    def _load_model(self,model_path:Optional[str])->Any:
        model, classes = load_vit_model(self.model_path,num_classes=70)
        if model is None:
            raise ValueError("Failed to load model from the specified path.")
        if self.class_names is None and classes is not None:
            self.class_names = list(classes)
        return model
        


    def _forward(self,x:np.ndarray)-> np.ndarray:
        import torch 
        import torch.nn.functional as F
        
        xt = torch.from_numpy(x).permute(0,3,1,2)

        with torch.no_grad():
            logits = self.model(xt)
            probs = F.softmax(logits,dim=1)
        
        return probs.cpu().numpy().astype(np.float32)