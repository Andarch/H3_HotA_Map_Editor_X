import data.objects as objects
from ...common import *

def set_random_monsters(obj_data: list) -> bool:
    xprint(type=Text.ACTION, text="Setting random monsters 1-7 to any level...")

    # Find the first generic Random Monster to get its properties
    generic_random_monster = None
    for obj in obj_data:
        if obj["id"] == objects.ID.Random_Monster:
            generic_random_monster = obj
            break

    if not generic_random_monster:
        xprint(type=Text.ERROR, text="No generic Random Monster found in map data")
        return False

    # Get the target properties from generic Random Monster
    target_def_id = generic_random_monster["def_id"]
    target_id = generic_random_monster["id"]
    target_sub_id = generic_random_monster["sub_id"]

    # Random Monster IDs to convert (1-7)
    random_monster_ids = [
        objects.ID.Random_Monster_1,
        objects.ID.Random_Monster_2,
        objects.ID.Random_Monster_3,
        objects.ID.Random_Monster_4,
        objects.ID.Random_Monster_5,
        objects.ID.Random_Monster_6,
        objects.ID.Random_Monster_7
    ]

    # Update Random Monster 1-7 objects
    for obj in obj_data:
        if obj["id"] in random_monster_ids:
            obj["def_id"] = target_def_id
            obj["id"] = target_id
            obj["sub_id"] = target_sub_id
            obj["type"] = "Random Monster"
            obj["subtype"] = "Random Monster"

    xprint(type=Text.SPECIAL, text=DONE)
    return True
