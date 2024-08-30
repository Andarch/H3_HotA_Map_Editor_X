#!/usr/bin/env python3

import os
import sys
from enum import Enum
from gzip import open

from src import *

HELP_COMMANDS = ['help', 'h']
BACK_COMMANDS = ['/back', '/return', '/b', '/r']
EXIT_COMMANDS = ['/exit', '/quit', '/e', '/q']
ERROR_NO_MAP = "Error: No map loaded."
ERROR_HELP = (f"For help, enter one of these commands:\n{COLOR.CYAN}\t{'\n\t'.join(HELP_COMMANDS)}\n{COLOR.RESET}"
              f"To exit, enter one of these commands:\n{COLOR.CYAN}\t{'\n\t'.join(EXIT_COMMANDS)}\n{COLOR.RESET}")
ABORT_MSG = "Operation aborted.\n"
EXIT_MSG = "Exiting program..."

map_data = {
    "map1": None,
    "map2": None
}

#################
# MAIN FUNCTION #
#################

def main() -> None:

    ##################
    # INITIALIZATION #
    ##################

    map_key = "map1"
    busy = False

    ####################
    # HELPER FUNCTIONS #
    ####################

    def exit() -> None:
        print(EXIT_MSG)
        time.sleep(SLEEP_TIME)
        print(f"{COLOR.RESET}")
        sys.exit(0)

    def get_map_key() -> str:
        if map_data["map2"] is None:
            return "map1"

        choice = print_prompt("Which map? (1 or 2)")
        if choice.lower() in BACK_COMMANDS:
            print(ABORT_MSG)
            return
        elif choice.lower() in EXIT_COMMANDS:
            exit()

        return "map1" if choice == '1' else "map2"

    def open_maps() -> None:
        while True:
            num_maps = print_prompt("Enter the number of maps to open")

            if num_maps.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            elif num_maps.lower() in EXIT_COMMANDS:
                exit()

            if num_maps == '1':
                map_data["map1"] = {}
                map_data["map2"] = None
                while True:
                    filename1 = print_prompt("Enter the map filename")
                    if filename1.lower() in BACK_COMMANDS:
                        break
                    elif filename1.lower() in EXIT_COMMANDS:
                        exit()
                    if open_map(filename1, "map1"):
                        return
                    else:
                        print_error(f"ERROR: Could not find '{filename1}'.")
            elif num_maps == '2':
                map_data["map1"] = {}
                map_data["map2"] = {}
                back_command_used = False
                while True:
                    filename1 = print_prompt("Enter the filename for map 1")
                    if filename1.lower() in BACK_COMMANDS:
                        back_command_used = True
                        break
                    elif filename1.lower() in EXIT_COMMANDS:
                        exit()
                    if open_map(filename1, "map1"):
                        break
                    else:
                        print_error(f"ERROR: Could not find '{filename1}'.")
                if back_command_used:
                    continue
                while True:
                    filename2 = print_prompt("Enter the filename for map 2")
                    if filename2.lower() in BACK_COMMANDS:
                        print("Loading of map 2 aborted. Map 1 is still loaded.\n")
                        break
                    elif filename2.lower() in EXIT_COMMANDS:
                        exit()
                    if open_map(filename2, "map2"):
                        return
                    else:
                        print_error(f"ERROR: Could not find '{filename2}'.")
                break
            else:
                print_error("Error: Can only load 1 or 2 maps.")

    def open_map(filename: str, map_key: str) -> None:
        # Make sure that the filename ends with ".h3m". For convenience,
        # users should be able to open maps without typing the extension.
        if filename[-4:] != ".h3m":
            filename += ".h3m"

        print_action("Loading map...")

        # Make sure that the file actually exists.
        try:
            with open(filename, 'rb'):
                pass
        except FileNotFoundError:
            return False

        # Parse file data byte by byte.
        # Refer to the separate handlers for documentation.
        with open(filename, 'rb') as io.in_file:
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

        print_done()

        terminal_width = os.get_terminal_size().columns

        print_cyan("-" * terminal_width)
        print_cyan(f"{map_data[map_key]['general']['name']}")
        print_cyan("-" * terminal_width)
        print_cyan(f"{map_data[map_key]['general']['description']}")
        print_cyan("-" * terminal_width)
        print("")

        return True

    def save_maps() -> None:
        # Check if a second map is open
        if map_data["map2"] is not None:
            filename1 = print_prompt("Enter a filename to save map 1")
            if filename1.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            save_map(filename1, "map1")
            filename2 = print_prompt("Enter a filename to save map 2")
            if filename2.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            save_map(filename2, "map2")
        else:
            filename1 = print_prompt("Enter a filename to save the map")
            if filename1.lower() in BACK_COMMANDS:
                print(ABORT_MSG)
                return
            save_map(filename1, "map1")

    def save_map(filename: str, map_key: str) -> None:
        # Make sure that the filename ends with ".h3m". For convenience,
        # users should be able to save maps without typing the extension.
        if len(filename) > 4:
            if filename[-4:] != ".h3m":
                filename += ".h3m"
        else: filename += ".h3m"

        print_action("Saving map...")

        # Save the map byte by byte.
        with open(filename, 'wb') as io.out_file:
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

    #############
    # EXECUTION #
    #############

    print("")
    print_cyan(f"##################################")
    print_cyan(f"##                              ##")
    print_cyan(f"##  H3 HotA Map Editor X v0.3   ##")
    print_cyan(f"##                              ##")
    print_cyan(f"##################################")
    print("")

    open_maps()

    while True:
        if not busy:
            command = print_prompt("Enter command")
            busy = True
        else:
            continue

        try:
            match command.split():
                case ["load"] | ["open"]:
                    open_maps()

                case ["save"]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        save_maps()

                case ["print", data_key]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.print_data(map_data[map_key], data_key)

                case ["export", filename]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.export_json(map_data[map_key], filename)

                case ["count"]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.count_objects(map_data[map_key]["object_data"])

                case ["swap"]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.swap_layers(
                            map_data[map_key]["terrain"],
                            map_data[map_key]["object_data"],
                            map_data[map_key]["player_specs"],
                            map_data[map_key]["general"]["is_two_level"],
                            map_data[map_key]["conditions"]
                        )

                case ["towns"]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.modify_towns(map_data[map_key]["object_data"])

                case ["minimap"]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.generate_minimap(
                            map_data[map_key]["general"],
                            map_data[map_key]["terrain"],
                            map_data[map_key]["object_data"],
                            map_data[map_key]["object_defs"]
                        )

                case ["events"]:
                    if map_data["map1"] is None:
                        print_error(ERROR_NO_MAP)
                    else:
                        map_key = get_map_key()
                        scripts.update_events()

                case ["help"] | ["h"]:
                    print_cyan(
                        "Basic commands:\n"
                        "   help | h\n"
                        "   load | open\n"
                        "   save\n"
                        "   /back | /return | /b | /r\n"
                        "   /exit | /quit | /e | /q\n"
                        "\n"
                        "Script commands:\n"
                        "   count\n"
                        "   events\n"
                        "   export <filename>.json\n"
                        "   minimap\n"
                        "   print <key>\n"
                        "   swap\n"
                        "   towns\n"
                        "\n"
                        "Data keys for 'print <key>':\n"
                        "   general\n"
                        "   player_specs\n"
                        "   conditions\n"
                        "   teams\n"
                        "   start_heroes\n"
                        "   ban_flags\n"
                        "   rumors\n"
                        "   hero_data\n"
                        "   terrain\n"
                        "   object_defs\n"
                        "   object_data\n"
                        "   events\n"
                        "   null_bytes\n"
                    )

                case [cmd]:
                    if cmd in BACK_COMMANDS:
                        print_error("Error: You are already at the main menu.")
                        print(ERROR_HELP)
                        continue
                    elif cmd in EXIT_COMMANDS:
                        exit()
                    else:
                        print_error("Error: Unrecognized command.")
                        print(ERROR_HELP)
        finally:
            busy = False

if __name__ == "__main__":
    main()
