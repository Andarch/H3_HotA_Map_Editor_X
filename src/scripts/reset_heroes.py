import data.objects as objects
import data.heroes as heroes
from ..common import *

def reset_heroes(player_specs: list, custom_heroes: list, hero_data: list, obj_data: list) -> bool:
    xprint(type=Text.ACTION, text="Resetting heroes...")

    skippable_heroes = determine_skippable_heroes(custom_heroes, obj_data)

    reset_player_specs(player_specs, skippable_heroes)
    reset_custom_heroes(custom_heroes, skippable_heroes)
    reset_hero_data(hero_data, skippable_heroes)
    reset_object_data(obj_data, skippable_heroes)

    xprint(type=Text.SPECIAL, text=DONE)
    return True

def determine_skippable_heroes(custom_heroes: list, obj_data: list) -> list:
    skippable_heroes = []
    for hero in custom_heroes:
        face_member = heroes.Portrait(hero["face"])
        face_name = face_member.name
        if face_name.startswith("Extra"):
            skippable_heroes.append(hero.get("id"))
    for obj in obj_data:
        if obj["type"] in (objects.ID.Hero, objects.ID.Prison):
            hero = obj["hero_data"]
            face_member = heroes.Portrait(hero["portrait"])
            face_name = face_member.name
            if face_name.startswith("Extra"):
                skippable_heroes.append(hero.get("id").value)
    return skippable_heroes

def reset_player_specs(player_specs: list, skippable_heroes: list) -> None:
    for player in player_specs:
        if player["starting_hero_id"] != heroes.ID.Default and player["starting_hero_id"] not in skippable_heroes:
            player["starting_hero_face"] = 255
            player["starting_hero_name"] = ""
        if player["available_heroes"]:
            for hero in player["available_heroes"]:
                if hero["id"] not in skippable_heroes:
                    hero["name"] = ""
    return

def reset_custom_heroes(custom_heroes: list, skippable_heroes: list) -> None:
    custom_heroes[:] = [hero for hero in custom_heroes if hero["id"] in skippable_heroes]
    return

def reset_hero_data(hero_data: list, skippable_heroes: list) -> None:
    for i, hero in enumerate(hero_data):
        if len(hero) == 3 or i in skippable_heroes:
            continue
        modified_hero = {
            "always_add_skills": hero.get("always_add_skills", True),
            "cannot_gain_xp": hero.get("cannot_gain_xp", False),
            "level": hero.get("level", 1)
        }
        hero_data[i] = modified_hero
    return

def reset_object_data(obj_data: list, skippable_heroes: list) -> None:
    for obj in obj_data:
        if obj["type"] in (objects.ID.Hero, objects.ID.Prison):
            hero = obj["hero_data"]
            if hero["id"] in skippable_heroes:
                continue
            hero["has_name"] = False
            hero["name"] = ""
            hero["has_portrait"] = False
            hero["portrait"] = 255
            hero["has_biography"] = False
            hero["biography"] = ""
            hero["gender"] = 255
    return