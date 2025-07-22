from edit.modify_towns import modify_towns
from edit.monster_values import set_compliant_monster_values
from edit.random_monsters import set_random_monsters
from edit.reset_heroes import reset_heroes
from edit.unreachable_tiles import list_unreachable_tiles

from ..common import KB, draw_header, xprint
from ..menus import Menu


def edit_data() -> None:
    user_input = xprint(menu=Menu.EDIT.value)

    if user_input == KB.ESC.value:
        return

    draw_header()

    match user_input:
        case 1:
            modify_towns()
        case 2:
            reset_heroes()
        case 3:
            list_unreachable_tiles()
        case 4:
            set_random_monsters()
        case 5:
            set_compliant_monster_values()

    xprint()
