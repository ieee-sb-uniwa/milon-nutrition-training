import torch 
import torch.nn as nn
from torchvision.models import vit_b_16

#without this it returns vit.class_token instead of class_token causing an error
def _strip_prefix(state_dict,prefix:str):
    if not prefix:
        return state_dict
    out = {}
    for k,v in state_dict.items():
        if k.startswith(prefix):
            out[k[len(prefix):]] = v
        else:
            out[k] = v
    return out

def load_vit_model(model_path:str,num_classes:int=101):
    model_path = str(model_path)
    ckpt = torch.load(model_path,map_location='cpu')

    if isinstance(ckpt,dict) and "state_dict" in ckpt:
        state_dict=  ckpt['state_dict']
        num_classes = int(ckpt.get('num_classes',num_classes))
        classes = ckpt.get('classes',None)
    else:
        state_dict = ckpt
        classes = None
    
    #handle wrapper prefixes
    for p in ("module.","model.","vit."):
        if any(k.startswith(p) for k in state_dict.keys()):
            state_dict = _strip_prefix(state_dict,p)

    #build model
    model = vit_b_16(weights=None,num_classes=num_classes)
    in_features = model.heads.head.in_features
    model.heads.head = nn.Linear(in_features,num_classes)
    model.load_state_dict(state_dict,strict=True)
    model.eval()

    return model,classes