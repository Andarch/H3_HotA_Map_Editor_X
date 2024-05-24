#!/usr/bin/env python3

from sys  import argv
from gzip import open

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

#######################
## HANDLE USER INPUT ##
#######################

def main() -> None:
    global map_data    
    map_key = "map1"

    # Print some block of text as an introduction to the editor.
    # This should contain some common info, tips and maybe some news.
    print("\n##################################")
    print(  "##                              ##")
    print(  "##  h3_map_editor_plus.py v0.2  ##")
    print(  "##                              ##")
    print(  "##################################")

    # First argument passed when launching the editor can be a map file.
    #if len(argv) > 1:
    #    print("")
    #    open_map(argv[1])

    # open_maps()  # when not debugging    
    # DEBUGGING
    open_map("prism.h3m", "map1")
    minimap.main(map_data[map_key]["general"],
                 map_data[map_key]["terrain"],
                 map_data[map_key]["object_data"],
                 map_data[map_key]["object_defs"]
                )

    while True:
        command = input("\n[Enter command] > ")
        match command.split():
            case ["open"] | ["load"]: open_maps()
            case ["save"]: save_maps()

            case ["print", key] | ["show", key]:
                if map_data["map2"] is not None:
                    map_key = choose_map()                
                if map_key is not None:
                    if key in map_data[map_key]:
                        print(map_data[map_key][key])
                    else: print("\nUnrecognized key.")

            case ["export", filename]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if map_key is not None:
                    export.main(map_data[map_key], filename)

            case ["count"] | ["list"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if map_key is not None:
                    count.main(map_data[map_key]["object_data"])

            case ["guards"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if map_key is not None:
                    map_data[map_key]["object_data"] = guards.main(map_data[map_key]["object_data"])

            case ["swap"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if map_key is not None:
                    swap.main(
                        map_data[map_key]["terrain"],
                        map_data[map_key]["object_data"],
                        map_data[map_key]["player_specs"],
                        map_data[map_key]["general"]["is_two_level"],
                        map_data[map_key]["conditions"]
                )

            case ["towns"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if map_key is not None:
                    towns.main(map_data[map_key]["object_data"])

            case ["minimap"]:
                if map_data["map2"] is not None:
                    map_key = choose_map()
                if map_key is not None:
                    minimap.main(map_data[map_key]["general"],
                                 map_data[map_key]["terrain"],
                                 map_data[map_key]["object_data"],
                                 map_data[map_key]["object_defs"]
                    )

            case ["h"] | ["hlp"] | ['help']:
                print(
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
                    "guards\n"
                )

            case [cmd] if cmd in EXIT_COMMANDS: break
            
            case _: print("\nUnrecognized command.")

def choose_map() -> str:
    choice = input("\nWhich map do you want to edit? (1/2) ")

    if choice.lower() in EXIT_COMMANDS:
        print("\nAborting...")
        return

    return "map1" if choice == '1' else "map2"

################
## OPEN A MAP ##
################

def open_maps() -> None:
    num_maps = input("\nHow many maps do you want to open (1 or 2)? ")

    if num_maps.lower() in EXIT_COMMANDS:
        print("\nAborting...")
        return

    if num_maps == '1':
        map_data["map2"] = None
        filename1 = input("\nEnter the map filename: ")
        if filename1.lower() in EXIT_COMMANDS:
            print("\nAborting...")
            return
        open_map(filename1, "map1")
    elif num_maps == '2':
        filename1 = input("\nEnter the filename for map 1: ")
        if filename1.lower() in EXIT_COMMANDS:
            print("\nAborting...")
            return
        open_map(filename1, "map1")
        filename2 = input("\nEnter the filename for map 2: ")
        if filename2.lower() in EXIT_COMMANDS:
            print("\nAborting...")
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
    else:
        print("\nInvalid number of maps. Please enter 1 or 2.")
        return

def open_map(filename: str, map_key: str) -> None:
    global map_data

    # Make sure that the filename ends with ".h3m". For convenience,
    # users should be able to open maps without typing the extension.
    if filename[-4:] != ".h3m":
        filename += ".h3m"

    print(f"Reading map '{filename}' ...", end=' ')

    # Make sure that the file actually exists.
    try:
        with open(filename, 'rb'):
            pass
    except FileNotFoundError:
        print(f"ERROR - Could not find '{filename}'")
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

    print(f"\nDONE - '{map_data[map_key]['general']['name']}':")
    print(f"\n{map_data[map_key]['general']['description']}")

################
## SAVE A MAP ##
################

def save_maps() -> None:
    # Check if a second map is open
    if map_data["map2"] is not None:
        filename1 = input("\nEnter a filename to save map 1: ")
        save_map(filename1, "map1")
        filename2 = input("\nEnter a filename to save map 2: ")
        save_map(filename2, "map2")
    else:
        filename1 = input("\nEnter a filename to save the map: ")
        save_map(filename1, "map1")

def save_map(filename: str, map_key: str) -> None:
    global map_data

    # Make sure that the filename ends with ".h3m". For convenience,
    # users should be able to save maps without typing the extension.
    if len(filename) > 4:
        if filename[-4:] != ".h3m":
            filename += ".h3m"
    else: filename += ".h3m"

    print(f"Writing map '{filename}' ...", end=' ')

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

    print("DONE")

if __name__ == "__main__":
    main()
