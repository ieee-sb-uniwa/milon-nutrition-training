import cv2
from app.model import Model 
from pathlib import Path 
root = Path(__file__).resolve().parent.parent.parent
WEIGHTS_PATH = root / "src" / "models" / "artifacts" / "weights" / "transfood101.pth"
IMG_PATH = root/"app"/"test"/"test_image"/"macaron.jpeg"
m = Model(model_path=str(WEIGHTS_PATH),class_names=None,target_size=(224,224))

img = cv2.imread(str(IMG_PATH),cv2.IMREAD_COLOR)
x = m.preprocess(img)
print("preprocessed shape: ",x.shape)

results = m.predict(img)
print(results)