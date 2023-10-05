import json
import os


def load_schema(method_schema):
    path = os.path.join('json_schemas', method_schema)
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
