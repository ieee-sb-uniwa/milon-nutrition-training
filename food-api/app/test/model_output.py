import numpy as np 
from app.model import Model

m = Model(model_path="/Users/Damian/milon-nutrition-training/src/models/artifacts/weights/transfood101.pth",class_names=None,target_size=(224,224))

x = np.random.rand(1,224,224,3).astype(np.float32)

prob = m._forward(x)
print("probabilities shape: ",prob.shape)
print("sum: ",prob[0].sum())