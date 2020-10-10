import torch
import os
import torch.nn as nn
from torch.nn import functional as F
from PIL import Image
import pandas as pd
from config import PATH_CAT_ATTR_PREDICTOR
from utils import get_transform, expand, get_desc, plot_annos
from bbox import BBoxMaker

class FashionModel(nn.Module):
    """ 
    Class for the multi-task model for category and attribute 
    prediction. 
    
    Backbone: MobileNet v2
    
    Output heads: category, sleeve_length, neckline, upper_body_length,
                    lower_body_length, closure_type 
                    
    """
    
    def __init__(self, backbone, num_classes):
        super(FashionModel, self).__init__()
        self.backbone = backbone
        n_ftrs = 128

        # Heads
        self.cat = nn.Sequential(
            nn.Linear(n_ftrs, num_classes['cat'])
        )
        
        # self.clr = nn.Sequential(
        #     nn.Linear(n_ftrs, num_classes['clr'])
        # )

        self.slv = nn.Sequential(
            nn.Linear(n_ftrs, num_classes['slv'])
        )

        self.neck = nn.Sequential(
            nn.Linear(n_ftrs, num_classes['neck'])
        )

        self.ubl = nn.Sequential(
            nn.Linear(n_ftrs, num_classes['ubl'])
        )

        self.lbl = nn.Sequential(
            nn.Linear(n_ftrs, num_classes['lbl'])
        )

        self.clos = nn.Sequential(
            nn.Linear(n_ftrs, num_classes['clos'])
        )

    def forward(self, image):
        features = self.backbone(image)
        # heads
        cat = F.softmax(self.cat(features), dim=1)
        #clr = F.softmax(self.clr(features), dim=1)
        slv = F.softmax(self.slv(features), dim=1)
        neck = F.softmax(self.neck(features), dim=1)
        ubl = F.softmax(self.ubl(features), dim=1)
        lbl = F.softmax(self.lbl(features), dim=1)
        clos = F.softmax(self.clos(features), dim=1) 
        return [cat, slv, neck, ubl, lbl, clos]    


class CatAttrPredictor(object):
    """ 
    Class for predicting categories and attributes using FashionModel 
    
    """
    
    def __init__(self, device):
        self.device = device
        self.path = PATH_CAT_ATTR_PREDICTOR
        self.model = torch.load(self.path, map_location=device).to(device)
        self.model.eval()
        self.transform = get_transform(normalize=True)
        self.tasks = ['cat', 'slv', 'neck', 'ubl', 'lbl', 'clos']
        
    def get_labels(self, images, bboxes):
        """ 
        Method for assigning labels to bounding boxes in images 
    
        Arguments:
        ---
        images: list of PIL images
        bboxes: list of bounding boxes for images
        (bbox config: [x1, y1, x2, y2])

        Returns:
        ---
        label_list: list of labels assigned to bounding boxes in images
        prob_list: confidence values for labels assigned 
        
        """
        
        label_list = []
        prob_list = []
        for index, img in enumerate(images):
            boxes = bboxes[index]
            data = []
            for i in range(len(boxes)):
                im = img.resize([224,224], box= expand(boxes[i], img))
                data.append(self.transform(im))
            data = torch.stack(data).to(self.device)
            outputs = self.model(data)
            labels = [torch.max(op, 1)[1] for op in outputs]
            labels = {self.tasks[i]: label.cpu().numpy() for i, label in enumerate(labels)}
            probs = {}
            for idx, task in enumerate(self.tasks):
                task_probs = []
                for i in range(len(labels[task])):
                    p = outputs[idx][i][labels[task][i]].item()
                    task_probs.append(p)
                probs[task] = task_probs
            label_list.append(labels)
            prob_list.append(probs)
        
        return label_list, prob_list

# if __name__ == '__main__':
#     images = []
#     for fn in os.listdir('user_2'):
#         images.append(Image.open('user_2/' + fn))
#     images = [img.convert('RGB').resize([400, 600]) for img in images]
#     device = torch.device('cuda')
#     bbm = BBoxMaker(device)
#     bboxes, _ = bbm.get_boxes(images)
#     cap = CatAttrPredictor(device)
#     labels, probs = cap.get_labels(images, bboxes)
#     preference = []
#     for i, img in enumerate(images):
#         desc, conf = get_desc(bboxes[i], labels[i], probs[i])
#         preference.append(desc)
#         # b = [desc['full_body_bbox'], desc['lower_body_bbox'], desc['upper_body_bbox']]
#         # l = [desc['full_body'], desc['lower_body'], desc['outerwear']] if desc['outerwear'] != 'nan' else [desc['full_body'], desc['lower_body'], desc['upper_body']]
#         # # plot_annos(img, b, l)
#     preference = pd.DataFrame(preference)
