from ..common import *
from ..menus import *
from src import scripts
from .edit import *


def edit_data() -> None:
    user_input = xprint(menu=Menu.EDIT.value)

    if user_input == KB.ESC.value:
        return

    draw_header()

    match user_input:
        case 1: scripts.modify_towns()
        case 2: scripts.reset_heroes()
        case 3: scripts.edit.list_unreachable_tiles()
        case 4: scripts.edit.set_random_monsters()
        case 5: scripts.edit.set_compliant_monster_values()

    xprint()
