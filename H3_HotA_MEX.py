#!/usr/bin/env python3

import os
import time

import src.file_io as io
from src.common import KB, Sleep, initialize, map_data, xprint
from src.menus import Menu
from src.scripts.edit_data import edit_data
from src.scripts.export_excel import export_excel
from src.scripts.export_json import export_json
from src.scripts.generate_minimap import generate_minimap
from src.scripts.print_data import print_data

os.chdir("maps")


def main() -> None:
    if initialize():
        try:
            io.load_map()

            # Main menu
            while True:
                user_input = xprint(menu=Menu.MAIN.value)

                if user_input == KB.ESC.value:
                    continue

                match user_input:
                    case 1:
                        print_data()
                    case 2:
                        edit_data()
                    case 3:
                        export_excel(map_data)
                    case 4:
                        export_json(map_data)
                    case 5:
                        generate_minimap(
                            map_data["filename"],
                            map_data["map_specs"],
                            map_data["terrain"],
                            map_data["object_data"],
                            map_data["object_defs"],
                        )
                    case 6:
                        io.load_map(quickload=True)
                    case 7:
                        io.save_map(quicksave=True)
                    case 8:
                        io.load_map()
                    case 9:
                        io.save_map()
                    case 0:
                        exit()
                time.sleep(Sleep.TIC.value)
        except KeyboardInterrupt:
            exit()
    else:
        exit()


if __name__ == "__main__":
    main()
