from pipeline import Pipeline
import os
import torch
from PIL import Image
from cat_attr import FashionModel

# Change to 'cuda' for GPU and 'cpu' for CPU 
device = torch.device('cuda') 

if __name__=='__main__':
    occasion = 'Travel'
    gender = 'female'
    images = [Image.open('test_images/' + fn) for fn in os.listdir('test_images')]
    rec = Pipeline(device)
    print(rec.get_recommendation(gender, occasion, images))
    