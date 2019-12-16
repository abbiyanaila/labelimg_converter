import xmltodict
import json
import pathlib
import os
import argparse
from typing import *
import copy

def word_or_char(val):
    lv = len(val)
    if lv > 1:
        return "word"
    else:
        return "char"

base_mockup = {
    'image': {
        'filename': "",
        'dim': {
            "width": 0,
            "height": 0,
            "channel": 0
        }
    },
    "object": []
}

object_mockup = {
    "class_type": "",
    "class_value": "",
    "coord_type": "",
    "coord_value": {
        "xmin": 0,
        "xmax": 0,
        "ymin": 0,
        "ymax": 0
    }
}


def open_xmlfile_to_dict(filepath):
    with open(filepath) as fd:
        doc: Dict = xmltodict.parse(fd.read())

    if "annotation" in doc.keys():
        xml_dict = doc['annotation']
        return xml_dict
    else:
        raise ValueError("XML file nggak punya annotation, ini bukan file labelimg!")


def save_to_file(jsonfile, content):
    with open(jsonfile, 'w+') as json_file:
        json.dump(content, json_file, indent=4)


def convert_xml_to_dict(xmldict):
    conv_json = copy.deepcopy(base_mockup)
    conv_json['image']['filename'] = xmldict['filename']
    conv_json['image']['dim']['width'] = int(xmldict['size']['width'])
    conv_json['image']['dim']['height'] = int(xmldict['size']['height'])
    conv_json['image']['dim']['channel'] = int(xmldict['size']['depth'])

    tlen = len(xmldict['object'])
    
    for obj in xmldict['object']:
        
        object_json = copy.deepcopy(object_mockup)
        object_json['class_type'] = word_or_char(obj['name'])
        object_json['class_value'] = obj['name']
        object_json['coord_type'] = 'bndbox'
        object_json['coord_value'] = obj['bndbox']
        # object_json['coord_value']['xmin'] = int(obj['bndbox']['xmin'])
        # object_json['coord_value']['ymin'] = int(obj['bndbox']['ymin'])
        # object_json['coord_value']['xmax'] = int(obj['bndbox']['xmax'])
        # object_json['coord_value']['ymax'] = int(obj['bndbox']['ymax'])
        conv_json['object'].append(object_json)
#     print(conv_json)
    return conv_json


def convert(xmlfile, jsonfile):
    print(f'Load file xml in path: {xmlfile}')
    xml_dict = open_xmlfile_to_dict(xmlfile)

    conv_json = convert_xml_to_dict(xml_dict)

    save_to_file(jsonfile, content=conv_json)
    print(f'Convert xml to json in path: {jsonfile}')


def convert_xml_to_json(path):
    base_path = pathlib.Path(path)
    list_files = base_path.glob('*.xml')

    for path_file in list(list_files):
        base_path = path_file.parent
        xml_file = path_file.name
        xml_filename = os.path.join(str(base_path), str(xml_file))

        json_file = path_file.stem + ".json"
        json_filename = os.path.join(str(base_path), str(json_file))

        convert(xml_filename, json_filename)

# path = '/home/abbiyanaila/Tigapilar/CRAFT bounding box/Testing/Dataset Class B/'
# convert_xml_to_json(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="converter xml to json")
    parser.add_argument('--path', type=str, help='choose path')
    args = parser.parse_args()
    args_path = args.path

    if args_path is not None:
        path = pathlib.Path(args_path)
        if path.exists():
            file = list(path.glob('*.xml'))
            if len(file)==0:
                raise FileNotFoundError("tidak ada file xml")
            else:
                convert_xml_to_json(args_path)
    else:
        raise ValueError("--path nggak boleh kosong! ingat di isi!")

