from gzip import open as gzopen
from gzip import GzipFile
from typing import Tuple
from .common  import *
from .menus import *
from . import handler_01_general           as h1
from . import handler_02_players_and_teams as h2
from . import handler_03_conditions        as h3
from . import handler_04_heroes            as h4
from . import handler_05_additional_flags  as h5
from . import handler_06_rumors_and_events as h6
from . import handler_07_terrain           as h7
from . import handler_08_objects           as h8

in_file  = None
out_file = None

def read_raw(length: int) -> bytes:
    global in_file
    return in_file.read(length)

def read_int(length: int) -> int:
    global in_file
    return int.from_bytes(in_file.read(length), 'little')

def read_str(length: int) -> str:
    global in_file
    return in_file.read(length).decode('latin-1')

def read_bits(length: int) -> list:
    temp_bits = []
    raw_data  = read_raw(length)

    for c in raw_data:
        bits = format(int(c), '#010b').removeprefix('0b')[::-1]
        for b in bits:
            temp_bits.append(1 if b == '1' else 0)

    return temp_bits

def write_raw(data: bytes):
    global out_file
    out_file.write(data)

def write_int(data: int, length: int) -> None:
    global out_file
    out_file.write(data.to_bytes(length, 'little'))

def write_str(data: str) -> None:
    global out_file
    out_file.write(data.encode('latin-1'))

def write_bits(data: list) -> None:
    for i in range(0, len(data), 8):
        s = ""
        for b in range(8):
            s += '1' if data[i + b] else '0'
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
        s += ' ' * (3-len(n))  + n + ' '
        s += format(int(n), '#010b').removeprefix('0b')
        s += '\n'
        i += 1

    print(s)
    in_file.seek(-length, 1)

