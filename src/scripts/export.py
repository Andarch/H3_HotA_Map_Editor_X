#!/usr/bin/env python3

import json

#################
## JSON EXPORT ##
#################

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('latin-1')
        return json.JSONEncoder.default(self, obj)

def export_to_json(map_data: dict, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(map_data, f, cls=CustomEncoder, indent=4)
