#!/usr/bin/env python3

from src import *

#########################
# GLOBAL INITIALIZATION #
#########################

# valid_files = []

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
            success = False
            while not success:
                input = xprint(menu=menus["start"])
                if input == "esc": continue
                match input:
                    case 1: success = io.open_maps()
                    case 2: exit()
                time.sleep(SLEEP.TIC)

            while True:
                success = False
                while not success:
                    input = xprint(menu=menus["main"])
                    if input == "esc": continue
                    xprint()
                    match input:
                        case 1: success = io.open_maps()
                        case 2: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 3: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 4: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 5: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 6: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 7: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 8: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 9: xprint(type=MSG.ERROR, text="Not yet functional.")
                        case 0: exit()
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
