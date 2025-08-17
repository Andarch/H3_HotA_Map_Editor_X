import src.scripts.edit as edit
from src.scripts.edit.monster_values import set_compliant_monster_values
from src.scripts.edit.random_monsters import set_random_monsters
from src.scripts.edit.unreachable_tiles import list_unreachable_tiles

from ..common import KB, draw_header, xprint
from ..menus import Menu


def edit_data() -> None:
    user_input = xprint(menu=Menu.EDIT.value)

    if user_input == KB.ESC.value:
        return

    draw_header()

    match user_input:
        case 1:
            edit.towns.modify(events=False)
        case 2:
            edit.towns.modify(events=True)
        case 3:
            edit.heroes.modify()
        case 4:
            list_unreachable_tiles()
        case 5:
            set_random_monsters()
        case 6:
            set_compliant_monster_values()

    xprint()
