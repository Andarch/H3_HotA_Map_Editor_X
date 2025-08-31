import random

from core.h3m import objects
from src.common import DONE, MsgType, map_data, xprint


def add_treasures():
    LAND_TREASURES = [
        objects.ID.Campfire,
        objects.ID.Scholar,
        objects.ID.Treasure_Chest,
    ]

    SEA_TREASURES = [
        objects.ID.Sea_Chest,
        objects.ID.Flotsam,
        objects.ID.Shipwreck_Survivor,
        objects.ID.HotA_Collectible,
    ]

    SEA_HOTA_COLLECTIBLE = [
        objects.HotA_Collectible.Sea_Barrel,
        objects.HotA_Collectible.Jetsam,
        objects.HotA_Collectible.Vial_of_Mana,
    ]

    size = map_data["general"]["map_size"]
    has_underground = map_data["general"]["has_underground"]

    levels = [0]
    if has_underground:
        levels.append(1)

    # Try to add 10 treasures
    added = 0
    attempts = 0
    max_attempts = 1000
    while added < 100 and attempts < max_attempts:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        z = random.choice(levels)
        coord = (x, y, z)

        # Check if object already exists at coord
        occupied = any(obj.get("coords") == coord for obj in map_data["object_data"])
        if occupied:
            attempts += 1
            continue

        # Check terrain type
        if z == 0:
            idx = y * size + x
        else:
            idx = size * size + y * size + x
        tile = map_data["terrain"][idx]
        terrain = tile["terrain_type_int"]  # or tile["terrain_type"]
        if terrain != 8:
            treasure_id = random.choice(LAND_TREASURES)
            new_obj = {
                "id": treasure_id,
                "coords": coord,
                "type": "Treasure",
            }
        else:
            treasure_id = random.choice(SEA_TREASURES)
            new_obj = {
                "id": treasure_id,
                "coords": coord,
                "type": "Treasure",
            }
            # If HotA_Collectible, set sub_id to 1-3 (not 0)
            if treasure_id == objects.ID.HotA_Collectible:
                new_obj["sub_id"] = random.choice(SEA_HOTA_COLLECTIBLE)
        map_data["object_data"].append(new_obj)
        added += 1
        xprint(
            type=MsgType.INFO,
            text=f"Added treasure {treasure_id} at {coord}{' (sub_id=' + str(new_obj.get('sub_id')) + ')' if 'sub_id' in new_obj else ''}",
        )
        attempts += 1

    xprint(type=MsgType.SPECIAL, text=DONE)
    xprint(type=MsgType.INFO, text=f"Added {added} treasures.")


# _get_
