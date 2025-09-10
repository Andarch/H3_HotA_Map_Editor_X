import random  # noqa: F401

from src.common import MsgType, map_data
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
    xprint(type=MsgType.ACTION, text="Setting random monsters 1-7 to any level…")

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
        if obj["id"] in RANDOM_MONSTER_IDS and obj["id"] != objects.ID.Random_Monster:
            obj["def_id"] = def_id
            obj["id"] = objects.ID.Random_Monster
            obj["sub_id"] = 0
            obj["type"] = "Random Monster"
            obj["subtype"] = "Random Monster"

    xprint(type=MsgType.DONE)


def set_monster_values() -> None:
    xprint(type=MsgType.ERROR, text="Not functional…")
    # xprint(type=MsgType.ACTION, text="Setting monster values…")

    # count = 0
    # for obj in map_data["object_data"]:
    #     if obj["id"] in RANDOM_MONSTER_IDS:
    #         monster = obj
    #         if not monster["is_value"] and monster["quantity"] == 0:
    #             monster["is_value"] = True
    #             monster["ai_value"] = random.randint(15000, 50000)

    #         count += 1

    # xprint(type=MsgType.SPECIAL, text=DONE)
    # xprint()
    # xprint(type=MsgType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def set_compliant_monster_values() -> None:
    xprint(type=MsgType.ACTION, text="Setting compliant monster values…")

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

    xprint(type=MsgType.DONE)
    xprint()
    xprint(type=MsgType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()
