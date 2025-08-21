from ...core.menus import Menu
from ..common import KB, draw_header, xprint
from . import excel_, json_, minimap


def menu() -> None:
    keypress = xprint(menu=Menu.EXPORT.value)
    if keypress == KB.ESC.value:
        return

    draw_header()

    match keypress:
        case 1:
            excel_.export()
        case 2:
            json_.export(1)
        case 3:
            json_.export(2)
        case 4:
            json_.export(3)
        case 5:
            json_.export(4)
        case 6:
            minimap.export(1)
        case 7:
            minimap.export(2)

    xprint()
