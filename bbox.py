import torch
from config import PATH_BBOX_MAKER
from utils import get_transform

class BBoxMaker(object):
    """ 
    Class for identifying region of interests:
    (Top, Bottom, and Full Body) in outfit images. 
    
    """
    
    def __init__(self, device):
        self.device = device
        self.path = PATH_BBOX_MAKER
        self.model = torch.load(self.path, map_location=device).to(device)
        self.model.eval()
        self.transform = get_transform(normalize=False)
        
    def get_boxes(self, images):
        """ 
        Method for returning bounding boxes of the
        given list of images 
        
        Arguments
        ---
        images: list of PIL images 
        
        Returns 
        ---
        box_list: list of bounding boxes for images 
        (bbox config: [x1, y1, x2, y2])
        prob_list: confidence values for bounding boxes 
        
        """
        
        box_list = []
        prob_list = []
        for img in images:
            inp = [self.transform(img).to(self.device)]
            detections = self.model(inp)
            detections = [{k: v.detach().cpu().numpy() for k, v in t.items()} 
                            for t in detections]
            detections = detections[0]
            boxes = []
            probs = []
            if detections is not None:
                n_preds = len(detections['boxes'])
                for i in range(n_preds):
                    if(detections['scores'][i] >= 0.9):
                        x1 = detections['boxes'][i][0]
                        y1 = detections['boxes'][i][1]
                        x2 = detections['boxes'][i][2]
                        y2 = detections['boxes'][i][3]
                        boxes.append([x1, y1, x2, y2])
                        probs.append(detections['scores'][i])
            box_list.append(boxes)
            prob_list.append(probs)
        return box_list, prob_list

# if __name__ == "__main__":
#     images = []
#     for fn in os.listdir('user_2'):
#         images.append(Image.open('user_2/' + fn))
#     images = [img.convert('RGB').resize([400, 600]) for img in images]
#     device = torch.device('cuda')
#     bbm = BBoxMaker(device)
#     bboxes, probs = bbm.get_boxes(images)