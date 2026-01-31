from src.common import TextType, map_data
from src.defs import objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress

RANDOM_CONTENTS = 4294967295


def replace_objects() -> None:
    xprint(type=TextType.ACTION, text="Replacing objects…")

    replaced_count = 0

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.HotA_Pickup and obj["sub_id"] == objects.SubID.HotAPickups.Vial_of_Mana:
            obj["trash_bytes"] = b"\xff\xff\xff\xff"
            replaced_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Replaced {replaced_count} objects.",
    )
    wait_for_keypress()
