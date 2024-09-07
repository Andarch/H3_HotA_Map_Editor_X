#!/usr/bin/env python3

import sys
# from enum import Enum
from src import *

# HELP_COMMANDS = ["help", "h"]
# BACK_COMMANDS = ["/back", "/return", "/b", "/r"]
# EXIT_COMMANDS = ["/exit", "/quit", "/e", "/q"]
ERROR_NO_MAP = "Error: No map loaded."
# ERROR_HELP = (f"For help, enter one of these commands:\n{CLR.CYAN}\t{"\n\t".join(HELP_COMMANDS)}\n{CLR.RESET}"
#               f"To exit, enter one of these commands:\n{CLR.CYAN}\t{"\n\t".join(EXIT_COMMANDS)}\n{CLR.RESET}")
# ABORT_MSG = "Operation aborted.\n"
EXIT_MSG = "Exiting program..."

#########################
# GLOBAL INITIALIZATION #
#########################

menu_start = [
    "OPEN",
    "QUIT"
]

menu_open = [
    "Open 1 map",
    "Open 2 maps"
]

menus = {
    "start": menu_start,
    "open" : menu_open
}

valid_files = []

map_data = {
    "Map 1": None,
    "Map 2": None
}

#################
# MAIN FUNCTION #
#################

def main() -> None:

    ####################
    # HELPER FUNCTIONS #
    ####################

    # def get_map_key() -> str:
    #     if map_data["Map 2"] is None:
    #         return "Map 1"

    #     print("Select a map:")
    #     print_cyan(f"   1. {map_data["Map 1"]["filename"]}")
    #     print_cyan(f"   2. {map_data["Map 2"]["filename"]}")
    #     print()
    #     choice = detect_key_press("Choose a map", "12")
    #     return "Map 1" if choice == "1" else "Map 2"

    def exit() -> None:
        xprint()
        xprint(text = EXIT_MSG)
        time.sleep(SLEEP.NORMAL)
        xprint(text = CLR.RESET)
        sys.exit(0)

    ##################
    # INITIALIZATION #
    ##################

    map_key = "Map 1"
    busy = False

    #############
    # EXECUTION #
    #############

    if(initialize()):
        try:
            while True:
                key_press = menu_prompt(menus["start"])
                match key_press:
                    case "1": io.open_map_prompts()
                    case "2": exit()
                time.sleep(SLEEP.TIC)
        except KeyboardInterrupt:
            exit()
    else:
        exit()

    # while True:
    #     try:
    #         match command.split():
    #             case ["load"] | ["open"]:
    #                 open_map_prompts()

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
