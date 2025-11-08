import os
import tensorflow as tf
import csv
import numpy as np
from pathlib import Path
import kagglehub
from PIL import Image
import matplotlib.pyplot as plt
from kagglehub import KaggleDatasetAdapter

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

path = Path(kagglehub.dataset_download("marquis03/fruits-100"))
filename_names = path / "classname.txt"
filename_train = path / "train.csv"
filename_test = path / "test.csv"
filename_vali = path / "val.csv"


# load data

def take_fruit_names(filename):
    fruit_names = {}
    fruit_id  = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            fruit_name = parts[0]
            fruit_names[fruit_id] = fruit_name
            fruit_id += 1            
    return fruit_names


def load_data_fruit_paths(path):
   image_paths = []
   with open(path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            image_paths.append(row[0])
   return image_paths

def load_data_fruit_category(path):
   image_category = []
   with open(path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            image_category.append(row[1])
   return image_category

def take_picture(image_path, image_size=(250, 250)):
    img = Image.open(image_path).convert('RGB')  # άνοιγμα σε RGB
    img = img.resize(image_size)  # αλλαγή μεγέθους
    return np.array(img)   
            
def pictures_to_0_1 (images):
    image = image.astype(np.float32)/255.0
    return image

def main():
    fruit_names = take_fruit_names(filename_names)
    train_image_paths = load_data_fruit_paths(filename_train)
    train_image_category = load_data_fruit_category(filename_train)

    test_image_paths = load_data_fruit_paths(filename_test)
    vali_image_paths = load_data_fruit_paths(filename_vali)
    vali_image_category = load_data_fruit_category(filename_vali)

    image_fruit_train_image  = []
    image_fruit_train_image_labels = []

    image_fruit_test_image  = []

    for img_path, id in zip(train_image_paths, train_image_category):
        id = int(id)  # βεβαιωνόμαστε ότι είναι int
        full_path = path / img_path  # img_path από το CSV
        img_array = take_picture(full_path)
        image_fruit_train_image.append(img_array)
        image_fruit_train_image_labels.append(id)

    for img_path in zip(image_fruit_test_image):
        full_path = path / img_path  # img_path από το CSV
        img_array = take_picture(full_path)
        image_fruit_test_image.append(img_array)
        
    image_fruit_train_image = np.array(image_fruit_train_image)
    image_fruit_train_image_labels = np.array(image_fruit_train_image_labels)
    image_fruit_test_image = np.array(image_fruit_test_image)



    # Σώζουμε τις εικόνες στον δίσκο
    np.save("fruit_train_images.npy", image_fruit_train_image)
    np.save("fruit_train_labels.npy", image_fruit_train_image_labels)
    np.save("fruit_train_images.npy", image_fruit_test_image)
    
 

    
if __name__=="__main__":
    main()
