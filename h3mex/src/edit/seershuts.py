from typing import Tuple

from src.common import TextType, map_data
from src.defs import objects
from src.file.m8_objects import Quest, Reward
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def modify_seers_huts():
    xprint(type=TextType.ACTION, text="Modifying seers' huts…")

    count = 0
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Seers_Hut:
            count_modified = False
            if obj["one_time_quests"]:
                for i in range(len(obj["one_time_quests"])):
                    quest, modified = _modify_quest(obj["one_time_quests"][i])
                    if modified:
                        obj["one_time_quests"][i] = quest
                        if not count_modified:
                            count += 1
                            count_modified = True
            if obj["repeatable_quests"]:
                for i in range(len(obj["repeatable_quests"])):
                    quest, modified = _modify_quest(obj["repeatable_quests"][i])
                    if modified:
                        obj["repeatable_quests"][i] = quest
                        if not count_modified:
                            count += 1
                            count_modified = True

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Modified {count} seers' huts.")
    wait_for_keypress()


def _modify_quest(quest: dict) -> Tuple[dict, bool]:
    if quest["quest"]["type"] == Quest.RETURN_WITH_RESOURCES:
        quest["quest"]["value"] = [v * 2 for v in quest["quest"]["value"]]
        if quest["reward"]["type"] == Reward.PRIMARY_SKILL:
            quest["reward"]["value"][1] = 2
        return quest, True
    elif quest["quest"]["type"] == Quest.RETURN_WITH_CREATURES:
        if quest["reward"]["type"] == Reward.PRIMARY_SKILL:
            quest["reward"]["value"][1] = 3
        if quest["reward"]["type"] == Reward.CREATURES:
            quest["reward"]["value"][0]["amount"] = 10
        return quest, True
    elif quest["quest"]["type"] == Quest.ACHIEVE_EXPERIENCE_LEVEL:
        if quest["quest"]["value"] == 20:
            quest["quest"]["value"] = 30
            quest["reward"]["value"][1] = 3
        elif quest["quest"]["value"] == 35 or quest["quest"]["value"] == 45:
            quest["quest"]["value"] = 60
            quest["reward"]["value"][1] = 6
        return quest, True

    return quest, False
