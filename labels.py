categorical_labels = {
    'dress': 0,
    'jump_suit': 1,
    'shirt_blouse': 2,
    'sweater': 3,
    'sweatshirt_hoodies': 4,
    't_shirt': 5,
    'tank_top': 6,
    'top_others': 7,
    'athletic_pants': 8,
    'jeans': 9,
    'leggings': 10,
    'pants/trousers': 11,
    'shorts': 12,
    'skirt': 13,
    'blazer': 14,
    'coat': 15,
    'jacket': 16,
}

attribute_labels = {
    'colour': {
        'black': 0, 
        'blue': 1,
        'brown': 2, 
        'gold': 3, 
        'green': 4, 
        'grey': 5,
        'multi': 6, 
        'navy': 7, 
        'orange': 8, 
        'pink': 9, 
        'purple': 10, 
        'red': 11, 
        'silver': 12, 
        'white': 13,
        'yellow': 14
    },

    'sleeve_length': {
        'nan': 0,
        'long': 1, 
        'short': 2, 
        'sleeveless': 3, 
        'three_quarter': 4
    },

    'neckline': {
        'nan': 0,
        'collar': 1, 
        'halter_neck': 2, 
        'hooded': 3,  
        'off_shoulder': 4,
        'round_neck': 5, 
        'turtleneck': 6, 
        'v_neck': 7
    },

    'upper_body_length': {
        'nan': 0,
        'below_knee': 1, 
        'crop': 2, 
        'hip_length': 3, 
        'knee_length': 4, 
        'thigh_length': 5
    },

    'lower_body_length':{
        'nan': 0,
        'calf_length': 1, 
        'extra_short': 2, 
        'full_length': 3, 
        'knee_length': 4, 
        'thigh_length': 5
    },

    'closure_type': {
        'nan': 0, 
        'button': 1, 
        'pullover': 2, 
        'zip': 3
    }
}

cat_supercat = {
    'dress': 'full_body',
    'jump_suit': 'full_body',
    'play_suit': 'full_body',
    'shirt_blouse': 'upper_body',
    'sweater': 'upper_body',
    'sweatshirt_hoodies': 'upper_body',
    't_shirt': 'upper_body',
    'tank_top': 'upper_body',
    'top_others': 'upper_body',
    'athletic_pants': 'lower_body',
    'jeans': 'lower_body',
    'leggings': 'lower_body',
    'pants/trousers': 'lower_body',
    'shorts': 'lower_body',
    'skirt': 'lower_body',
    'skirt ': 'lower_body',
    'blazer': 'outer',
    'cardigan': 'outer',
    'coat': 'outer',
    'jacket': 'outer',
    'vest_waistcoat': 'outer',
}

common_categories = {
    'full_body': 'dress',
    'upper_body': 'shirt_blouse',
    'lower_body': 'pants/trousers',
    'outer': 'blazer'
}

def cat_to_id(label):
    return categorical_labels(label)

def id_to_cat(id):
    tmp = list(categorical_labels.keys())
    return tmp[id]

def cat_to_supercat(label):
    return cat_supercat[label]

def id_to_supercat(id):
    return cat_supercat[id_to_cat(id)]

def id_to_attr(id, attr_type):
    return list(attribute_labels[attr_type].keys())[id]

def attr_to_id(attr, attr_type):
    return attribute_labels[attr_type][attr]