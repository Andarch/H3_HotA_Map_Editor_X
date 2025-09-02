from gzip import open as gzopen

from src.common import map_data

from ..common import (
    DONE,
    MsgType,
    draw_header,
    is_file_writable,
    xprint,
)
from . import (
    h1_general,
    h2_players,
    h3_conditions,
    h4_heroes,
    h5_additional_flags,
    h6_rumors_and_events,
    h7_terrain,
    h8_objects,
    h9_null,
    io,
)


def load(filename: str = None) -> None:
    draw_header()

    # Prompt for filename if not provided
    if filename is None:
        filename = xprint(type=MsgType.PROMPT, text="Enter the map filename to load")
        if not filename:
            return False

    # Ensure the filename has the correct extension
    filename = filename if filename[-4:] == ".h3m" else filename + ".h3m"

    xprint(type=MsgType.NORMAL, text=f"Loading {filename}…\n")

    try:
        with gzopen(filename, "rb") as io.in_file:
            map_data["filename"] = filename

            xprint(text="Parsing 1/13: General…", overwrite=1)
            map_data["general"] = h1_general.read_general()

            xprint(text="Parsing 2/13: Player Specs…", overwrite=1)
            map_data["player_specs"] = h2_players.read_players()

            xprint(text="Parsing 3/13: Victory/Loss Conditions…", overwrite=1)
            map_data["conditions"] = h3_conditions.parse_conditions()

            xprint(text="Parsing 4/13: Teams…", overwrite=1)
            map_data["teams"] = h2_players.parse_teams()

            xprint(text="Parsing 5/13: Hero Availability…", overwrite=1)
            map_data["starting_heroes"] = h4_heroes.parse_starting_heroes()

            xprint(text="Parsing 6/13: Additional Specs…", overwrite=1)
            map_data["ban_flags"] = h5_additional_flags.parse_flags()

            xprint(text="Parsing 7/13: Rumors…", overwrite=1)
            map_data["rumors"] = h6_rumors_and_events.parse_rumors()

            xprint(text="Parsing 8/13: Hero Templates…", overwrite=1)
            map_data["hero_data"] = h4_heroes.parse_hero_data()

            xprint(text="Parsing 9/13: Terrain Data…", overwrite=1)
            map_data["terrain"] = h7_terrain.parse_terrain(map_data["general"])

            xprint(text="Parsing 10/13: Object Defs…", overwrite=1)
            map_data["object_defs"] = h8_objects.parse_object_defs()

            xprint(text="Parsing 11/13: Object Data…", overwrite=1)
            map_data["object_data"] = h8_objects.parse_object_data(map_data["object_defs"], map_data["filename"])

            xprint(text="Parsing 12/13: Events…", overwrite=1)
            map_data["events"] = h6_rumors_and_events.parse_events()

            xprint(type=MsgType.ACTION, text="Parsing 13/13: Null Bytes…", overwrite=1)
            map_data["null_bytes"] = h9_null.read_null()

            xprint(type=MsgType.SPECIAL, text=DONE)

    except FileNotFoundError:
        xprint(type=MsgType.ERROR, text=f"Could not find {filename}.")


def save(filename: str = None) -> bool:
    global map_file

    draw_header()

    # Prompt for filename if not provided
    if filename is None:
        filename = xprint(type=MsgType.PROMPT, text="Enter a new filename")
        if not filename:
            return False

    # Ensure the filename has the correct extension
    filename = filename if filename[-4:] == ".h3m" else filename + ".h3m"

    if not is_file_writable(filename):
        return False

    xprint(type=MsgType.ACTION, text=f"Saving {filename}…")

    # Save the map data to the specified filename
    with gzopen(filename, "wb") as io.out_file:
        h1_general.write(map_data["general"])
        h2_players.write(map_data["player_specs"])
        h3_conditions.write_conditions(map_data["conditions"])
        h2_players.write_teams(map_data["teams"])
        h4_heroes.write_starting_heroes(map_data["starting_heroes"])
        h5_additional_flags.write_flags(map_data["ban_flags"])
        h6_rumors_and_events.write_rumors(map_data["rumors"])
        h4_heroes.write_hero_data(map_data["hero_data"])
        h7_terrain.write_terrain(map_data["terrain"])
        h8_objects.write_object_defs(map_data["object_defs"])
        h8_objects.write_object_data(map_data["object_data"])
        h6_rumors_and_events.write_events(map_data["events"])
        h9_null.write_null(map_data["null_bytes"])

    map_file = None

    xprint(type=MsgType.SPECIAL, text=DONE)

    return True
