import os
import shutil
from gzip import GzipFile
from gzip import open as gzopen

from src.handlers import handler_01_map_specs as h1
from src.handlers import handler_02_players_and_teams as h2
from src.handlers import handler_03_conditions as h3
from src.handlers import handler_04_heroes as h4
from src.handlers import handler_05_additional_flags as h5
from src.handlers import handler_06_rumors_and_events as h6
from src.handlers import handler_07_terrain as h7
from src.handlers import handler_08_objects as h8

from .common import DONE, Text, draw_header, is_file_writable, map_data, xprint

in_file = None
out_file = None


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
    if not filename:
        user_input = xprint(type=Text.PROMPT, text="Enter the map filename to load")
        if not user_input:
            return False
        filename = user_input

    # Ensure the filename has the correct extension
    filename = filename if filename[-4:] == ".h3m" else filename + ".h3m"

    xprint(type=Text.NORMAL, text=f"Loading {filename}...\n")

    try:
        with gzopen(filename, "rb") as in_file:
            map_data["filename"] = filename

            xprint(text="Parsing 1/13: Map Specs...", overwrite=1)
            map_data["map_specs"] = h1.parse_map_specs()

            xprint(text="Parsing 2/13: Player Specs...", overwrite=1)
            map_data["player_specs"] = h2.parse_player_specs()

            xprint(text="Parsing 3/13: Victory/Loss Conditions...", overwrite=1)
            map_data["conditions"] = h3.parse_conditions()

            xprint(text="Parsing 4/13: Teams...", overwrite=1)
            map_data["teams"] = h2.parse_teams()

            xprint(text="Parsing 5/13: Hero Availability...", overwrite=1)
            map_data["starting_heroes"] = h4.parse_starting_heroes()

            xprint(text="Parsing 6/13: Additional Specs...", overwrite=1)
            map_data["ban_flags"] = h5.parse_flags()

            xprint(text="Parsing 7/13: Rumors...", overwrite=1)
            map_data["rumors"] = h6.parse_rumors()

            xprint(text="Parsing 8/13: Hero Templates...", overwrite=1)
            map_data["hero_data"] = h4.parse_hero_data()

            xprint(text="Parsing 9/13: Terrain Data...", overwrite=1)
            map_data["terrain"] = h7.parse_terrain(map_data["map_specs"])

            xprint(text="Parsing 10/13: Object Defs...", overwrite=1)
            map_data["object_defs"] = h8.parse_object_defs()

            xprint(text="Parsing 11/13: Object Data...", overwrite=1)
            map_data["object_data"] = h8.parse_object_data(map_data["object_defs"], map_data["filename"])

            xprint(text="Parsing 12/13: Events...", overwrite=1)
            map_data["events"] = h6.parse_events()

            xprint(type=Text.ACTION, text="Parsing 13/13: Null Bytes...", overwrite=1)
            map_data["null_bytes"] = in_file.read()

            xprint(type=Text.SPECIAL, text=DONE)
    except FileNotFoundError:
        xprint(type=Text.ERROR, text=f"Could not find {filename}.")


def save_map(quicksave: bool = False) -> bool:
    global out_file

    draw_header()

    if quicksave:
        filename = map_data["filename"]
    else:
        user_input = xprint(type=Text.PROMPT, text="Enter a new filename")
        if not user_input:
            return False
        filename = user_input if user_input[-4:] == ".h3m" else user_input + ".h3m"

    if not filename or not is_file_writable(filename):
        return False

    # Create backup if filename matches the current map
    if filename == map_data["filename"]:
        backup_dir = "backups"
        base_name = os.path.basename(map_data["filename"][:-4])
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith(base_name) and f.endswith(".h3m")]
        next_suffix = 0

        if backup_files:
            suffixes = [int(f.split("_")[-1].split(".")[0]) for f in backup_files]
            next_suffix = max(suffixes) + 1

        backup_filename = os.path.join(backup_dir, f"{base_name}_{next_suffix:04d}.h3m")

        try:
            xprint(type=Text.ACTION, text=f"Creating {backup_filename}...")
            shutil.copy2(map_data["filename"], backup_filename)
            xprint(type=Text.SPECIAL, text=DONE)
            xprint()
        except Exception as e:
            xprint(type=Text.ERROR, text=f"Failed to create backup: {e}")

    xprint(type=Text.ACTION, text=f"Saving {filename}...")

    # Save the map data to the specified filename
    with open(filename, "wb") as f:
        with GzipFile(filename="", mode="wb", fileobj=f) as out_file:
            h1.write_map_specs(map_data["map_specs"])
            h2.write_player_specs(map_data["player_specs"])
            h3.write_conditions(map_data["conditions"])
            h2.write_teams(map_data["teams"])
            h4.write_starting_heroes(map_data["starting_heroes"])
            h5.write_flags(map_data["ban_flags"])
            h6.write_rumors(map_data["rumors"])
            h4.write_hero_data(map_data["hero_data"])
            h7.write_terrain(map_data["terrain"])
            h8.write_object_defs(map_data["object_defs"])
            h8.write_object_data(map_data["object_data"])
            h6.write_events(map_data["events"])
            out_file.write(map_data["null_bytes"])

    xprint(type=Text.SPECIAL, text=DONE)

    return True
