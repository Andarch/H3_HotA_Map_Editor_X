from src.common import TextType, map_data
from src.defs import objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def remove_objects() -> None:
    xprint(type=TextType.ACTION, text="Removing objects…")

    # Protected coordinates
    protected_coords = [
        [85, 84, 0],
        [83, 86, 0],
        [87, 86, 0],
        [6, 231, 1],
        [4, 233, 1],
        [8, 233, 1],
        [12, 239, 1],
        [14, 239, 1],
        [16, 239, 1],
        [18, 239, 1],
        [12, 244, 1],
        [14, 244, 1],
        [16, 244, 1],
    ]

    # Separate monoliths into removable and protected
    monoliths = [
        obj
        for obj in map_data["object_data"]
        if obj["id"] == objects.ID.One_Way_Portal_Entrance and not (4 <= obj["sub_id"] <= 7 and obj["sub_id"] != 11)
    ]
    removable_monoliths = [m for m in monoliths if m["coords"] not in protected_coords]
    protected_monoliths = [m for m in monoliths if m["coords"] in protected_coords]

    # Remove all removable monoliths
    removed_count = len(removable_monoliths)
    removed_set = set(id(m) for m in removable_monoliths)
    map_data["object_data"] = [
        obj
        for obj in map_data["object_data"]
        if not (obj["id"] == objects.ID.One_Way_Portal_Entrance and id(obj) in removed_set)
    ]

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Removed {removed_count} monoliths. Protected {len(protected_monoliths)} monoliths.",
    )
    wait_for_keypress()
