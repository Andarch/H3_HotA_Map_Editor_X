#!/usr/bin/env python3

import sys
import threading
from enum import Enum
from gzip import open
from src import *

HELP_COMMANDS = ["help", "h"]
BACK_COMMANDS = ["/back", "/return", "/b", "/r"]
EXIT_COMMANDS = ["/exit", "/quit", "/e", "/q"]
ERROR_NO_MAP = "Error: No map loaded."
ERROR_HELP = (f"For help, enter one of these commands:\n{CLR.CYAN}\t{"\n\t".join(HELP_COMMANDS)}\n{CLR.RESET}"
              f"To exit, enter one of these commands:\n{CLR.CYAN}\t{"\n\t".join(EXIT_COMMANDS)}\n{CLR.RESET}")
ABORT_MSG = "Operation aborted.\n"
EXIT_MSG = "Exiting program..."

menu_start = [
    "OPEN",
    "QUIT"
]

valid_files = []

map_data = {
    "Map 1": None,
    "Map 2": None
}

#################
# MAIN FUNCTION #
#################

def main() -> None:

    ##################
    # INITIALIZATION #
    ##################

    map_key = "Map 1"
    busy = False
    global previous_width

    ####################
    # HELPER FUNCTIONS #
    ####################

    def open_maps() -> None:
        def main() -> str:
            while True:
                start_new_screen()
                cprint(type = MSG.MENU, menu_item = 1, text = "Open 1 map")
                cprint(type = MSG.MENU, menu_item = 2, text = "Open 2 maps")
                result = process_key_press(detect_key_press("12"))
                if result == "esc":
                    break
        def process_key_press(choice: str) -> str:
            def main() -> str:
                match choice:
                    case "1":
                        map_data["Map 1"] = {}
                        map_data["Map 2"] = None
                    case "2":
                        map_data["Map 1"] = {}
                        map_data["Map 2"] = {}
                    case "esc":
                        return "esc"
                while True:
                    start_new_screen()
                    result = process_filename("Map 1", choice)
                    match result:
                        case "success": return "success"
                        case "failure": continue
                        case "esc": return
                    if choice == "2":
                        if not process_filename("Map 2", choice):
                            continue
            def process_filename(map_key: str, choice: str) -> str:
                match choice:
                    case "1":
                        prompt = "Enter the map filename"
                    case "2":
                        prompt = f"Enter the filename for {map_key}"
                filename = cprint(type = MSG.PROMPT, text = prompt)
                if filename:
                    filename = append_h3m(filename)
                    if open_map(filename, map_key):
                        return "success"
                    else:
                        cprint(type = MSG.ERROR, text = f"Could not find {filename}.", flush = True)
                        return "failure"
                else:
                    return "esc"
            return main()
        return main()

    def open_map(filename: str, map_key: str) -> None:
        cprint(type = MSG.ACTION, text = f"Loading {filename}...")
        try:
            with open(filename, "rb"):
                pass
        except FileNotFoundError:
            return False
        with open(filename, "rb") as io.in_file:
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
            map_data[map_key]["null_bytes"]   = io.in_file.read()
        cprint(type = MSG.SPECIAL, text = DONE)
        terminal_width = get_terminal_width()
        cprint(type = MSG.INFO, text = "-" * terminal_width)
        cprint(type = MSG.INFO, text = f"{map_data[map_key]["general"]["name"]}")
        cprint(type = MSG.INFO, text = "-" * terminal_width)
        cprint(type = MSG.INFO, text = f"{map_data[map_key]["general"]["description"]}")
        cprint(type = MSG.INFO, text = "-" * terminal_width)
        return True

    def save_maps() -> None:
        # Check if a second map is open
        if map_data["Map 2"] is not None:
            filename1 = print_string_prompt("Enter a filename to save Map 1")
            if filename1.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            save_map(filename1, "Map 1")
            filename2 = print_string_prompt("Enter a filename to save Map 2")
            if filename2.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            save_map(filename2, "Map 2")
        else:
            filename1 = print_string_prompt("Enter a filename to save the map")
            if filename1.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            save_map(filename1, "Map 1")

    def save_map(filename: str, map_key: str) -> None:
        # Make sure that the filename ends with ".h3m". For convenience,
        # users should be able to save maps without typing the extension.
        if len(filename) > 4:
            if filename[-4:] != ".h3m":
                filename += ".h3m"
        else: filename += ".h3m"

        print_action("Saving map...")

        # Save the map byte by byte.
        with open(filename, "wb") as io.out_file:
            h1.write_general(        map_data[map_key]["general"])
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
            io.out_file.write(       map_data[map_key]["null_bytes"])

        print_done()

    def append_h3m(filename: str) -> str:
        if filename[-4:] != ".h3m":
            filename += ".h3m"
        return filename

    def get_map_key() -> str:
        if map_data["Map 2"] is None:
            return "Map 1"

        print("Select a map:")
        print_cyan(f"   1. {map_data["Map 1"]["filename"]}")
        print_cyan(f"   2. {map_data["Map 2"]["filename"]}")
        print()
        choice = detect_key_press("Choose a map", "12")
        return "Map 1" if choice == "1" else "Map 2"

    # def check_if_nav_cmd(string: str) -> bool:
    #     if string.lower() in BACK_COMMANDS:
    #         return True
    #     elif string.lower() in EXIT_COMMANDS:
    #         exit()
    #     return False

    def exit() -> None:
        print(EXIT_MSG)
        time.sleep(SLEEP.NORMAL)
        print(f"{CLR.RESET}")
        sys.exit(0)

    #############
    # EXECUTION #
    #############

    previous_width = get_terminal_width()
    monitor_thread = threading.Thread(target = monitor_terminal_size, daemon = True)
    monitor_thread.start()

    hide_cursor(True)
    # time.sleep(SLEEP.NORMAL)

    while True:
        start_new_screen()
        for i, option in enumerate(menu_start):
            cprint(type = MSG.MENU, menu_item = i + 1, text = option)
        choice = detect_key_press("12")

        match choice:
            case "1": open_maps()
            case "2": exit()

        time.sleep(SLEEP.TIC)

    # while True:
    #     if not busy:
    #         busy = True
    #         print("Select an option:")
    #         print_cyan("   1. Open map(s)")
    #         print_cyan("   2. Quit editor")
    #         print()
    #         command = detect_key_press("12")
    #     else:
    #         continue

    #     try:
    #         match command.split():
    #             case ["load"] | ["open"]:
    #                 open_maps()

    #             case ["save"]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     save_maps()

    #             case ["print", data_key]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.print_data(map_data[map_key], data_key)

    #             case ["export", filename]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.export_json(map_data[map_key], filename)

    #             case ["count"]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.count_objects(map_data[map_key]["object_data"])

    #             case ["swap"]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.swap_layers(
    #                         map_data[map_key]["terrain"],
    #                         map_data[map_key]["object_data"],
    #                         map_data[map_key]["player_specs"],
    #                         map_data[map_key]["general"]["is_two_level"],
    #                         map_data[map_key]["conditions"]
    #                     )

    #             case ["towns"]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.modify_towns(map_data[map_key]["object_data"])

    #             case ["minimap"]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.generate_minimap(
    #                         map_data[map_key]["general"],
    #                         map_data[map_key]["terrain"],
    #                         map_data[map_key]["object_data"],
    #                         map_data[map_key]["object_defs"]
    #                     )

    #             case ["events"]:
    #                 if map_data["Map 1"] is None:
    #                     print_error(ERROR_NO_MAP)
    #                 else:
    #                     map_key = get_map_key()
    #                     scripts.update_events(
    #                         map_data[map_key]["events"],
    #                         map_data[map_key]["object_data"]
    #                     )

    #             case ["help"] | ["h"]:
    #                 print_cyan(
    #                     "Basic commands:\n"
    #                     "   help | h\n"
    #                     "   load | open\n"
    #                     "   save\n"
    #                     "   /back | /return | /b | /r\n"
    #                     "   /exit | /quit | /e | /q\n"
    #                     "\n"
    #                     "Script commands:\n"
    #                     "   count\n"
    #                     "   events\n"
    #                     "   export <filename>.json\n"
    #                     "   minimap\n"
    #                     "   print <key>\n"
    #                     "   swap\n"
    #                     "   towns\n"
    #                     "\n"
    #                     "Print categories:\n"
    #                     "   general\n"
    #                     "   player_specs\n"
    #                     "   conditions\n"
    #                     "   teams\n"
    #                     "   start_heroes\n"
    #                     "   ban_flags\n"
    #                     "   rumors\n"
    #                     "   hero_data\n"
    #                     "   terrain\n"
    #                     "   object_defs\n"
    #                     "   object_data\n"
    #                     "   events\n"
    #                     "   null_bytes\n"
    #                 )

    #             case [cmd]:
    #                 if cmd in BACK_COMMANDS:
    #                     print_error("Error: You are already at the main menu.")
    #                     print(ERROR_HELP)
    #                     continue
    #                 elif cmd in EXIT_COMMANDS:
    #                     exit()
    #                 else:
    #                     print_error("Error: Unrecognized command.")
    #                     print(ERROR_HELP)
    #     finally:
    #         busy = False

if __name__ == "__main__":
    main()
