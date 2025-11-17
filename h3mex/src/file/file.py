import os
from gzip import open as gzopen
from typing import Tuple

from src.common import Keypress, TextType, map_data
from src.ui import header
from src.ui.xprint import xprint
from src.utilities import exit, is_file_writable

from . import (
    io,
    m1_general,
    m2_players,
    m3_conditions,
    m4_heroes,
    m5_additional_flags,
    m6_rumors_and_events,
    m7_terrain,
    m8_objects,
    m9_null,
)


def choose_map() -> Tuple[str, int]:
    header.draw()

    filenames = [f for f in sorted(os.listdir(), key=str.lower) if f.lower().endswith(".h3m") and os.path.isfile(f)]
    if not filenames:
        xprint(type=TextType.ERROR, text="No .h3m files found in the current directory.")
        exit()

    total_pages = (len(filenames) + 8) // 9
    pages = [filenames[i : i + 9] for i in range(0, len(filenames), 9)]

    esc_text = "Back" if map_data else "Exit"
    menus = []
    for page in pages:
        entries = [(str(i + 1), mapname) for i, mapname in enumerate(page)]
        if total_pages > 1:
            entries += [None, ("M", "Show more…"), None, None, ("ESC", esc_text)]
        else:
            entries += [None, None, ("ESC", esc_text)]
        menus.append(entries)

    h3m_menu = {"name": "LOAD MAP", "menus": menus}

    current_page = 0
    while True:
        keypress = xprint(menu=(h3m_menu["name"], h3m_menu["menus"][current_page]))
        if keypress == Keypress.ESC:
            return ""
        if keypress == "M" and total_pages > 1:
            current_page = (current_page + 1) % total_pages
            continue
        if keypress.isdigit():
            return filenames[current_page * 9 + (int(keypress) - 1)]


def load(filename: str = None) -> None:
    header.draw()

    xprint(text=f"Loading {filename}…")
    xprint()

    try:
        with gzopen(filename, "rb") as io.in_file:
            map_data["filename"] = filename

            xprint(text="Parsing 1/13: General…")
            map_data["general"] = m1_general.read_general()

            xprint(text="Parsing 2/13: Player Specs…", overwrite=1)
            map_data["player_specs"] = m2_players.read_players()

            xprint(text="Parsing 3/13: Victory/Loss Conditions…", overwrite=1)
            map_data["conditions"] = m3_conditions.parse_conditions()

            xprint(text="Parsing 4/13: Teams…", overwrite=1)
            map_data["teams"] = m2_players.parse_teams()

            xprint(text="Parsing 5/13: Hero Availability…", overwrite=1)
            map_data["starting_heroes"] = m4_heroes.parse_starting_heroes()

            xprint(text="Parsing 6/13: Additional Specs…", overwrite=1)
            map_data["ban_flags"] = m5_additional_flags.parse_flags()

            xprint(text="Parsing 7/13: Rumors…", overwrite=1)
            map_data["rumors"] = m6_rumors_and_events.parse_rumors()

            xprint(text="Parsing 8/13: Hero Templates…", overwrite=1)
            map_data["hero_data"] = m4_heroes.parse_hero_data()

            xprint(text="Parsing 9/13: Terrain Data…", overwrite=1)
            map_data["terrain"] = m7_terrain.parse_terrain(map_data["general"])

            xprint(text="Parsing 10/13: Object Defs…", overwrite=1)
            map_data["object_defs"] = m8_objects.parse_object_defs()

            xprint(text="Parsing 11/13: Object Data…", overwrite=1)
            map_data["object_data"] = m8_objects.parse_object_data(map_data["object_defs"], map_data["filename"])

            xprint(text="Parsing 12/13: Events…", overwrite=1)
            map_data["events"] = m6_rumors_and_events.parse_events()

            xprint(type=TextType.ACTION, text="Parsing 13/13: Null Bytes…", overwrite=1)
            map_data["null_bytes"] = m9_null.read_null()

            xprint(type=TextType.DONE)

    except FileNotFoundError:
        xprint(type=TextType.ERROR, text=f"Could not find {filename}.")


def save(filename: str = None) -> bool:
    global map_file

    header.draw()

    # Prompt for filename if not provided
    if filename is None:
        filename = xprint(type=TextType.PROMPT, text="Enter a new filename")
        if not filename:
            return False

    # Ensure the filename has the correct extension
    filename = filename if filename[-4:] == ".h3m" else filename + ".h3m"

    if not is_file_writable(filename):
        return False

    xprint(type=TextType.ACTION, text=f"Saving {filename}…")

    # Save the map data to the specified filename
    with gzopen(filename, "wb") as io.out_file:
        m1_general.write(map_data["general"])
        m2_players.write(map_data["player_specs"])
        m3_conditions.write_conditions(map_data["conditions"])
        m2_players.write_teams(map_data["teams"])
        m4_heroes.write_starting_heroes(map_data["starting_heroes"])
        m5_additional_flags.write_flags(map_data["ban_flags"])
        m6_rumors_and_events.write_rumors(map_data["rumors"])
        m4_heroes.write_hero_data(map_data["hero_data"])
        m7_terrain.write_terrain(map_data["terrain"])
        m8_objects.write_object_defs(map_data["object_defs"])
        m8_objects.write_object_data(map_data["object_data"])
        m6_rumors_and_events.write_events(map_data["events"])
        m9_null.write_null(map_data["null_bytes"])

    map_file = None

    xprint(type=TextType.DONE)

    return True
