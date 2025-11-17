import random  # noqa: F401

from src.common import TextType, map_data
from src.defs import creatures, objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress

RANDOM_MONSTER_IDS = [
    objects.ID.Random_Monster,
    objects.ID.Random_Monster_1,
    objects.ID.Random_Monster_2,
    objects.ID.Random_Monster_3,
    objects.ID.Random_Monster_4,
    objects.ID.Random_Monster_5,
    objects.ID.Random_Monster_6,
    objects.ID.Random_Monster_7,
]


def set_random_monsters() -> None:
    xprint(type=TextType.ACTION, text="Setting random monsters 1-7 to any level…")

    # Find the first Random Monster (non-level-specific) to get its def_id
    def_id = None
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Random_Monster:
            def_id = obj["def_id"]
            break
    if def_id is None:
        xprint(type=TextType.ERROR, text="No random monster found.", skip_line=True)
        return

    # Update Random Monster 1-7 objects
    for obj in map_data["object_data"]:
        if obj["id"] in RANDOM_MONSTER_IDS and obj["id"] != objects.ID.Random_Monster:
            obj["def_id"] = def_id
            obj["id"] = objects.ID.Random_Monster
            obj["sub_id"] = 0
            obj["type"] = "Random Monster"
            obj["subtype"] = "Random Monster"

    xprint(type=TextType.DONE)


def set_monster_values() -> None:
    xprint(type=TextType.ACTION, text="Setting monster values…")

    AI_VALUE_RANGES = {
        "P1": (2000, 50000),
        "P2": (50000, 200000),
        "P3": (200000, 500000),
        "P4": (500000, 999999),
        "R1": (2000, 50000),
        "R2": (50000, 200000),
        "R3": (200000, 500000),
        "R4": (500000, 999999),
        "L1": (2000, 50000),
        "L2": (50000, 200000),
        "L3": (200000, 500000),
        "L4": (500000, 999999),
        "W1": (2000, 50000),
        "W2": (50000, 200000),
        "W3": (200000, 500000),
        "W4": (500000, 999999),
    }

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj["id"] in {objects.ID.Monster, objects.ID.Random_Monster}
            and obj["disposition"] != creatures.Disposition.Compliant
        ):
            obj["disposition"] = random.randint(1, 4)
            obj["is_value"] = True
            if obj["zone_type"] in AI_VALUE_RANGES:
                obj["ai_value"] = random.randint(*AI_VALUE_RANGES[obj["zone_type"]])
            count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def set_compliant_monster_values() -> None:
    xprint(type=TextType.ACTION, text="Setting compliant monster values…")

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj.get("id") == objects.ID.Monster
            and obj.get("zone_type") == "Player"
            and obj.get("disposition") == creatures.Disposition.Compliant
        ):

            match obj["ai_value"]:
                case 1000:
                    obj["ai_value"] = 3000
                case 1500:
                    obj["ai_value"] = 10000
                case 2000:
                    obj["ai_value"] = 15000
                case 2500:
                    obj["ai_value"] = 25000
                case 10000:
                    obj["ai_value"] = 100000

            count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()
