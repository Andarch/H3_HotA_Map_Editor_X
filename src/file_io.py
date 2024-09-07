from gzip import open
from .common  import *
from . import handler_01_general           as h1
from . import handler_02_players_and_teams as h2
from . import handler_03_conditions        as h3
from . import handler_04_heroes            as h4
from . import handler_05_additional_flags  as h5
from . import handler_06_rumors_and_events as h6
from . import handler_07_terrain           as h7
from . import handler_08_objects           as h8
from H3_HotA_MEX import map_data, menus

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

def open_prompts() -> bool:
    def main() -> str:
        global menus
        while True:
            input, _ = menu_prompt(menus["open"])
            result = process_keypress(input)
            if result == "esc":
                break
            match result:
                case "success": return True
                case "esc": return False
    def process_keypress(input: str) -> str:
        def main() -> str:
            global map_data
            match input:
                case "1":
                    map_data["Map 1"] = {}
                    map_data["Map 2"] = None
                case "2":
                    map_data["Map 1"] = {}
                    map_data["Map 2"] = {}
                case "esc":
                    return "esc"
            while True:
                draw_header()
                result = process_filename("Map 1", input)
                match result:
                    case "success": return "success"
                    case "failure": continue
                    case "esc": return ""
                if input == "2":
                    if not process_filename("Map 2", input):
                        continue
        def process_filename(map_key: str, input: str) -> str:
            def main() -> str:
                match input:
                    case "1": prompt = "Enter the map filename"
                    case "2": prompt = f"Enter the filename for {map_key}"
                filename = xprint(type = MSG.PROMPT, text = prompt)
                if filename:
                    filename = append_h3m(filename)
                    if open_map(filename, map_key):
                        return "success"
                    else:
                        xprint(type = MSG.ERROR, text = f"Could not find {filename}.", align = True)
                        return "failure"
                else:
                    return "esc"
            def open_map(filename: str, map_key: str) -> bool:
                global map_data, in_file
                xprint(type = MSG.ACTION, text = f"Loading {filename}...")
                try:
                    with open(filename, "rb"):
                        pass
                except FileNotFoundError:
                    return False
                with open(filename, "rb") as in_file:
                    map_data[map_key]["filename"]     = filename
                    map_data[map_key]["general"]      = h1.parse_general()
                    map_data[map_key]["player_specs"] = h2.parse_player_specs()
                    map_data[map_key]["conditions"]   = h3.parse_conditions()
                    map_data[map_key]["teams"]        = h2.parse_teams()
                    map_data[map_key]["start_heroes"] = h4.parse_starting_heroes(map_data[map_key]["general"])
                    map_data[map_key]["ban_flags"]    = h5.parse_flags()
                    map_data[map_key]["rumors"]       = h6.parse_rumors()
                    map_data[map_key]["hero_data"]    = h4.parse_hero_data()
                    map_data[map_key]["terrain"]      = h7.parse_terrain(map_data[map_key]["general"])
                    map_data[map_key]["object_defs"]  = h8.parse_object_defs()
                    map_data[map_key]["object_data"]  = h8.parse_object_data(map_data[map_key]["object_defs"])
                    map_data[map_key]["events"]       = h6.parse_events()
                    map_data[map_key]["null_bytes"]   = in_file.read()
                xprint(type = MSG.SPECIAL, text = DONE)
                return True
            return main()
        return main()
    return main()

# def save_map_prompts() -> None:
#     if map_data["Map 2"] is not None:
#         filename1 = print_string_prompt("Enter a filename to save Map 1")
#         if filename1.lower() in BACK_COMMANDS:
#             print(ABORT_MSG)
#             return
#         save_map(filename1, "Map 1")
#         filename2 = print_string_prompt("Enter a filename to save Map 2")
#         if filename2.lower() in BACK_COMMANDS:
#             print(ABORT_MSG)
#             return
#         save_map(filename2, "Map 2")
#     else:
#         filename1 = print_string_prompt("Enter a filename to save the map")
#         if filename1.lower() in BACK_COMMANDS:
#             print(ABORT_MSG)
#             return
#         save_map(filename1, "Map 1")

# def save_map(filename: str, map_key: str) -> None:
#     if len(filename) > 4:
#         if filename[-4:] != ".h3m":
#             filename += ".h3m"
#     else: filename += ".h3m"

#     print_action("Saving map...")

#     with open(filename, "wb") as io.out_file:
#         h1.write_general(        map_data[map_key]["general"])
#         h2.write_player_specs(   map_data[map_key]["player_specs"])
#         h3.write_conditions(     map_data[map_key]["conditions"])
#         h2.write_teams(          map_data[map_key]["teams"])
#         h4.write_starting_heroes(map_data[map_key]["start_heroes"])
#         h5.write_flags(          map_data[map_key]["ban_flags"])
#         h6.write_rumors(         map_data[map_key]["rumors"])
#         h4.write_hero_data(      map_data[map_key]["hero_data"])
#         h7.write_terrain(        map_data[map_key]["terrain"])
#         h8.write_object_defs(    map_data[map_key]["object_defs"])
#         h8.write_object_data(    map_data[map_key]["object_data"])
#         h6.write_events(         map_data[map_key]["events"])
#         io.out_file.write(       map_data[map_key]["null_bytes"])

#     print_done()

def append_h3m(filename: str) -> str:
    if filename[-4:] != ".h3m":
        filename += ".h3m"
    return filename
