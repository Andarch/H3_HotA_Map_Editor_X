from src.ui import header
from src.ui.menus import Menu
from src.ui.xprint import xprint

from ..common import Keypress
from . import eventobjects, fix, garrisons, heroes, monsters, pandoras, towns, treasures


def menu() -> None:
    while True:
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
            case "M":
                while True:
                    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][1]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            eventobjects.add_explorer_bonuses()
                        case "2":
                            eventobjects.delete_explorer_bonuses()
                        case "3":
                            eventobjects.modify_ai_main_hero_boost()
                        case "4":
                            pandoras.modify_pandoras()
                        case "5":
                            garrisons.copy_garrison_guards()
                        case "6":
                            garrisons.fill_empty_garrison_guards()
                        case "M":
                            break

        # xprint()
