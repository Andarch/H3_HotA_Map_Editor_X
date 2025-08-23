from gzip import GzipFile
from gzip import open as gzopen

from ..common import (
    DONE,
    MsgType,
    draw_header,
    is_file_writable,
    map,
    map_data,
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
)

h3m = None


def load(filename: str = None) -> None:
    global map_data, h3m

    draw_header()

    # Prompt for filename if not provided
    if filename is None:
        filename = xprint(type=MsgType.PROMPT, text="Enter the map filename to load")
        if not filename:
            return False

    # Ensure the filename has the correct extension
    filename = filename if filename[-4:] == ".h3m" else filename + ".h3m"

    xprint(type=MsgType.NORMAL, text=f"Loading {filename}...\n")

    try:
        with gzopen(filename, "rb") as h:
            h3m = h

            map_data["filename"] = filename

            xprint(text="Parsing 1/13: General...", overwrite=1)
            map_data["general"] = h1_general.read()

            xprint(text="Parsing 2/13: Player Specs...", overwrite=1)
            map_data["player_specs"] = h2_players.read()

            xprint(text="Parsing 3/13: Victory/Loss Conditions...", overwrite=1)
            map_data["conditions"] = h3_conditions.parse_conditions()

            xprint(text="Parsing 4/13: Teams...", overwrite=1)
            map_data["teams"] = h2_players.parse_teams()

            xprint(text="Parsing 5/13: Hero Availability...", overwrite=1)
            map_data["starting_heroes"] = h4_heroes.parse_starting_heroes()

            xprint(text="Parsing 6/13: Additional Specs...", overwrite=1)
            map_data["ban_flags"] = h5_additional_flags.parse_flags()

            xprint(text="Parsing 7/13: Rumors...", overwrite=1)
            map_data["rumors"] = h6_rumors_and_events.parse_rumors()

            xprint(text="Parsing 8/13: Hero Templates...", overwrite=1)
            map_data["hero_data"] = h4_heroes.parse_hero_data()

            xprint(text="Parsing 9/13: Terrain Data...", overwrite=1)
            map_data["terrain"] = h7_terrain.parse_terrain(map_data["general"])

            xprint(text="Parsing 10/13: Object Defs...", overwrite=1)
            map_data["object_defs"] = h8_objects.parse_object_defs()

            xprint(text="Parsing 11/13: Object Data...", overwrite=1)
            map_data["object_data"] = h8_objects.parse_object_data(map_data["object_defs"], map_data["filename"])

            xprint(text="Parsing 12/13: Events...", overwrite=1)
            map_data["events"] = h6_rumors_and_events.parse_events()

            xprint(type=MsgType.ACTION, text="Parsing 13/13: Null Bytes...", overwrite=1)
            map_data["null_bytes"] = map.read()

            xprint(type=MsgType.SPECIAL, text=DONE)

        h3m = None

    except FileNotFoundError:
        xprint(type=MsgType.ERROR, text=f"Could not find {filename}.")


def save(filename: str = None) -> bool:
    global h3m

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

    xprint(type=MsgType.ACTION, text=f"Saving {filename}...")

    # Save the map data to the specified filename
    with open(filename, "wb") as f:
        with GzipFile(filename="", mode="wb", fileobj=f) as h:
            h3m = h
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
            h3m.write(map_data["null_bytes"])

    h3m = None

    xprint(type=MsgType.SPECIAL, text=DONE)

    return True
