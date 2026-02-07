import src.view.special as special
from src.common import Cursor, Keypress, TextType, map_data
from src.defs import objects
from src.minimap import minimap
from src.ui import header
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress

from .format import format_map_data

###################################
# OBJECT_FILTER = [*objects.ID]
OBJECT_FILTER = [objects.ID.Tavern]
# OBJECT_SUBFILTER = [objects.SubID.HotADecor2.Glacier]
# OBJECT_COORDS_FILTER = [[53, 238, 1], [59, 238, 1], [63, 239, 1], [68, 239, 1], [72, 239, 1], [76, 239, 1]]
###################################


def menu() -> None:
    while True:
        keypress = xprint(menu=(Menu.VIEW["name"], Menu.VIEW["menus"][0]))
        if keypress == Keypress.ESC:
            return

        header.draw()

        match keypress:
            case "1":
                data = format_map_data(("general", map_data["general"]))
                _print_lines(data)
            case "2":
                data = format_map_data(("player_specs", map_data["player_specs"]))
                _print_lines(data)
            case "3":
                data = format_map_data(("starting_heroes", map_data["starting_heroes"]))
                _print_lines(data)
            case "4":
                data = format_map_data(("ban_flags", map_data["ban_flags"]))
                _print_lines(data)
            case "5":
                data = format_map_data(("rumors", map_data["rumors"]))
                _print_lines(data)
            case "6":
                data = format_map_data(("hero_data", map_data["hero_data"]))
                _print_lines(data)
            case "7":
                xprint(text="Loading terrain data…")
                data = format_map_data(("terrain", map_data["terrain"]))
                _print_lines(data)
            case "8":
                xprint(text="Loading object defs…")
                data = format_map_data(("object_defs", map_data["object_defs"]))
                _print_lines(data)
            case "9":
                xprint(text="Loading object data…")
                object_data = [
                    obj
                    for obj in map_data["object_data"]
                    if obj["id"] in OBJECT_FILTER
                    # if obj["id"] in OBJECT_FILTER and obj["sub_id"] in OBJECT_SUBFILTER
                    # if obj["id"] in OBJECT_FILTER and obj["coords"] in OBJECT_COORDS_FILTER
                ]
                data = format_map_data(("object_data", object_data))
                _print_lines(data)
            case "0":
                data = format_map_data(("town_events", map_data["town_events"]))
                _print_lines(data)
            case "E":
                data = format_map_data(("global_events", map_data["global_events"]))
                _print_lines(data)
            case "M":
                minimap.view()
            case "S":
                while True:
                    keypress = xprint(menu=(Menu.VIEW["name"], Menu.VIEW["menus"][1]))
                    if keypress == Keypress.ESC:
                        break
                    match keypress:
                        case "1":
                            data = special.list_unreachable_tiles()
                        case "2":
                            data = special.list_invalid_zone_objects()
                    _print_lines(data) if data else wait_for_keypress()


def _print_lines(lines: list) -> None:
    lines_printed = 0
    for line in lines:
        xprint(type=TextType.INFO, text=line)
        lines_printed += 1
        if lines_printed % 100 == 0:
            keypress = wait_for_keypress(suffix=" to continue printing")
            if keypress == Keypress.ESC:
                return
            for _ in range(3):
                print(Cursor.RESET_PREVIOUS, end="")
        if lines_printed == len(lines):
            wait_for_keypress()
