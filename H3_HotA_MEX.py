#!/usr/bin/env python3

import os
from src import *


os.chdir('maps')


def main() -> None:
    if(initialize()):
        try:
            io.load_map()

            # Main menu
            while True:
                success = False
                while not success:
                    input = xprint(menu=Menu.MAIN.value)
                    if input == KB.ESC.value: continue
                    xprint()

                    success = False

                    match input:
                        case 1: success = scripts.print_data(map_data)
                        case 2: success = scripts.edit_data(map_data)
                        case 3: success = scripts.export_excel(map_data)
                        case 4: success = scripts.export_json(map_data)
                        case 5: success = scripts.generate_minimap(
                                    map_data["filename"],
                                    map_data["map_specs"],
                                    map_data["terrain"],
                                    map_data["object_data"],
                                    map_data["object_defs"]
                                )
                        case 6: io.load_map(quickload=True)
                        case 7: io.save_map(quicksave=True)
                        case 8: io.load_map()
                        case 9: io.save_map()
                        case 0: exit()
                    time.sleep(Sleep.TIC.value)
        except KeyboardInterrupt:
            exit()
    else:
        exit()


if __name__ == "__main__":
    main()
