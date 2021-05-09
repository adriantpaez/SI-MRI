import json
import string


def parse_docs(json_file):
    data = {}
    with open(json_file) as jf:
        data = json.load(jf)
        for key in data:
            text = ''
            for metadata in data[key]:
                text += data[key][metadata] + '\n'
            data[key] = text
    return data

def parse_queries(json_file):
    data={}
    with open(json_file) as jf:
        data=json.load(jf)
        for key in data:
            text=data[key]['text']
            text=text.translate(str.maketrans('', '', string.punctuation))
            data[key]=text.split(' ')
    return data


def parse_rel(json_file):
    data={}
    with open(json_file) as jf:
        data=json.load(jf)
        for key in data:
            data[key]=[k for k in data[key]]
    return data

