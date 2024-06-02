import json

from ..common import *

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('latin-1')
        return json.JSONEncoder.default(self, obj)

def export_json(map_key: dict, filename: str) -> None:
    print_action("Exporting JSON file...")

    with open(filename, 'w') as f:
        json.dump(map_key, f, cls=CustomEncoder, indent=4)

    print_done()
