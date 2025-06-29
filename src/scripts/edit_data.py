import pprint
from ..common import *
from ..menus import *
from src import scripts

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
            xprint(type=Text.ERROR, text="Not yet functional.")
        case 4:
            xprint(type=Text.ERROR, text="Not yet functional.")

    xprint()

    return success
