import json
import os
import string

from tqdm import tqdm


def translate_all(input_file):
    output_file = f'_{input_file}'
    output = {}
    with open(input_file) as f:
        data = json.load(f)
        for key in tqdm(data):
            item = {}
            item['id'] = key
            try:
                item['title'] = data[key]['title']
            except KeyError:
                item['title'] = ''
            try:
                item['author'] = data[key]['author']
            except KeyError:
                item['author'] = ''
            try:
                item['text'] = data[key]['abstract']
            except KeyError:
                item['text'] = ''
            output[key] = item
    out_f = open(output_file, "w+")
    json.dump(output, out_f, indent=2)


def translate_qry(input_file):
    output_file = f'_{input_file}'
    output = {}
    with open(input_file) as f:
        data = json.load(f)
        for key in data:
            _key = str(int(key))
            output[_key] = {
                'id': _key,
                'text': data[key]['text']
            }
    out_f = open(output_file, "w+")
    json.dump(output, out_f, indent=2)


translate_qry('CRAN.QRY.json')
