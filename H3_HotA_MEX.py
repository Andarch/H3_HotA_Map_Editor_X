#!/usr/bin/env python3

import os
from src import *

os.chdir('maps')

def main() -> None:
    map_key = "Map 1"

    if(initialize()):
        try:
            io.load_maps(1)

            # Main menu
            while True:
                success = False
                while not success:
                    input = xprint(menu=Menu.MAIN.value)
                    if input == KB.ESC.value: continue
                    xprint()

                    success = False
                    match input:
                        case 1:
                            map_key = get_map_key()
                            success = scripts.print_data(map_data[map_key])
                        case 2:
                            map_key = get_map_key()
                            success = scripts.edit_data(map_data[map_key])
                        case 3:
                            map_key = get_map_key()
                            success = scripts.export_excel(map_data[map_key])
                        case 4:
                            map_key = get_map_key()
                            success = scripts.export_json(map_data[map_key])
                        case 5:
                            map_key = get_map_key()
                            success = scripts.generate_minimap(
                                map_data[map_key]["map_specs"],
                                map_data[map_key]["terrain"],
                                map_data[map_key]["object_data"],
                                map_data[map_key]["object_defs"]
                            )
                        case 6: xprint(type=Text.ERROR, text="Not yet functional.")
                        case 7: xprint(type=Text.ERROR, text="Not yet functional.")
                        case 8: io.load_maps(1)
                        case 9: io.save_maps()
                        case 0: exit()
                    time.sleep(Sleep.TIC.value)
        except KeyboardInterrupt:
            exit()
    else:
        exit()

if __name__ == "__main__":
    main()
