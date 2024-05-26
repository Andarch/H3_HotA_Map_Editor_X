#!/usr/bin/env python3

from sys  import argv
from gzip import open

import time
import os

from src.constants import *
from src.scripts import count
from src.scripts import export
from src.scripts import guards
from src.scripts import minimap
from src.scripts import swap
from src.scripts import towns

import src.file_io as io
import src.handler_01_general            as h1
import src.handler_02_players_and_teams  as h2
import src.handler_03_conditions         as h3
import src.handler_04_heroes             as h4
import src.handler_05_additional_flags   as h5
import src.handler_06_rumors_and_events  as h6
import src.handler_07_terrain            as h7
import src.handler_08_objects            as h8

EXIT_COMMANDS = ['q', 'exit', 'quit']

map_data = {
    "map1": {
        "general"     : {}, # General tab in Map Specifications
        "player_specs": [], # ...
        "conditions"  : {}, # Special Victory and Loss Conditions
        "teams"       : {}, # ...
        "start_heroes": {}, # Available starting heroes
        "ban_flags"   : {}, # Available artifacts, spells, and skills
        "rumors"      : [], # ...
        "hero_data"   : [], # Custom hero details (name, bio, portrait, etc.)
        "terrain"     : [], # ...
        "object_defs" : [], # Object definitions (sprite, type, squares, etc.)
        "object_data" : [], # Object details (messages, guards, quests, etc.)
        "events"      : [], # ...
        "null_bytes"  : b'' # All maps end with some null bytes
    },
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
    map_data = {map_key: {}}
    busy = False
    yellow = "\033[33m"
    red = "\033[31m"
    cyan = "\033[36m"
    green = "\033[32m"
    white = "\033[37m"
    color_reset = "\033[0m"

    # First argument passed when launching the editor can be a map file.
    #if len(argv) > 1:
    #    print("")
    #    open_map(argv[1])

    ####################
    # HELPER FUNCTIONS #
    ####################

    def print_cyan(text: str) -> None:
        print(f"{cyan}{text}{color_reset}")

    def print_prompt(prompt: str) -> str:
        return input(f"\n{yellow}[{prompt}] > {color_reset}")

    def print_flush(text: str) -> None:
        print(f"{white}{text}{color_reset}", end=" ", flush=True)

    def print_done() -> None:
        print(f"{green}DONE{color_reset}")
        time.sleep(SLEEP_TIME)

    def print_error(error: str) -> None:
        print(f"{red}{error}{color_reset}")
        time.sleep(SLEEP_TIME)

    def choose_map() -> str:
        choice = print_prompt(f"Enter the map number to edit")
        if choice.lower() in EXIT_COMMANDS:
            print("Aborting...")
            return
        return "map1" if choice == '1' else "map2"

    def open_maps() -> None:
        while True:
            num_maps = print_prompt(f"Enter the number of maps to open")

            if num_maps.lower() in EXIT_COMMANDS:
                print("Aborting...")
                return

            if num_maps == '1':
                map_data["map2"] = None
                filename1 = print_prompt("Enter the map filename")
                if filename1.lower() in EXIT_COMMANDS:
                    print("Aborting...")
                    return
                open_map(filename1, "map1")
                break
            elif num_maps == '2':
                filename1 = print_prompt("Enter the filename for map 1")
                if filename1.lower() in EXIT_COMMANDS:
                    print("Aborting...")
                    return
                open_map(filename1, "map1")
                filename2 = print_prompt("Enter the filename for map 2")
                if filename2.lower() in EXIT_COMMANDS:
                    print("Aborting...")
                    return
                map_data["map2"] = {
                    "general"     : {},
                    "player_specs": [],
                    "conditions"  : {},
                    "teams"       : {},
                    "start_heroes": {},
                    "ban_flags"   : {},
                    "rumors"      : [],
                    "hero_data"   : [],
                    "terrain"     : [],
                    "object_defs" : [],
                    "object_data" : [],
                    "events"      : [],
                    "null_bytes"  : b''
                }
                open_map(filename2, "map2")
                break
            else:
                print_error("Error: Can only load 1 or 2 maps.")
        return

    def open_map(filename: str, map_key: str) -> None:
        # Make sure that the filename ends with ".h3m". For convenience,
        # users should be able to open maps without typing the extension.
        if filename[-4:] != ".h3m":
            filename += ".h3m"

        print_flush("Loading map...")
        time.sleep(SLEEP_TIME)

        # Make sure that the file actually exists.
        try:
            with open(filename, 'rb'):
                pass
        except FileNotFoundError:
            print_error(f"ERROR: Could not find '{filename}'.")
            return

        # Parse file data byte by byte.
        # Refer to the separate handlers for documentation.
        with open(filename, 'rb') as io.in_file:
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

        print("")
        print_cyan("-" * terminal_width)
        print_cyan(f"{map_data[map_key]['general']['name']}")
        print_cyan("-" * terminal_width)
        print_cyan(f"{map_data[map_key]['general']['description']}")
        print_cyan("-" * terminal_width)

    def save_maps() -> None:
        # Check if a second map is open
        if map_data["map2"] is not None:
            filename1 = print_prompt("Enter a filename to save map 1")
            save_map(filename1, "map1")
            filename2 = print_prompt("Enter a filename to save map 2")
            save_map(filename2, "map2")
        else:
            filename1 = print_prompt("Enter a filename to save the map")
            save_map(filename1, "map1")

    def save_map(filename: str, map_key: str) -> None:
        # Make sure that the filename ends with ".h3m". For convenience,
        # users should be able to save maps without typing the extension.
        if len(filename) > 4:
            if filename[-4:] != ".h3m":
                filename += ".h3m"
        else: filename += ".h3m"

        print_flush("Saving map...")
        time.sleep(SLEEP_TIME)

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
    print_cyan(f"##  h3_map_editor_plus.py v0.3  ##")
    print_cyan(f"##                              ##")
    print_cyan(f"##################################")

    open_maps()

    while True:
        if not busy:
            command = print_prompt("Enter command")
            busy = True
        else:
            continue

        match command.split():
            case ["open"] | ["load"]:
                open_maps()
                busy = False

            case ["save"]:
                save_maps()
                busy = False

            case ["print", data_key] | ["show", data_key]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if data_key in map_data[map_key]:
                    print_cyan(map_data[map_key][data_key])
                else:
                    print_error("Error: Unrecognized data key.")
                busy = False

            case ["export", filename]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                export.main(map_data[map_key], filename)
                busy = False

            case ["count"] | ["list"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                count.main(map_data[map_key]["object_data"])
                busy = False

            case ["guards"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                guards.main(map_data[map_key]["object_data"])
                busy = False

            case ["swap"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                swap.main(
                    map_data[map_key]["terrain"],
                    map_data[map_key]["object_data"],
                    map_data[map_key]["player_specs"],
                    map_data[map_key]["general"]["is_two_level"],
                    map_data[map_key]["conditions"]
                )
                busy = False

            case ["towns"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                towns.main(map_data[map_key]["object_data"])
                busy = False

            case ["minimap"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                minimap.main(
                    map_data[map_key]["general"],
                    map_data[map_key]["terrain"],
                    map_data[map_key]["object_data"],
                    map_data[map_key]["object_defs"]
                )
                busy = False

            case ["h"] | ["hlp"] | ['help']:
                print_cyan(
                    "\n"
                    "*COMMANDS*\n"
                    "open | load\n"
                    "save\n"
                    "print\n"
                    "export\n"
                    "h | hlp | help\n"
                    "q | quit | exit\n"
                    "\n"
                    "*VALID KEYS FOR PRINT*\n"
                    "general\n"
                    "player_specs\n"
                    "conditions\n"
                    "teams\n"
                    "start_heroes\n"
                    "ban_flags\n"
                    "rumors\n"
                    "hero_data\n"
                    "terrain\n"
                    "object_defs\n"
                    "object_data\n"
                    "events\n"
                    "null_bytes\n"
                    "\n"
                    "*SCRIPTS*\n"
                    "minimap\n"
                    "towns\n"
                    "swap\n"
                    "count | list\n"
                    "guards"
                )
                busy = False

            case [cmd]:
                if cmd in EXIT_COMMANDS:
                    print(f"{color_reset}")
                    break
                else:
                    print_error("Error: Unrecognized command.")
                    time.sleep(SLEEP_TIME)
                    busy = False

if __name__ == "__main__":
    main()