def load_maps(input=-1) -> bool:
    def main(input: int) -> bool:
        while True:
            if input == -1:
                amount = get_map_amount()
                if not amount: return False
            else: amount = input
            while True:
                filename, success = load_map(MAP1, amount)
                if not filename:
                    if input == -1: break
                    else: return False
                if not success: continue
                if amount is 1: return True
                if amount is 2:
                    first_loop = True
                    while True:
                        if first_loop: new_screen = False
                        else: new_screen = True
                        filename, success = load_map(MAP2, amount, new_screen)
                        if not filename: break
                        if not success: continue
                        return True

    def get_map_amount() -> int:
        input = xprint(menu=Menu.LOAD.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    def load_map(map_key: str, amount: int, new_screen=True) -> Tuple[bool, bool]:
        def main() -> Tuple[bool, bool]:
            draw_header(new_screen=new_screen)
            filename = get_filename(map_key, amount)
            if not filename: return False, False
            success = test_load(filename)
            if not success: return True, False
            parse_map(filename, map_key)
            return True, True

        def get_filename(map_key: str, amount: int) -> str:
            if amount == 1: prompt = "Enter the map filename to load"
            elif amount == 2: prompt = f"Enter the filename for {map_key}"
            input = xprint(type=Text.PROMPT, text=prompt)
            if input: filename = append_h3m(input)
            else: return False
            return filename

        def test_load(filename: str) -> str:
            xprint(type=Text.NORMAL, text=f"Loading {filename}...")
            xprint()
            try:
                with gzopen(filename, "rb"): return True
            except FileNotFoundError:
                xprint(type=Text.ERROR, text=f"Could not find {filename}.", align=Align.FLUSH)
                return False

        def parse_map(filename: str, map_key: str) -> bool:
            global map_data, in_file
            with gzopen(filename, "rb") as in_file:
                map_data[map_key]["filename"]     = filename
                xprint(text=f"Parsing 1/13: Map Specs...", overwrite=1)
                map_data[map_key]["map_specs"]      = h1.parse_general()
                xprint(text=f"Parsing 2/13: Player Specs...", overwrite=1)
                map_data[map_key]["player_specs"] = h2.parse_player_specs()
                xprint(text=f"Parsing 3/13: Victory/Loss Conditions...", overwrite=1)
                map_data[map_key]["conditions"]   = h3.parse_conditions()
                xprint(text=f"Parsing 4/13: Teams...", overwrite=1)
                map_data[map_key]["teams"]        = h2.parse_teams()
                xprint(text=f"Parsing 5/13: Hero Availability...", overwrite=1)
                map_data[map_key]["start_heroes"] = h4.parse_starting_heroes(map_data[map_key]["map_specs"])
                xprint(text=f"Parsing 6/13: Additional Specs...", overwrite=1)
                map_data[map_key]["ban_flags"]    = h5.parse_flags()
                xprint(text=f"Parsing 7/13: Rumors...", overwrite=1)
                map_data[map_key]["rumors"]       = h6.parse_rumors()
                xprint(text=f"Parsing 8/13: Hero Templates...", overwrite=1)
                map_data[map_key]["hero_data"]    = h4.parse_hero_data()
                xprint(text=f"Parsing 9/13: Terrain Data...", overwrite=1)
                map_data[map_key]["terrain"]      = h7.parse_terrain(map_data[map_key]["map_specs"])
                xprint(text=f"Parsing 10/13: Object Defs...", overwrite=1)
                map_data[map_key]["object_defs"]  = h8.parse_object_defs()
                xprint(text=f"Parsing 11/13: Object Data...", overwrite=1)
                map_data[map_key]["object_data"]  = h8.parse_object_data(map_data[map_key]["object_defs"])
                xprint(text=f"Parsing 12/13: Events...", overwrite=1)
                map_data[map_key]["events"]       = h6.parse_events()
                xprint(type=Text.ACTION, text=f"Parsing 13/13: Null Bytes...", overwrite=1)
                map_data[map_key]["null_bytes"]   = in_file.read()
            map_data[map_key]["general"] = {
                "filename": map_data[map_key]["filename"],
                "map_specs": map_data[map_key]["map_specs"],
                "teams": map_data[map_key]["teams"],
                "conditions": map_data[map_key]["conditions"],
                "start_heroes": map_data[map_key]["start_heroes"],
                "ban_flags": map_data[map_key]["ban_flags"]
            }
            xprint(type=Text.SPECIAL, text=DONE)

        return main()
    return main(input)

def save_maps() -> bool:
    def main() -> bool:
        global map_data
        while True:
            if map_data["Map 2"]:
                amount = get_map_amount()
                if not amount: return False
            else: amount = 1
            while True:
                type = get_save_type()
                if not type:
                    if map_data["Map 2"]: break
                    else: return False
                while True:
                    filename, success = save_map(MAP1, amount, type)
                    if not filename: break
                    if not success: continue
                    if amount is 1: return True
                    if amount is 2:
                        first_loop = True
                        while True:
                            if first_loop: new_screen = False
                            else: new_screen = True
                            filename, success = save_map(MAP2, amount, type, new_screen)
                            if not filename: break
                            if not success: continue
                            return True

    def get_map_amount() -> int:
        input = xprint(menu=Menu.SAVE_A.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    def get_save_type() -> int:
        input = xprint(menu=Menu.SAVE_B.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    def save_map(map_key: str, amount: int, type: int, new_screen=True) -> Tuple[bool, bool]:
        def main() -> Tuple[bool, bool]:
            draw_header(new_screen=new_screen)
            if type is 1: filename = map_data[map_key]["filename"]
            if type is 2: filename = get_filename(map_key, amount)
            if not filename: return False, False
            save_parsed_data(filename, map_key)
            return True, True

        def get_filename(map_key: str, amount: int) -> str:
            if amount == 1: prompt = "Enter a new filename"
            elif amount == 2: prompt = f"Enter a new filename for {map_key}"
            input = xprint(type=Text.PROMPT, text=prompt)
            if input: filename = append_h3m(input)
            else: return False
            return filename

        def save_parsed_data(filename: str, map_key: str) -> bool:
            global map_data, out_file
            xprint(type=Text.ACTION, text=f"Saving {filename}...")
            with open(filename, "wb") as f:
                with GzipFile(filename="", mode="wb", fileobj=f) as out_file:
                    h1.write_general(        map_data[map_key]["map_specs"])
                    h2.write_player_specs(   map_data[map_key]["player_specs"])
                    h3.write_conditions(     map_data[map_key]["conditions"])
                    h2.write_teams(          map_data[map_key]["teams"])
                    h4.write_starting_heroes(map_data[map_key]["start_heroes"])
                    h5.write_flags(          map_data[map_key]["ban_flags"])
                    h6.write_rumors(         map_data[map_key]["rumors"])
                    h4.write_hero_data(      map_data[map_key]["hero_data"])
                    h7.write_terrain(        map_data[map_key]["terrain"])
                    h8.write_object_defs(    map_data[map_key]["object_defs"])
                    h8.write_object_data(    map_data[map_key]["object_data"])
                    h6.write_events(         map_data[map_key]["events"])
                    out_file.write(          map_data[map_key]["null_bytes"])
            xprint(type=Text.SPECIAL, text=DONE)
            return True
        return main()
    return main()

def append_h3m(input: str) -> str:
    if input[-4:] != ".h3m": filename = input + ".h3m"
    else: filename = input
    return filename
