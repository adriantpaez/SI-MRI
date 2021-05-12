import json


def fix(json_file):
    data = {}
    new_data = {}
    with open(json_file) as jf:
        data = json.load(jf)
        for i, key in enumerate(data):
            new_data[f'{i + 1}'] = data[key]

        json.dump(new_data, open('new_database.json', 'x'))
    return data


fix('CRAN\CRAN.QRY.json')
