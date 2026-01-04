from src.common import TextType, map_data
from src.defs import heroes, objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def reset() -> None:
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

    xprint(type=TextType.ACTION, text="Resetting identity details for all non-special heroes…")

    special_heroes = _get_special_heroes()

    _reset_player_specs(special_heroes)
    _reset_custom_heroes(special_heroes)
    _reset_hero_data(special_heroes)
    _reset_object_data(special_heroes)

    xprint(type=TextType.DONE)


def move_heroes_from_towns_to_map() -> None:
    xprint(type=TextType.ACTION, text="Moving heroes from towns to map…")

    heroes = {}
    moved_count = 0
    object_data = map_data["object_data"]

    names_of_interest = {"Morgoth", "Jezebel", "Ba'al", "Olokun", "Nerus"}

    for i in range(len(object_data) - 1, -1, -1):  # from last to first
        obj = object_data[i]
        if obj["id"] == objects.ID.Hero and obj["hero_data"]["name"] in names_of_interest:
            name = obj["hero_data"]["name"]
            heroes[name] = obj
            object_data.pop(i)  # safe when going backwards

    for i, obj in enumerate(object_data):
        if obj["id"] == objects.ID.Ocean_Bottle and obj["message"] in heroes:
            hero = heroes[obj["message"]]

            hero["coords"] = [obj["coords"][0] + 1, obj["coords"][1], obj["coords"][2]]
            hero["coords_offset"] = obj["coords_offset"]
            hero["zone_type"] = obj["zone_type"]
            hero["zone_player"] = obj["zone_player"]

            object_data[i] = hero
            moved_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Moved {moved_count} heroes.",
    )
    wait_for_keypress()


def swap_hero_indexes():
    HERO1 = "Morgoth"
    HERO2 = "Ner'zhul"
    xprint(type=TextType.ACTION, text=f"Swapping {HERO1} and {HERO2}…")

    object_data = map_data["object_data"]

    hero1_index = None
    hero2_index = None

    for i, obj in enumerate(object_data):
        if obj.get("hero_data", {}).get("name") == HERO1:
            hero1_index = i
        elif obj.get("hero_data", {}).get("name") == HERO2:
            hero2_index = i

    # Only swap if both heroes exist
    if hero1_index is not None and hero2_index is not None:
        object_data[hero1_index], object_data[hero2_index] = (
            object_data[hero2_index],
            object_data[hero1_index],
        )

    xprint(type=TextType.DONE)
    wait_for_keypress()
