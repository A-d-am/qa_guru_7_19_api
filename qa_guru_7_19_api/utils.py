import json
import os

CURRENT_FILE_PATH = os.path.abspath(__file__)
ROOT_PATH = os.path.dirname(CURRENT_FILE_PATH)
JSON_DIR = os.path.join(ROOT_PATH, 'json_schemas')


def load_schema(api_name, method_schema):
    path = os.path.join(JSON_DIR, api_name, method_schema)
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
