from core.h3m import objects
from src.common import DONE, MsgType, map_data, xprint

RANDOM_MONSTER_LEVEL_IDS = [
    objects.ID.Random_Monster_1,
    objects.ID.Random_Monster_2,
    objects.ID.Random_Monster_3,
    objects.ID.Random_Monster_4,
    objects.ID.Random_Monster_5,
    objects.ID.Random_Monster_6,
    objects.ID.Random_Monster_7,
]


def set_random_monsters() -> None:
    xprint(type=MsgType.ACTION, text="Setting random monsters 1-7 to any level...")

    # Find the first Random Monster (non-level-specific) to get its def_id
    def_id = None
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Random_Monster:
            def_id = obj["def_id"]
            break
    if def_id is None:
        xprint(type=MsgType.ERROR, text="No random monster found.", skip_line=True)
        return

    # Update Random Monster 1-7 objects
    for obj in map_data["object_data"]:
        if obj["id"] in RANDOM_MONSTER_LEVEL_IDS:
            obj["def_id"] = def_id
            obj["id"] = objects.ID.Random_Monster
            obj["sub_id"] = 0
            obj["type"] = "Random Monster"
            obj["subtype"] = "Random Monster"

    xprint(type=MsgType.SPECIAL, text=DONE)
