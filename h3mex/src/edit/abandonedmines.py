import random

from src.common import TextAlign, TextType, map_data
from src.defs import creatures, objects, players
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress

VALID_RESOURCES = [
    objects.SubID.Resource.Mercury,
    objects.SubID.Resource.Sulfur,
    objects.SubID.Resource.Crystal,
    objects.SubID.Resource.Gems,
    objects.SubID.Resource.Gold,
]


def modify_abandoned_mines():
    xprint(type=TextType.ACTION, text="Modifying abandoned mines…")

    modified_count = 0

    for obj in map_data["object_data"]:
        if (
            obj["id"] == objects.ID.Mine
            and obj["sub_id"] == objects.SubID.Resource.Abandoned
            or obj["id"] == objects.ID.Abandoned_Mine
        ):
            obj["is_custom"] = True

            # # Set resources
            # obj["resources"] = [0, 1, 0, 1, 1, 1, 1, 0]

            # # Set guards
            # if obj["zone_owner"] != players.ID.Neutral:
            #     obj["creature"] = random.choice(list(creatures.Level5))
            #     obj["min_val"] = 250
            #     obj["max_val"] = 500
            # elif obj["zone_type"] == "I":
            #     obj["creature"] = random.choice(list(creatures.Level1))
            #     obj["min_val"] = 1000
            #     obj["max_val"] = 1500
            # elif obj["zone_type"] == "II":
            #     level = random.choice([2, 3, 4])
            #     if level == 2:
            #         obj["creature"] = random.choice(list(creatures.Level2))
            #         obj["min_val"] = 1250
            #         obj["max_val"] = 1500
            #     elif level == 3:
            #         obj["creature"] = random.choice(list(creatures.Level3))
            #         obj["min_val"] = 750
            #         obj["max_val"] = 1000
            #     elif level == 4:
            #         obj["creature"] = random.choice(list(creatures.Level4))
            #         obj["min_val"] = 250
            #         obj["max_val"] = 500
            # elif obj["zone_type"] == "III":
            #     level = random.choice([6, 7])
            #     if level == 6:
            #         obj["creature"] = random.choice(list(creatures.Level6))
            #         obj["min_val"] = 500
            #         obj["max_val"] = 750
            #     elif level == 7:
            #         obj["creature"] = random.choice(list(creatures.Level7))
            #         obj["min_val"] = 100
            #         obj["max_val"] = 250

            modified_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, align=TextAlign.CENTER, text=f"Modified {modified_count} abandoned mines.")
    wait_for_keypress()
