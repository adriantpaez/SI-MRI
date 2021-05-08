import json


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
