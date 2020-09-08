import json


def get_keys(filename):
    with open(filename, 'r') as fin:
        keys = json.load(fin)

    return keys
