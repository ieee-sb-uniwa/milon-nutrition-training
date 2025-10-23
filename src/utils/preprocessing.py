import os 
import cv2
from typing import List , Dict
import shutil

def clean_category(category:str)-> str:
    return "_".join(category.strip().lower().split())


def get_categories(base_dir:str,categories:List[str])->Dict[str,List[str]]:
    if not isinstance(categories,List[str]):
        raise ValueError("The categories must be a list of strings")
    
    clean_category = [clean_category(cat) for cat in categories]
    valid_exts = [".jpg",".jpeg",".png",".bmp",".tiff"]
    result = {cat:[] for cat in clean_category}

    for cat in clean_category:
        dir_path = os.path.join(base_dir, cat)
        if not os.path.isdir(dir_path):
            continue

        for root, _, files in os.walk(dir_path):
            for fname in files:
                if fname.lower().endswith(valid_exts):
                    full_path = os.path.join(root, fname)
                    result[cat].append(full_path)

    return result , clean_category #returns the result of every image and the clean_categories inside the dict


#dataset creation
def create_dataset(result:Dict[str,List[str]],output_path:str) ->None:
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for category,img_paths in result.items():
        category_dir = os.path.join(output_path,category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        for img_path in img_paths:
            fname = os.path.basename(img_path)
            dest_path = os.path.join(category_dir,fname)
            if not os.path.exists(dest_path):
                shutil.copy2(img_path,dest_path)

#----- KAGGLE FUNCTIONS BELOW --------

def normalize_img(img,TARGET_SIZE=512,pad_color=0):
    h ,w = img.shape[:2]
    if w!= TARGET_SIZE:
        aspect_ratio = h/w
        new_h = int(TARGET_SIZE*aspect_ratio)
        img = cv2.resize(img,(TARGET_SIZE,new_h),interpolation=cv2.INTER_AREA)

        h,w = img.shape[:2]
    if h <TARGET_SIZE:
        img = pad_height(img,TARGET_SIZE,pad_color)
    elif h > TARGET_SIZE:
        img = crop_height(img)

    return img

    

def pad_height(img,TARGET_SIZE=512,pad_color=0):
    h,w = img.shape[:2]
    if h>= TARGET_SIZE:
        return img 
    padding_needed = TARGET_SIZE-h
    pad_top = padding_needed//2
    pad_bottom = padding_needed-pad_top

    return cv2.copyMakeBorder(img,pad_top,pad_bottom,0,0,cv2.BORDER_CONSTANT,value=(pad_color,pad_color,pad_color))

def crop_height(img,TARGET_SIZE=512):
    h,w = img.shape[:2]
    if h <= TARGET_SIZE:
        return img
    crop_amount = h-TARGET_SIZE
    crop_top = crop_amount//2
    crop_bottom = crop_top+TARGET_SIZE
    return img[crop_top:crop_bottom,:]

def laplacian_variance(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray,ddepth=cv2.CV_64F,ksize=3).var())

def unsharp_mask(img, ksize=(5,5), strength=1.5):
    blur = cv2.GaussianBlur(img, ksize, 0)
    sharp = cv2.addWeighted(img, 1 + strength, blur, -strength, 0)
    return sharp