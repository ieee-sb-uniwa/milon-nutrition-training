import torch

path = "src/models/artifacts/weights/transfood101.pth"

ckpt = torch.load(path, map_location="cpu", weights_only=False)
print("Loaded:", type(ckpt))

if isinstance(ckpt, dict):
    print("Keys:", ckpt.keys())
