import os 
import pickle 

"""
for saving the results for each dataset
"""

def ensure_cache_dirs(dataset_name):
    base_dir = os.path.join("cache",dataset_name)
    for split in ["train","test","valid"]:
        os.makedirs(os.path.join(base_dir,split),exist_ok=True)
    return base_dir

def get_cache_path(dataset_name,split,filename):
    ensure_cache_dirs(dataset_name=dataset_name)
    return  os.path.join("cache",dataset_name,split,f"{filename}.pkl")


def save_cache(data,dataset_name,split='train',file_path=None):
    if file_path is None:
        raise ValueError("YOu must provide a file name")
    
    file_path= get_cache_path(dataset_name=dataset_name,split=split,file_path=file_path)
    with open(file_path,'wb') as f:
        pickle.dump(data,f)


def load_cache(dataset_name,split,filename):
    file_path = get_cache_path(dataset_name,split,filename)
    if os.path.exists(file_path):
        with open(file_path,'rb') as f:
            return pickle.load(f)
    return None 