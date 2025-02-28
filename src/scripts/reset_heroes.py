import data.objects as objects
import data.heroes as heroes
from ..common import *

def reset_heroes(player_specs: dict, starting_heroes: dict, hero_data: dict, obj_data: dict) -> bool:
    xprint(type=Text.ACTION, text="Resetting heroes...")

    reset_player_specs(player_specs)
    reset_starting_heroes(starting_heroes)
    reset_hero_data(hero_data)
    reset_obj_data(obj_data)

    xprint(type=Text.SPECIAL, text=DONE)
    return True

def reset_player_specs(player_specs: dict) -> None:
    for player in player_specs:
        if player["starting_hero_id"] != heroes.ID.Default:
            player["starting_hero_face"] = 255
            player["starting_hero_name"] = ""
        if "available_heroes" in player:
            for hero in player["available_heroes"]:
                hero["name"] = ""
    return

def reset_starting_heroes(starting_heroes: dict) -> None:
    starting_heroes["custom_heroes"] = []
    return

def reset_hero_data(hero_data: dict) -> None:
    for i, hero in enumerate(hero_data):
        if len(hero) == 3:
            continue
        new_hero = {
            "always_add_skills": hero.get("always_add_skills", True),
            "cannot_gain_xp": hero.get("cannot_gain_xp", False),
            "level": hero.get("level", 1)
        }
        hero_data[i] = new_hero
    return

def reset_obj_data(obj_data: dict) -> None:
    for obj in obj_data:
        if obj["type"] in (objects.ID.Hero, objects.ID.Prison):
            hero = obj["hero_data"]
            hero["has_name"] = False
            hero["name"] = ""
            hero["has_portrait"] = False
            hero["portrait"] = 255
            hero["has_biography"] = False
            hero["biography"] = ""
            hero["gender"] = 255
    return