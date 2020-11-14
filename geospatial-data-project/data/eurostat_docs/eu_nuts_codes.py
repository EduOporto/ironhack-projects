import json
import os

def name_ref(nuts_type):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+'/'+f'nuts{nuts_type}.json') as f:
        name_ref_dict = json.load(f)

    dict_turned = {y:x for x,y in name_ref_dict['dimension']['geo']['category']['label'].items()}
    
    return dict_turned