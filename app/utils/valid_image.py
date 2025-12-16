from fastapi import UploadFile, HTTPException
FILE_TYPES = [".jpg",".jpeg",".png"]

def validation_image_upload(file:UploadFile):
    if file is None:
        raise HTTPException(status_code=400,detail="No file uploaded")
    
    if file.endwith not in FILE_TYPES:
        raise HTTPException(status_code=400,detail="Missing Content")