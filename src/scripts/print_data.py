import pprint

from ..common import (
    KB,
    MAX_PRINT_WIDTH,
    Text,
    draw_header,
    map_data,
    press_any_key,
    xprint,
)
from ..menus import Menu


def print_data() -> bool:
    global map_data

    user_input = xprint(menu=Menu.INFO.value)

    if user_input == KB.ESC.value:
        return False

    draw_header()

    match user_input:
        case 1:
            data = pprint.pformat(map_data["map_specs"], width=MAX_PRINT_WIDTH)
        case 2:
            data = pprint.pformat(map_data["player_specs"], width=MAX_PRINT_WIDTH)
        case 3:
            data = pprint.pformat(map_data["starting_heroes"], width=MAX_PRINT_WIDTH)
        case 4:
            data = pprint.pformat(map_data["rumors"], width=MAX_PRINT_WIDTH)
        case 5:
            data = pprint.pformat(map_data["hero_data"], width=MAX_PRINT_WIDTH)
        case 6:
            data = pprint.pformat(map_data["terrain"], width=MAX_PRINT_WIDTH)
        case 7:
            data = pprint.pformat(map_data["object_defs"], width=MAX_PRINT_WIDTH)
        case 8:
            data = pprint.pformat(map_data["object_data"], width=MAX_PRINT_WIDTH)
        case 9:
            data = pprint.pformat(map_data["events"], width=MAX_PRINT_WIDTH)

    xprint(type=Text.INFO, text=data)
    xprint()

    press_any_key()

    return True
