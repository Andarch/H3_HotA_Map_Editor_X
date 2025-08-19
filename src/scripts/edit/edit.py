from ...common import KB, draw_header, xprint
from ...menus import Menu
from . import heroes, towns
from .monster_values import set_compliant_monster_values
from .random_monsters import set_random_monsters


def main() -> None:
    keypress = xprint(menu=Menu.EDIT.value)
    if keypress == KB.ESC.value:
        return

    draw_header()

    match keypress:
        case 1:
            towns.modify(spells=True, buildings=True)
        case 2:
            towns.modify(events=True)
        case 3:
            heroes.reset()
        case 4:
            set_random_monsters()
        case 5:
            set_compliant_monster_values()

    xprint()
