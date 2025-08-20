import src.core.heroes as heroes
import src.core.objects as objects

from ...common import DONE, Text, map_data, xprint


def reset() -> None:
    xprint(type=Text.ACTION, text="Resetting identity details for all non-special heroes...")

    special_heroes = _get_special_heroes()

    _reset_player_specs(special_heroes)
    _reset_custom_heroes(special_heroes)
    _reset_hero_data(special_heroes)
    _reset_object_data(special_heroes)

    xprint(type=Text.SPECIAL, text=DONE)


def _get_special_heroes() -> list:
    special_heroes = []

    for hero in map_data["starting_heroes"]["custom_heroes"]:
        face_member = heroes.Portrait(hero["face"])
        face_name = face_member.name

        if face_name.startswith("Extra"):
            special_heroes.append(hero.get("id"))

    for obj in map_data["object_data"]:
        if obj["id"] in (objects.ID.Hero, objects.ID.Prison):
            hero = obj["hero_data"]
            face_member = heroes.Portrait(hero["portrait_id"])
            face_name = face_member.name

            if face_name.startswith("Extra"):
                special_heroes.append(hero.get("id"))

    return special_heroes


def _reset_player_specs(special_heroes: list) -> None:
    for player in map_data["player_specs"]:
        if player["starting_hero_id"] != heroes.ID.Default and player["starting_hero_id"] not in special_heroes:
            player["starting_hero_face"] = 255
            player["starting_hero_name"] = ""

        if player["available_heroes"]:
            for hero in player["available_heroes"]:
                if hero["id"] not in special_heroes:
                    hero["custom_name"] = ""


def _reset_custom_heroes(special_heroes: list) -> None:
    map_data["starting_heroes"]["custom_heroes"][:] = [
        hero for hero in map_data["starting_heroes"]["custom_heroes"] if hero["id"] in special_heroes
    ]


def _reset_hero_data(special_heroes: list) -> None:
    for i, hero in enumerate(map_data["hero_data"]):
        if len(hero) == 3 or i in special_heroes:
            continue

        modified_hero = {
            "add_skills": hero.get("add_skills", True),
            "cannot_gain_xp": hero.get("cannot_gain_xp", False),
            "level": hero.get("level", 1),
        }

        map_data["hero_data"][i] = modified_hero


def _reset_object_data(special_heroes: list) -> None:
    for obj in map_data["object_data"]:
        if obj["id"] in (objects.ID.Hero, objects.ID.Prison):
            hero = obj["hero_data"]

            if hero["id"] in special_heroes:
                continue

            hero["has_custom_name"] = False
            hero["custom_name"] = ""
            hero["has_portrait"] = False
            hero["portrait_id"] = 255
            hero["has_biography"] = False
            hero["biography"] = ""
            hero["gender"] = 255
