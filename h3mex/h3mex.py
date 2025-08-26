#!/usr/bin/env python3

import os
import sys
import time

from src.common import Wait, exit, initialize, map_data, xprint
from src.edit import edit
from src.export import export
from src.h3m import h3m
from src.ui.menus import Menu
from src.view import view

# APPNAME = "H3 HotA Map Editor X"
# VERSION = "v0.3.1"

# class App

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "maps"))


def main(filename: str) -> None:
    if initialize():
        h3m.load(filename)
        while True:
            filename = map_data["filename"]
            keypress = xprint(menu=(Menu.MAIN["name"], Menu.MAIN["menus"][0]))
            match keypress:
                case "1":
                    view.menu()
                case "2":
                    edit.menu()
                case "3":
                    h3m.save(filename)
                case "4":
                    h3m.save()
                case "5":
                    export.menu()
                case "6":
                    h3m.load()
                case "7":
                    h3m.load(filename)
                case "0":
                    exit()
            time.sleep(Wait.TIC.value)
    else:
        exit()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    main(filename)
