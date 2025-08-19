from ...common import KB, draw_header, xprint
from ...menus import Menu
from . import json, minimap
from .excel import excel


def main() -> None:
    keypress = xprint(menu=Menu.EXPORT.value)
    if keypress == KB.ESC.value:
        return

    draw_header()

    match keypress:
        case 1:
            excel.export()
        case 2:
            json.export(1)
        case 3:
            json.export(2)
        case 4:
            json.export(3)
        case 5:
            json.export(4)
        case 6:
            minimap.export(1)
        case 7:
            minimap.export(2)

    xprint()
