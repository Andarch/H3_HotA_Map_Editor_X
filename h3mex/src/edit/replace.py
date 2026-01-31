from src.common import TextType, map_data
from src.defs import objects, terrain
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def replace_objects() -> None:
    xprint(type=TextType.ACTION, text="Replacing objects…")

    replaced_count = 0

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Random_Town:
            obj["def_id"] = 1808
            obj["id"] = 98
            obj["sub_id"] = 11
            replaced_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Replaced {replaced_count} objects.",
    )
    wait_for_keypress()
