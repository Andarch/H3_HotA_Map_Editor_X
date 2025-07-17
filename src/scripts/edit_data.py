import pprint
from ..common import *
from ..menus import *
from src import scripts
from .edit import *

def edit_data(map_key: dict) -> bool:
    input = xprint(menu=Menu.EDIT.value)
    if input == KB.ESC.value: return False
    draw_header()

    success = False
    match input:
        case 1:
            success = scripts.modify_towns(map_key["object_data"])
        case 2:
            success = scripts.reset_heroes(map_key["player_specs"], map_key["start_heroes"]["custom_heroes"], map_key["hero_data"], map_key["object_data"])
        case 3:
            success = scripts.edit.list_unreachable_tiles(map_key["map_specs"], map_key["terrain"], map_key["object_defs"], map_key["object_data"])
        case 4:
            success = scripts.edit.set_random_monsters(map_key["object_data"])

    xprint()

    return success
