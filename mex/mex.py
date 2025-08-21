#!/usr/bin/env python3

import os
import sys
import time

from core.menus import Menu
from src import file_io as io
from src.common import Sleep, exit, initialize, map_data, xprint
from src.edit import edit
from src.export import export
from src.view import view

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "maps"))


def main(filename: str) -> None:
    if initialize():
        io.load_map(filename)
        while True:
            keypress = xprint(menu=(Menu.MAIN["name"], Menu.MAIN["menus"][0]))
            match keypress:
                case "1":
                    view.menu()
                case "2":
                    edit.menu()
                case "3":
                    io.save_map(map_data["filename"])
                case "4":
                    io.save_map()
                case "5":
                    export.menu()
                case "6":
                    io.load_map()
                case "7":
                    io.load_map(map_data["filename"])
                case "0":
                    exit()
            time.sleep(Sleep.TIC.value)
    else:
        exit()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    main(filename)
