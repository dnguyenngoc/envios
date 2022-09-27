import json
import os

def save_file(path, data):
    data = json.dumps(data)
    with open(path, "w") as outfile:
        outfile.write(data)
        

def is_exists(path):
    return os.path.exists(path)


def load_file(path):
    data = json.loads(open(path, 'rb').read())
    return data
