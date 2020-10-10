from bbox import BBoxMaker
from cat_attr import CatAttrPredictor, FashionModel
from retrieval import retrieval
from utils import *
from config import PATH_DATASET
import pickle
import numpy as np
import pandas as pd

class Pipeline(object):
    """ 
    Class for containing the complete pipeline:
    bbox detection --> cat and attr prediction --> retrieval 
    
    """
    
    def __init__(self, device):
        self.device = device
        self.dataset = pickle.load(open(PATH_DATASET, 'rb'))
        self.bbm = BBoxMaker(device)
        self.cap = CatAttrPredictor(device)
        
    def get_recommendation(self, gender, occasion, images=None):
        """ 
        Method for generating recommndations for a query
        query = (gender, occasion, images)
        
        Arguments:
        ---
        gender: 'male' or 'female' 
        occasion: occasion string
        images: (optional) set of images for preference modelling 
        
        Returns:
        ---
        results: list of retrieved image IDs 
        
        """
  
        self.gender = gender
        self.occasion = occasion
        preference = None
        if images != None:
            images = preprocess(images)
            bboxes, _ = self.bbm.get_boxes(images)
            labels, probs = self.cap.get_labels(images, bboxes)
            preference = []
            for i, img in enumerate(images):
                desc, conf = get_desc(bboxes[i], labels[i], probs[i])
                preference.append(desc)
            preference = pd.DataFrame(preference)
            preference = preference.drop(columns=["colour_bottom","colour_top","full_body_bbox","upper_body_bbox","lower_body_bbox"])
            preference = np.array(preference)
        results = retrieval(self.dataset, occasion, gender, recom_num=10, pref_matrix=preference)

        return results