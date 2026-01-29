from src.common import TextType, map_data
from src.defs import objects, terrain
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def replace_objects() -> None:
    xprint(type=TextType.ACTION, text="Replacing objects…")

    replaced_count = 0
    size = map_data["general"]["map_size"]

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Seers_Hut:
            # Get terrain coordinates
            x, y, z = obj["coords_offset"]

            # Calculate terrain index (z=0 is surface, z=1 is underground)
            terrain_index = y * size + x + (size * size if z == 1 else 0)

            # Check if on snow tile
            if map_data["terrain"][terrain_index]["terrain_type"] == terrain.ID.Snow:
                obj["def_id"] = 1552
                obj["sub_id"] = 7
                replaced_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Replaced {replaced_count} objects.",
    )
    wait_for_keypress()
