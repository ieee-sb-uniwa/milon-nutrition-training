from fastapi import FastAPI , UploadFile,File,Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from errors.handlers import http_404_handler,http_500_handler,http_403_handler
from utils.valid_image import validation_image_upload
app = FastAPI(title="Food Classifier",description="Image Classifier for a variety of different foods")
templates = Jinja2Templates(directory="templates")
FILE_TYPES = [".jpg",".jpeg",".png"]

@app.get('/',response_class=HTMLResponse)
@app.get("/home")
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

app.add_exception_handler(404,http_404_handler)
app.add_exception_handler(500,http_500_handler)
app.add_exception_handler(403,http_403_handler)

@app.post('/predict')
async def predict(image:UploadFile=File(...)):
    validation_image_upload(image)
    #TODO: call predict function from predict.pyx
    pass
    