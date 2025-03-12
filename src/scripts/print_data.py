import pprint
from ..common import *
from ..menus import *

def print_data(map_key: dict) -> bool:
    input = xprint(menu=Menu.INFO.value)
    if input == KB.ESC.value: return False
    draw_header()

    match input:
        case 1:
            data = pprint.pformat(map_key["general"], width=PRINT_WIDTH)
        case 2:
            data = pprint.pformat(map_key["player_specs"], width=PRINT_WIDTH)
        case 3:
            data = pprint.pformat(map_key["conditions"], width=PRINT_WIDTH)
        case 4:
            data = pprint.pformat(map_key["start_heroes"], width=PRINT_WIDTH)
        case 5:
            data = pprint.pformat(map_key["ban_flags"], width=PRINT_WIDTH)
        case 6:
            data = pprint.pformat(map_key["terrain"], width=PRINT_WIDTH)
        case 7:
            data = pprint.pformat(map_key["object_defs"], width=PRINT_WIDTH)
        case 8:
            data = pprint.pformat(map_key["object_data"], width=PRINT_WIDTH)
        case 9:
            data = pprint.pformat(map_key["events"], width=PRINT_WIDTH)
        case 0:
            data = pprint.pformat(map_key["null_bytes"], width=PRINT_WIDTH)

    xprint(type=Text.INFO, text=data)

    match input:
        case 2:
            data = pprint.pformat(map_key["teams"], width=PRINT_WIDTH)
            xprint(type=Text.INFO, text=data)
        case 4:
            data = pprint.pformat(map_key["hero_data"], width=PRINT_WIDTH)
            xprint(type=Text.INFO, text=data)
        case 9:
            data = pprint.pformat(map_key["rumors"], width=PRINT_WIDTH)
            xprint(type=Text.INFO, text=data)

    xprint()

    while True:
        if msvcrt.getwch():
            break

    return True
