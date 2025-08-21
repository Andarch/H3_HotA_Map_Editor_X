from gzip import GzipFile
from gzip import open as gzopen

from .common import (
    DONE,
    MsgType,
    draw_header,
    in_file,
    is_file_writable,
    map_data,
    out_file,
    xprint,
)
from .parse import parse_01_map_specs as p1
from .parse import parse_02_players_and_teams as p2
from .parse import parse_03_conditions as p3
from .parse import parse_04_heroes as p4
from .parse import parse_05_additional_flags as p5
from .parse import parse_06_rumors_and_events as p6
from .parse import parse_07_terrain as p7
from .parse import parse_08_objects as p8


def read_raw(length: int) -> bytes:
    global in_file
    return in_file.read(length)


def read_int(length: int) -> int:
    global in_file
    return int.from_bytes(in_file.read(length), "little")


def read_str(length: int) -> str:
    global in_file
    return in_file.read(length).decode("latin-1")


def read_bits(length: int) -> list:
    temp_bits = []
    raw_data = read_raw(length)

    for c in raw_data:
        bits = format(int(c), "#010b").removeprefix("0b")[::-1]
        for b in bits:
            temp_bits.append(1 if b == "1" else 0)

    return temp_bits


def write_raw(data: bytes):
    global out_file
    out_file.write(data)


def write_int(data: int, length: int) -> None:
    global out_file
    out_file.write(data.to_bytes(length, "little"))


def write_str(data: str) -> None:
    global out_file
    out_file.write(data.encode("latin-1"))


def write_bits(data: list) -> None:
    for i in range(0, len(data), 8):
        s = ""
        for b in range(8):
            s += "1" if data[i + b] else "0"
        write_int(int(s[::-1], 2), 1)


def seek(length: int) -> None:
    global in_file
    in_file.seek(length, 1)


def peek(length: int) -> None:
    global in_file
    data = read_raw(length)

    s = "\n"
    i = 1
    for b in data:
        n = str(b)
        s += ("  " if i < 10 else " ") + str(i) + ": "
        s += " " * (3 - len(n)) + n + " "
        s += format(int(n), "#010b").removeprefix("0b")
        s += "\n"
        i += 1

    print(s)
    in_file.seek(-length, 1)


def load_map(filename: str = None) -> None:
    global map_data, in_file

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
        with gzopen(filename, "rb") as i:
            in_file = i

            map_data["filename"] = filename

            xprint(text="Parsing 1/13: Map Specs...", overwrite=1)
            map_data["map_specs"] = p1.parse_map_specs()

            xprint(text="Parsing 2/13: Player Specs...", overwrite=1)
            map_data["player_specs"] = p2.parse_player_specs()

            xprint(text="Parsing 3/13: Victory/Loss Conditions...", overwrite=1)
            map_data["conditions"] = p3.parse_conditions()

            xprint(text="Parsing 4/13: Teams...", overwrite=1)
            map_data["teams"] = p2.parse_teams()

            xprint(text="Parsing 5/13: Hero Availability...", overwrite=1)
            map_data["starting_heroes"] = p4.parse_starting_heroes()

            xprint(text="Parsing 6/13: Additional Specs...", overwrite=1)
            map_data["ban_flags"] = p5.parse_flags()

            xprint(text="Parsing 7/13: Rumors...", overwrite=1)
            map_data["rumors"] = p6.parse_rumors()

            xprint(text="Parsing 8/13: Hero Templates...", overwrite=1)
            map_data["hero_data"] = p4.parse_hero_data()

            xprint(text="Parsing 9/13: Terrain Data...", overwrite=1)
            map_data["terrain"] = p7.parse_terrain(map_data["map_specs"])

            xprint(text="Parsing 10/13: Object Defs...", overwrite=1)
            map_data["object_defs"] = p8.parse_object_defs()

            xprint(text="Parsing 11/13: Object Data...", overwrite=1)
            map_data["object_data"] = p8.parse_object_data(map_data["object_defs"], map_data["filename"])

            xprint(text="Parsing 12/13: Events...", overwrite=1)
            map_data["events"] = p6.parse_events()

            xprint(type=MsgType.ACTION, text="Parsing 13/13: Null Bytes...", overwrite=1)
            map_data["null_bytes"] = in_file.read()

            xprint(type=MsgType.SPECIAL, text=DONE)

        in_file = None

    except FileNotFoundError:
        xprint(type=MsgType.ERROR, text=f"Could not find {filename}.")


def save_map(filename: str = None) -> bool:
    global out_file

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
        with GzipFile(filename="", mode="wb", fileobj=f) as o:
            out_file = o
            p1.write_map_specs(map_data["map_specs"])
            p2.write_player_specs(map_data["player_specs"])
            p3.write_conditions(map_data["conditions"])
            p2.write_teams(map_data["teams"])
            p4.write_starting_heroes(map_data["starting_heroes"])
            p5.write_flags(map_data["ban_flags"])
            p6.write_rumors(map_data["rumors"])
            p4.write_hero_data(map_data["hero_data"])
            p7.write_terrain(map_data["terrain"])
            p8.write_object_defs(map_data["object_defs"])
            p8.write_object_data(map_data["object_data"])
            p6.write_events(map_data["events"])
            out_file.write(map_data["null_bytes"])

    out_file = None

    xprint(type=MsgType.SPECIAL, text=DONE)

    return True
