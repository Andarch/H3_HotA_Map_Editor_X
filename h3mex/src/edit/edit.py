from src.ui.menus import Menu

from ..common import Keypress, draw_header, xprint
from .scripts import fix_empty_contents, heroes, monster_values, random_monsters, towns


def menu() -> None:
    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][0]))
    if keypress == Keypress.ESC:
        return

    draw_header()

    match keypress:
        case "1":
            towns.edit(spells=True, buildings=True)
        case "2":
            towns.edit(events=True)
        case "3":
            heroes.reset()
        case "4":
            random_monsters.set_random_monsters()
        case "5":
            monster_values.set_compliant_monster_values()
        case "6":
            fix_empty_contents.fix_empty_contents()

    xprint()
