import json
from ..common import *

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('latin-1')
        return json.JSONEncoder.default(self, obj)

def export_json(map_key: dict, filename: str) -> None:
    if filename.endswith('.h3m'):
        filename = filename[:-4]
    if not filename.endswith('.json'):
        filename += '.json'
    
    xprint(type=Text.ACTION, text=f"Exporting JSON file...")

    try:
        with open(filename, 'w') as f:
            json.dump(map_key, f, cls = CustomEncoder, indent = 4)
        xprint(type=Text.SPECIAL, text=DONE)
    except Exception as e:
        xprint(type=Text.ERROR, text=f"Failed to export JSON file: {e}")
        