#!/usr/bin/env python3

import ctypes
import os
import sys

from src.common import App, Cursor, Keypress, TextType, map_data
from src.edit import edit
from src.export import export
from src.file import file
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import exit
from src.view import view

os.system("title H3 HotA Map Editor X")
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "maps"))


def main(filename: str) -> None:
    if _initialize():
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
    else:
        exit()


def _initialize():
    print(Cursor.HIDE, end="", flush=True)
    mutex_name = App.NAME.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if ctypes.windll.kernel32.GetLastError() != 183:
        return True
    else:
        xprint(type=TextType.ERROR, text="Another instance of the editor is already running.")
        return False


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    main(filename)
