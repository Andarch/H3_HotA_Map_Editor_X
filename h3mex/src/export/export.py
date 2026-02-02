import json
import os

from src.common import Keypress, TextType, map_data
from src.defs import objects
from src.minimap import minimap
from src.ui import header
from src.ui.menus import Menu
from src.ui.xprint import xprint


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("latin-1")
        return json.JSONEncoder.default(self, obj)


###################################
OBJECT_FILTER = [*objects.ID]
# OBJECT_FILTER = [objects.ID.Town, objects.ID.Hero]
# OBJECT_SUBFILTER = [objects.SubID.HotADecor2.Glacier]
# OBJECT_COORDS_FILTER = [[53, 238, 1], [59, 238, 1], [63, 239, 1], [68, 239, 1], [72, 239, 1], [76, 239, 1]]
###################################


def menu() -> None:
    while True:
        keypress = xprint(menu=(Menu.EXPORT["name"], Menu.EXPORT["menus"][0]))
        if keypress == Keypress.ESC:
            return

        header.draw()

        match keypress:
            case "1":
                minimap.generate(minimap.MMAction.EXPORT, minimap.MMType.STANDARD, None)
            case "2":
                minimap.generate(minimap.MMAction.EXPORT, minimap.MMType.EXTENDED, None)
            case "3":
                while True:
                    keypress = xprint(menu=(Menu.EXPORT["name"], Menu.EXPORT["menus"][1]))
                    if keypress == Keypress.ESC:
                        break
                    match keypress:
                        case "1":
                            data = map_data["general"]
                        case "2":
                            data = map_data["player_specs"]
                        case "3":
                            data = map_data["starting_heroes"]
                        case "4":
                            data = map_data["ban_flags"]
                        case "5":
                            data = map_data["rumors"]
                        case "6":
                            data = map_data["hero_data"]
                        case "7":
                            data = map_data["terrain"]
                        case "8":
                            data = map_data["object_defs"]
                        case "9":
                            data = [
                                obj
                                for obj in map_data["object_data"]
                                if obj["id"] in OBJECT_FILTER
                                # if obj["id"] in OBJECT_FILTER and obj["sub_id"] in OBJECT_SUBFILTER
                                # if obj["id"] in OBJECT_FILTER and obj["coords"] in OBJECT_COORDS_FILTER
                            ]
                        case "0":
                            data = map_data["town_events"]
                        case "E":
                            data = map_data["global_events"]
                    filepath = "exports/json"
                    filename = os.path.join(filepath, map_data["filename"][:-4] + ".json")
                    xprint(type=TextType.ACTION, text="Exporting JSON file…", overwrite=14)
                    with open(filename, "w") as f:
                        json.dump(data, f, cls=CustomEncoder, indent=4)
                    xprint(type=TextType.DONE)

        # xprint()
