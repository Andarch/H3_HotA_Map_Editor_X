from src.common import TextType, map_data
from src.defs import objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def remove_objects() -> None:
    xprint(type=TextType.ACTION, text="Removing objects…")

    removed_count = sum(
        1 for obj in map_data["object_data"] if obj.get("id") == objects.ID.Event_Object and obj.get("hero_event_id")
    )
    map_data["object_data"] = [
        obj
        for obj in map_data["object_data"]
        if not (obj.get("id") == objects.ID.Event_Object and obj.get("hero_event_id"))
    ]

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Removed {removed_count} objects.",
    )
    wait_for_keypress()
