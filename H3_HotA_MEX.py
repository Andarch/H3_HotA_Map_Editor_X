#!/usr/bin/env python3

import os
import sys
import time

import src.file_io as io
import src.scripts.edit.main as edit
import src.scripts.info.main as info
from src.common import Sleep, exit, initialize, map_data, xprint
from src.menus import Menu
from src.scripts.export_excel import export_excel
from src.scripts.export_json import export_json
from src.scripts.generate_minimap import generate_minimap

os.chdir("maps")


def main(filename: str) -> None:
    if initialize():
        io.load_map(filename)
        while True:
            keypress = xprint(menu=Menu.MAIN.value)
            match keypress:
                case 1:
                    info.main()
                case 2:
                    edit.main()
                case 3:
                    export_excel()
                case 4:
                    export_json()
                case 5:
                    generate_minimap(
                        map_data["filename"],
                        map_data["map_specs"],
                        map_data["terrain"],
                        map_data["object_data"],
                        map_data["object_defs"],
                    )
                case 6:
                    io.load_map(map_data["filename"])
                case 7:
                    io.save_map(quicksave=True)
                case 8:
                    io.load_map()
                case 9:
                    io.save_map()
                case 0:
                    exit()
            time.sleep(Sleep.TIC.value)
    else:
        exit()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    main(filename)
