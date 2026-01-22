from fastapi import UploadFile, HTTPException
FILE_TYPES = {".jpg",".jpeg",".png"}
 
def validation_image_upload(file:UploadFile):
    if file is None:
        raise HTTPException(status_code=400,detail="No file uploaded")

    filename = (file.filename or "").lower().strip()
    if not filename:
        raise HTTPException(status_code=400,detail="Uploaded file has no filename")
    
    #extension check
    dot = filename.rfind(".")
    ext = filename[dot:] if dot != -1 else ""
    if ext not in FILE_TYPES:
        raise HTTPException(status_code=415,detail=f"Unsupported file type {ext}. Allowed: {FILE_TYPES}")
    
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415,detail = f"Unsupproted content typeL {file.content_type}")