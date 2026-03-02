import random

from src.common import TextAlign, TextType, map_data
from src.defs import creatures, objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def modify_abandoned_mines():
    xprint(type=TextType.ACTION, text="Modifying abandoned mines…")

    modified_count = 0

    for obj in map_data["object_data"]:
        if (
            obj["id"] == objects.ID.Mine
            and obj["sub_id"] == objects.SubID.Resource.Abandoned
            or obj["id"] == objects.ID.Abandoned_Mine
        ):

            modified_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, align=TextAlign.CENTER, text=f"Modified {modified_count} abandoned mines.")
    wait_for_keypress()
