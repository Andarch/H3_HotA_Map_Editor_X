from src.ui import header
from src.ui.menus import Menu
from src.ui.xprint import xprint

from ..common import Keypress
from . import eventobjects, fix, heroes, monsters, pandoras, towns, treasures


def menu() -> None:
    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][0]))
    if keypress == Keypress.ESC:
        return

    header.draw()

    match keypress:
        case "1":
            towns.edit(spells=True, buildings=True)
        case "2":
            towns.edit(events=True)
        case "3":
            towns.edit(human=True)
        case "4":
            heroes.reset()
        case "5":
            monsters.set_random_monsters()
        case "6":
            monsters.set_monster_values()
        case "7":
            monsters.set_compliant_monster_values()
        case "8":
            treasures.add_treasures()
        case "9":
            fix.fix_empty_contents()
        case "E":
            eventobjects.add_explorer_bonuses()
        case "P":
            pandoras.modify_pandoras()

    xprint()
