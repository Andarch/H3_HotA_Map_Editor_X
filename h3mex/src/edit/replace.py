import random

from src.common import TextType, map_data
from src.defs import objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def replace_objects() -> None:
    xprint(type=TextType.ACTION, text="Replacing objects…")

    replaced_count = 0

    # Define the def_id mapping
    def_id_map = {3: 1798, 4: 1799, 2: 1800, 8: 1801, 5: 1802, 10: 1803}

    # Define the region boundaries
    # x_min, x_max = 28, 126
    # y_min, y_max = 63, 114
    # z_target = 0

    for i, obj in enumerate(map_data["object_data"]):
        if obj["id"] == objects.ID.Mountain:
            # Check if def_id is valid
            if obj["def_id"] in def_id_map:
                # Check if coords are in the region
                # x, y, z = obj["coords"][0], obj["coords"][1], obj["coords"][2]

                # if x_min <= x <= x_max and y_min <= y <= y_max and z == z_target:

                # 50% chance to replace
                if random.random() < 0.5:
                    # Replace the mountain with glacier
                    obj["def_id"] = def_id_map[obj["def_id"]]
                    obj["id"] = 140
                    obj["sub_id"] = 14
                    obj["type"] = "HotA Decor 2"
                    obj["subtype"] = "Glacier"
                    replaced_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Replaced {replaced_count} objects.",
    )
    wait_for_keypress()
