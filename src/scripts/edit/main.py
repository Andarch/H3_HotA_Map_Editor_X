import src.scripts.edit as edit
from src.scripts.edit.monster_values import set_compliant_monster_values
from src.scripts.edit.random_monsters import set_random_monsters

from ...common import KB, draw_header, xprint
from ...menus import Menu


def main() -> None:
    user_input = xprint(menu=Menu.EDIT.value)

    if user_input == KB.ESC.value:
        return

    draw_header()

    match user_input:
        case 1:
            edit.towns.modify(spells=True, buildings=True)
        case 2:
            edit.towns.modify(events=True)
        case 3:
            edit.heroes.reset()
        case 4:
            set_random_monsters()
        case 5:
            set_compliant_monster_values()

    xprint()
