from copy import deepcopy
import json
import data.objects as objects
from ..common import *
from ..menus import *

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

        type = get_export_type()
        if not type: return False
        match type:
            case 1: data = map_key
            case 2: data = get_hero_data(map_key)
            case 3: data = map_key['terrain']

        xprint(type=Text.ACTION, text=f"Exporting JSON file...")

        with open(filename, 'w') as f:
            json.dump(data, f, cls = CustomEncoder, indent = 4)
        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def get_export_type() -> int:
        input = xprint(menu=Menu.JSON.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    def get_hero_data(map_key: dict) -> dict:
        player_specs = deepcopy(map_key['player_specs'])
        player_specs[:] = [player for player in player_specs if len(player["available_heroes"]) > 0]
        for player in player_specs:
            del player["ai_behavior"]
            del player["alignments_customized"]
            del player["alignments_allowed"]
            del player["alignment_is_random"]
            del player["has_main_town"]
            if "generate_hero" in player:
                del player["generate_hero"]
            if "town_type" in player:
                del player["town_type"]
            if "town_coords" in player:
                del player["town_coords"]
            if "garbage_byte" in player:
                del player["garbage_byte"]
            if "placeholder_heroes" in player:
                del player["placeholder_heroes"]

        custom_heroes = deepcopy(map_key['start_heroes']['custom_heroes'])

        hero_data = deepcopy(map_key['hero_data'])
        hero_data[:] = [hero for hero in hero_data if len(hero) > 3]

        object_data = deepcopy(map_key['object_data'])
        object_data[:] = [obj for obj in object_data if obj["type"] in (objects.ID.Hero, objects.ID.Prison)]

        final_hero_data = {
            "player_specs": player_specs,
            "custom_heroes": custom_heroes,
            "hero_data": hero_data,
            "object_data": object_data
        }
        return final_hero_data

    return main(map_key)
