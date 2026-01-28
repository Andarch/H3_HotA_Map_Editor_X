from src.common import TextType, map_data
from src.defs import objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def remove_objects() -> None:
    xprint(type=TextType.ACTION, text="Removing objects…")

    removed_count = 0

    # Find all Vials of Mana
    vials = []
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.HotA_Pickup and obj["sub_id"] == objects.SubID.HotAPickups.Vial_of_Mana:
            vials.append(obj)

    # Track which vials to remove (indices to avoid during iteration issues)
    vials_to_remove = set()

    # Check each pair of vials
    for i in range(len(vials)):
        if i in vials_to_remove:
            continue

        for j in range(i + 1, len(vials)):
            if j in vials_to_remove:
                continue

            # Calculate distance between vials
            x1, y1 = vials[i]["coords"][0], vials[i]["coords"][1]
            x2, y2 = vials[j]["coords"][0], vials[j]["coords"][1]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            # If within 20 tiles, mark the second vial for removal
            if distance <= 20:
                vials_to_remove.add(j)

    # Remove marked vials from map_data
    for idx in sorted(vials_to_remove, reverse=True):
        map_data["object_data"].remove(vials[idx])
        removed_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Removed {removed_count} Vials of Mana.",
    )
    wait_for_keypress()
