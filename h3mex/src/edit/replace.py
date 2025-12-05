from src.common import TextType, map_data
from src.defs import objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def replace_objects() -> None:
    xprint(type=TextType.ACTION, text="Replacing objects…")

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

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Ocean_Bottle:
            def_id = obj["def_id"]

    replaced_count = 0
    protected_count = 0

    for i, obj in enumerate(map_data["object_data"]):
        if obj["id"] == objects.ID.One_Way_Portal_Entrance and obj["sub_id"] not in {4, 5, 6, 7, 11}:
            if obj["coords"] in protected_coords:
                protected_count += 1
                continue
            map_data["object_data"][i] = _get_ocean_bottle(
                coords=obj["coords"],
                coords_offset=obj["coords_offset"],
                zone_type=obj["zone_type"],
                zone_color=obj["zone_color"],
                def_id=def_id,
            )
            replaced_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Replaced {replaced_count} objects. Protected {protected_count} objects.",
    )
    wait_for_keypress()


def _get_ocean_bottle(
    coords: list[int], coords_offset: list[int], zone_type: str, zone_color: str, def_id: int
) -> dict:
    return {
        "coords": coords,
        "coords_offset": coords_offset,
        "zone_type": zone_type,
        "zone_color": zone_color,
        "def_id": def_id,
        "id": 59,
        "sub_id": 0,
        "type": "Ocean Bottle",
        "subtype": "Ocean Bottle",
        "message": "Old one-way monolith entrance",
        "garbage_bytes": b"\x00\x00\x00\x00",
    }
