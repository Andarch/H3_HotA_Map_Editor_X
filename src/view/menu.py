from ..common import (
    KB,
    draw_header,
    xprint,
)
from ..menus import Menu
from .format import format_data

# from . import terrain


def menu() -> None:
    while True:
        keypress = xprint(menu=Menu.VIEW.value)
        if keypress == KB.ESC.value:
            break

        draw_header()

        section_name = ""
        obj_filter = []

        match keypress:
            case 1:
                section_name = "map_specs"
            case 2:
                section_name = "player_specs"
            case 3:
                section_name = "starting_heroes"
            case 4:
                section_name = "rumors"
            case 5:
                section_name = "hero_data"
            case 6:
                xprint(text="Loading terrain data...")
                section_name = "terrain"
            case 7:
                xprint(text="Loading object defs...")
                section_name = "object_defs"
            case 8:
                xprint(text="Loading object data...")
                section_name = "object_data"
            case 9:
                section_name = "events"
            # case 0:
            #     terrain.list_unreachable_tiles()
            #     continue

        format_data(section_name, obj_filter)
