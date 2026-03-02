from src.ui import header
from src.ui.menus import NumberedMenu

from ..common import Keypress
from . import (
    abandonedmines,
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
        keypress = NumberedMenu.display((NumberedMenu.EDIT["name"], NumberedMenu.EDIT["menus"][0]))
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
                    keypress = NumberedMenu.display((NumberedMenu.EDIT["name"], NumberedMenu.EDIT["menus"][2]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            towns.enable_spells()
                            towns.enable_buildings()
                        case "2":
                            towns.create_events
                        case "3":
                            towns.create_fourth_town_events
                        case "4":
                            towns.create_mega_town_events
                        case "5":
                            towns.change_ai_events
                        case "6":
                            towns.copy_events
                        case "7":
                            towns.copy_buildings
                        case "8":
                            towns.set_guards()
            case "4":
                while True:
                    keypress = NumberedMenu.display((NumberedMenu.EDIT["name"], NumberedMenu.EDIT["menus"][3]))
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
                    keypress = NumberedMenu.display((NumberedMenu.EDIT["name"], NumberedMenu.EDIT["menus"][4]))
                    if keypress == Keypress.ESC:
                        break

                    header.draw()

                    match keypress:
                        case "1":
                            monsters.set_random_monsters()
                        case "2":
                            monsters.set_monster_quantities()
                        case "3":
                            monsters.set_compliant_monster_values()
                        case "4":
                            monsters.set_random_monster_flee_values()
                        case "5":
                            monsters.make_compliant_monsters_not_grow()
                        case "6":
                            monsters.make_non_compliant_monsters_grow()
                        case "7":
                            monsters.increase_creature_stashes()
            case "6":
                while True:
                    keypress = NumberedMenu.display((NumberedMenu.EDIT["name"], NumberedMenu.EDIT["menus"][5]))
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
                        case "5":
                            treasures.modify_treasure_rewards()
            case "M":
                while True:
                    keypress = NumberedMenu.display((NumberedMenu.EDIT["name"], NumberedMenu.EDIT["menus"][1]))
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
                        case "8":
                            abandonedmines.modify_abandoned_mines()
                        case "M":
                            break
