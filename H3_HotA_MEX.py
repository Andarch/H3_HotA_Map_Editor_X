#!/usr/bin/env python3

import os
import sys
import time

import src.file_io as io
from src.common import Sleep, exit, initialize, map_data, xprint
from src.menus import Menu
from src.scripts.edit import edit
from src.scripts.export import export
from src.scripts.view import view

os.chdir("maps")


def main(filename: str) -> None:
    if initialize():
        io.load_map(filename)
        while True:
            keypress = xprint(menu=Menu.MAIN.value)
            match keypress:
                case 1:
                    view.main()
                case 2:
                    edit.main()
                case 3:
                    io.save_map(map_data["filename"])
                case 4:
                    io.save_map()
                case 5:
                    export.main()
                case 6:
                    io.load_map()
                case 7:
                    io.load_map(map_data["filename"])
                case 0:
                    exit()
            time.sleep(Sleep.TIC.value)
    else:
        exit()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    main(filename)
