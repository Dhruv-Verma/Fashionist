import numpy as np
import torchvision.transforms as T
from labels import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def preprocess(images):
    images = [img.convert('RGB').resize([400, 600]) for img in images]
    return images

def get_transform(normalize = False):
    custom_transforms = []
    custom_transforms.append(T.ToTensor())
    if normalize:
        custom_transforms.append(T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]))
    return T.Compose(custom_transforms)

def expand(bbox, img):
    bbox = np.array(bbox, dtype=float)
    height, width, _ = np.array(img).shape
    if str(bbox) == 'nan':
        return None
    m = min(height,width)/30
    x1, y1, x2, y2 = bbox
    bbox = [max(0, x1-m), max(0, y1-m), min(width, x2+m), min(height, y2+m)]
    return bbox

def is_complete_overlap(box1, box2):
    # box1 > box2
    check_x = box1[0] <= box2[0] and box1[2] >= box2[2]
    check_y = box1[1] <= box2[1] and box1[3] >= box2[3]
    return check_x and check_y

def is_valid_overlap(box1, box2):
    # box1 > box2
    check_1 = box1[0] <= box2[0] and box1[2] >= box2[2]
    check_2 = box1[0] >= box2[0] and box1[2] <= box2[2]
    check_3 = max(box1[1], box2[1]) <= min(box1[3], box2[3]) # condition of y overlap
    return (check_1 or check_2) and check_3

def get_valid_top_bottom(box1, box2, label1, label2):
    suplabel1, suplabel2 = cat_to_supercat(label1), cat_to_supercat(label2) 
    if( box1[1] < box2[1] ):
        if suplabel1 != 'upper_body' and suplabel1 != 'outer':
            label1 = common_categories['upper_body']
        if suplabel2 != 'lower_body':
            label2 = common_categories['lower_body'] 
        return (box1, box2, label1, label2)

    else:
        if suplabel2 != 'upper_body' and suplabel2 != 'outer':
            label2 = common_categories['upper_body']
        if suplabel1 != 'lower_body':
            label1 = common_categories['lower_body']    
        return (box2, box1, label2, label1) 

def get_desc(boxes, labels, probs):
    labels_sup = [id_to_supercat(l) for l in labels['cat']]
    desc = init_desc()

    if(len(boxes)==1):
        if(labels_sup[0] == 'full_body'):   
            lbls = {k: labels[k][0] for k in labels.keys()}
            desc = init_desc(desc, boxes[0], lbls, 'full_body')
            conf = {k: [probs[k][0]] for k in probs.keys()}
        return desc, conf    
        
    areas = []
    for box in boxes:
        w = box[2] - box[0]
        h = box[3] - box[1]
        areas.append(w * h)
    areas = np.array(areas)
    top_areas = np.argsort(-areas)

    box1_i = 0
    box1 = boxes[top_areas[box1_i]]
    i = 1
    box2_i = i 
    box2 = boxes[top_areas[i]]
    while(is_complete_overlap(box1, box2) and i < len(boxes)):
        box2_i = i 
        box2 = boxes[top_areas[box2_i]]
        i+=1
        
    if(labels_sup[top_areas[box1_i]] == 'full_body'):
        if(is_valid_overlap(box1, box2)):
            x1 = min(box1[0], box2[0])
            x2 = max(box1[2], box2[2])
            y1 = min(box1[1], box2[1])
            y2 = max(box1[3], box2[3])
            long_box = [x1, y1, x2, y2]
        else:
            long_box = box1
        lbls = {k: labels[k][top_areas[box1_i]] for k in labels.keys()}
        desc = init_desc(desc, long_box, lbls, 'full_body')
        conf = {k: [probs[k][top_areas[box1_i]]] for k in probs.keys()}
        # return desc
        
    else:   
        conf = {k: [0, 0] for k in probs.keys()}
        for a, idx in enumerate([top_areas[box1_i], top_areas[box2_i]]):
            supercat = labels_sup[idx]
            lbls = {k: labels[k][idx] for k in labels.keys()}
            desc = init_desc(desc, boxes[idx], lbls, supercat)
            for k in probs.keys():
                if supercat == 'lower_body':
                    conf[k][1] = probs[k][idx]
                else:
                    conf[k][0] = probs[k][idx]
    return desc, conf

def init_desc(desc=None, bbox=None, labels=None, supercat=None):
    if desc == None:
        desc = {
            'full_body': 'nan',
            'lower_body': 'nan',
            'upper_body': 'nan',
            'outerwear': 'nan',
            'colour_bottom': 'nan',
            'colour_top': 'nan',
            'neckline': 'nan',
            'upper_body_length': 'nan',
            'lower_body_length': 'nan',
            'closure_type': 'nan',
            'sleeve_length': 'nan',
            'full_body_bbox': 'nan',
            'lower_body_bbox': 'nan',
            'upper_body_bbox': 'nan'
        }
    if supercat == 'full_body':
        desc['full_body'] = id_to_cat(labels['cat'])
        desc['neckline'] = id_to_attr(labels['neck'], 'neckline')
        desc['upper_body_length'] = id_to_attr(labels['ubl'], 'upper_body_length')
        desc['closure_type'] = id_to_attr(labels['clos'], 'closure_type')
        desc['sleeve_length'] = id_to_attr(labels['slv'], 'sleeve_length')
        desc['full_body_bbox'] = bbox

    elif supercat == 'lower_body':
        desc['lower_body'] = id_to_cat(labels['cat'])
        desc['lower_body_length'] = id_to_attr(labels['lbl'], 'lower_body_length')
        desc['lower_body_bbox'] = bbox

    elif supercat == 'upper_body':
        desc['upper_body'] = id_to_cat(labels['cat'])
        desc['neckline'] = id_to_attr(labels['neck'], 'neckline')
        desc['upper_body_length'] = id_to_attr(labels['ubl'], 'upper_body_length')
        desc['closure_type'] = id_to_attr(labels['clos'], 'closure_type')
        desc['sleeve_length'] = id_to_attr(labels['slv'], 'sleeve_length')
        desc['upper_body_bbox'] = bbox

    elif supercat == 'outer':
        desc['outerwear'] = id_to_cat(labels['cat'])
        desc['neckline'] = id_to_attr(labels['neck'], 'neckline')
        desc['upper_body_length'] = id_to_attr(labels['ubl'], 'upper_body_length')
        desc['closure_type'] = id_to_attr(labels['clos'], 'closure_type')
        desc['sleeve_length'] = id_to_attr(labels['slv'], 'sleeve_length')
        desc['upper_body_bbox'] = bbox

    return desc

def plot_annos(img, boxes, labels=None):
    cmap = plt.get_cmap("rainbow")
    plt.figure()
    fig, ax = plt.subplots(1, figsize=(10,8))
    ax.imshow(img)
    colors = [cmap(i) for i in np.linspace(0, 1, 20)]
    i=0
    for box in boxes:
        if str(box) != 'nan':
            x1 = box[0]
            y1 = box[1]
            x2 = box[2]
            y2 = box[3]
            color = colors[random.randint(0,19)]
            bbox = patches.Rectangle((x1, y1), x2-x1, y2-y1,
                linewidth=2, edgecolor=color, facecolor='none')
            ax.add_patch(bbox)
            if(labels != None):
                plt.text(x1, y1, s=labels[i], 
                        color='black', verticalalignment='top',
                        bbox={'color': color, 'pad': 0})
        i+=1
    plt.axis('off')
    # save image
    # plt.savefig(img_path.replace(".jpg", "-det.jpg"),        
    #                   bbox_inches='tight', pad_inches=0.0)
    plt.show()