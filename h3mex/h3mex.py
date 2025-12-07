#!/usr/bin/env python3

import ctypes
import os
import sys
import time

from src.common import App, Keypress, Wait, map_data
from src.edit import edit
from src.export import export
from src.file import file
from src.ui import header, ui
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.view import view


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    if filename:
        file.load(filename)
    else:
        filename = file.choose_map()
        file.load(filename) if filename else exit()

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
                filename = file.choose_map()
                if filename:
                    file.load(filename)
            case "7":
                file.load(filename)
            case Keypress.ESC:
                exit()


def exit(fast: bool = False) -> None:
    if not fast:
        header.draw()
        xprint(text="Exiting…")
        xprint()
        time.sleep(Wait.NORMAL.value)
        ui.uninitialize()
    sys.exit(0)


if __name__ == "__main__":
    ui.initialize()

    mutex_name = App.NAME.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if ctypes.windll.kernel32.GetLastError() == 183:
        print("Another instance of the program is already running.")
        time.sleep(Wait.NORMAL.value)
        exit(fast=True)

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "maps"))
    main()
