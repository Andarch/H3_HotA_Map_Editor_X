import json
import os
from copy import deepcopy

from core.h3m import objects
from src.common import DONE, MsgType, map_data, xprint


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("latin-1")
        return json.JSONEncoder.default(self, obj)


def export(keypress: str) -> None:
    def main() -> None:
        filepath = "....maps/exports/JSON/"
        filename = os.path.join(filepath, map_data["filename"][:-4] + ".json")

        match keypress:
            case "1":
                data = map_data
            case "2":
                data = get_hero_data()
            case "3":
                data = map_data["terrain"]
            case "4":
                obj_filter = [objects.ID.Town, objects.ID.Random_Town]
                data = [obj for obj in map_data["object_data"] if obj["id"] in obj_filter]

        xprint(type=MsgType.ACTION, text="Exporting JSON file…")

        with open(filename, "w") as f:
            json.dump(data, f, cls=CustomEncoder, indent=4)

        xprint(type=MsgType.SPECIAL, text=DONE)

    def get_hero_data() -> dict:
        player_specs = deepcopy(map_data["player_specs"])
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

        custom_heroes = deepcopy(map_data["starting_heroes"]["custom_heroes"])

        hero_data = deepcopy(map_data["hero_data"])
        hero_data[:] = [hero for hero in hero_data if len(hero) > 3]

        object_data = deepcopy(map_data["object_data"])
        object_data[:] = [obj for obj in object_data if obj["id"] in (objects.ID.Hero, objects.ID.Prison)]

        final_hero_data = {
            "player_specs": player_specs,
            "custom_heroes": custom_heroes,
            "hero_data": hero_data,
            "object_data": object_data,
        }

        return final_hero_data

    main()
