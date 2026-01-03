from src.ui import header
from src.ui.menus import Menu
from src.ui.xprint import xprint

from ..common import Keypress
from . import (
    eventobjects,
    garrisons,
    heroes,
    monsters,
    pandoras,
    remove,
    replace,
    seershuts,
    towns,
    treasures,
)


def menu() -> None:
    while True:
        keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][0]))
        if keypress == Keypress.ESC:
            return

        header.draw()

        match keypress:
            case "1":
                replace.replace_objects()
            case "2":
                remove.remove_objects()
            case "3":
                while True:
                    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][2]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            towns.edit(spells=True, buildings=True)
                        case "2":
                            towns.edit(add_events=True)
                        case "3":
                            towns.edit(fourth_town=True)
                        case "4":
                            towns.edit(mega_town=True)
                        case "5":
                            towns.edit(human=True)
                        case "6":
                            towns.edit(copy_events=True)
                        case "7":
                            towns.edit(copy_buildings=True)
            case "4":
                while True:
                    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][3]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            heroes.reset()
                        case "2":
                            heroes.move_heroes_from_towns_to_map()
                        case "3":
                            heroes.swap_hero_indexes()
            case "5":
                while True:
                    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][4]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            monsters.set_random_monsters()
                        case "2":
                            monsters.set_monster_values()
                        case "3":
                            monsters.set_compliant_monster_values()
            case "6":
                while True:
                    keypress = xprint(menu=(Menu.EDIT["name"], Menu.EDIT["menus"][5]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            treasures.add_treasures()
                        case "2":
                            treasures.fix_empty_contents()
                        case "3":
                            treasures.add_scholars()
                        case "4":
                            treasures.remove_sea_treasures()
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
                            seershuts.modify_seers_huts()
                        case "6":
                            garrisons.copy_garrison_guards()
                        case "7":
                            garrisons.fill_empty_garrison_guards()
                        case "M":
                            break

        # xprint()
