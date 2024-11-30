import json
from ..common import *

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('latin-1')
        return json.JSONEncoder.default(self, obj)

def export_json(map_key: dict) -> bool:
    def main(map_key: dict) -> bool:
        filename = map_key['filename']
        if filename.endswith('.h3m'):
            filename = filename[:-4]
        if not filename.endswith('.json'):
            filename += '.json'

        #while True:
        type = get_export_type()
        if not type: return False
        match type:
            case 1: data = map_key
            case 2: data = map_key['terrain']
        
        xprint(type=Text.ACTION, text=f"Exporting JSON file...")

        with open(filename, 'w') as f:
            json.dump(data, f, cls = CustomEncoder, indent = 4)
        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def get_export_type() -> int:
        input = xprint(menu=Menu.JSON.value)
        if input == ESC: return False
        else: return int(input)

    return main(map_key)
