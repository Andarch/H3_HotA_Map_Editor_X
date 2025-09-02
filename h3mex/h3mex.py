#!/usr/bin/env python3

import os
import sys

from src.common import exit, initialize, map_data, xprint
from src.edit import edit
from src.export import export
from src.file import file
from src.ui.menus import Menu
from src.view import view

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "maps"))


def main(filename: str) -> None:
    if initialize():
        file.load(filename)
        while True:
            filename = map_data["filename"]
            keypress = xprint(menu=(Menu.MAIN["name"], Menu.MAIN["menus"][0]))
            match keypress:
                case "1":
                    view.menu()
                case "2":
                    edit.menu()
                case "3":
                    file.save(filename)
                case "4":
                    file.save()
                case "5":
                    export.menu()
                case "6":
                    file.load()
                case "7":
                    file.load(filename)
                case "0":
                    exit()
    else:
        exit()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    main(filename)
