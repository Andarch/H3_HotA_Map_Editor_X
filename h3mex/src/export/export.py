from src.minimap import minimap
from src.ui import header
from src.ui.menus import Menu
from src.ui.xprint import xprint

from ..common import Keypress
from .excel_ import excel_
from .json_ import json_


def menu() -> None:
    keypress = xprint(menu=(Menu.EXPORT["name"], Menu.EXPORT["menus"][0]))
    if keypress == Keypress.ESC:
        return

    header.draw()

    match keypress:
        case "1":
            excel_.export()
        case "2":
            json_.export("1")
        case "3":
            json_.export("2")
        case "4":
            json_.export("3")
        case "5":
            json_.export("4")
        case "6":
            minimap.run("export")

    xprint()
