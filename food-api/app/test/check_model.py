from pathlib import Path
import torch
 
p =  Path(__file__).resolve().parent.parent.parent
WEIGHTS_PATH = p / "src" / "models" / "artifacts" / "weights" / "transfood101.pth"

print("Path: ",WEIGHTS_PATH)
print("Exists: ",WEIGHTS_PATH.exists())

ckpt = torch.load(WEIGHTS_PATH,map_location='cpu')
print("TYPE: ",type(ckpt))

if isinstance(ckpt,dict):
    print("Keys: ",ckpt.keys())