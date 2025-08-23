from src.ui.menus import Menu

from ..common import KB, draw_header, xprint
from .scripts import heroes, monster_values, random_monsters, towns


def menu() -> None:
    keypress = xprint(menu=Menu.EDIT.value)
    if keypress == KB.ESC:
        return

    draw_header()

    match keypress:
        case 1:
            towns.edit(spells=True, buildings=True)
        case 2:
            towns.edit(events=True)
        case 3:
            heroes.reset()
        case 4:
            random_monsters.set_random_monsters()
        case 5:
            monster_values.set_compliant_monster_values()

    xprint()
