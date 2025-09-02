import random

from src.common import Color, MsgType, map_data, wait_for_keypress, xprint
from src.defs import objects
from src.file.m8_objects import get_zone, has_zone_images

RANDOM_CONTENTS = 4294967295


def add_treasures():
    xprint(text="Adding treasures…")
    xprint()

    # Candidate pools
    land_treasures = [
        objects.ID.Campfire,
        objects.ID.Scholar,
        objects.ID.Treasure_Chest,
    ]

    sea_treasures = [
        objects.ID.Sea_Chest,
        objects.ID.Flotsam,
        objects.ID.Shipwreck_Survivor,
    ]

    sea_hota_collectible = [
        objects.HotA_Collectible.Sea_Barrel,
        objects.HotA_Collectible.Jetsam,
        objects.HotA_Collectible.Vial_of_Mana,
    ]

    size = map_data["general"]["map_size"]
    has_underground = map_data["general"]["has_underground"]

    # Build def_id map
    def_ids: dict[tuple[int, int], int] = {}
    for obj in map_data["object_data"]:
        def_ids[(obj["id"], obj["sub_id"])] = obj["def_id"]

    # Filter available treasures
    land_treasures = [id for id in land_treasures if (id, 0) in def_ids]
    sea_treasures = [id for id in sea_treasures if id != objects.ID.HotA_Collectible and (id, 0) in def_ids]
    sea_hota_available = [
        int(sub_id) for sub_id in sea_hota_collectible if (objects.ID.HotA_Collectible, int(sub_id)) in def_ids
    ]
    if sea_hota_available:
        sea_treasures.append(objects.ID.HotA_Collectible)

    if not land_treasures and not sea_treasures:
        xprint(type=MsgType.ERROR, text="No eligible treasure definitions found on map. Nothing to add.")
        return

    # Calculate blocked tiles: only tiles actually marked as blocked (red) or interactive (yellow) in the mask
    blocked_tiles = {0: set(), 1: set()}  # {level: set of (x, y) tuples}

    for obj in map_data["object_data"]:
        def_ = map_data["object_defs"][obj["def_id"]]
        blockMask = def_["red_squares"]
        interactiveMask = def_["yellow_squares"]

        obj_x, obj_y, obj_z = obj["coords"]

        for r in range(6):
            for c in range(8):
                index = r * 8 + c
                tile_x = obj_x - 7 + c
                tile_y = obj_y - 5 + r

                if 0 <= tile_x < size and 0 <= tile_y < size:
                    b = blockMask[index]
                    i = interactiveMask[index]
                    # Block if mask bit is not passable (b != 1) or interactable (i == 1)
                    if b != 1 or i == 1:
                        blocked_tiles[obj_z].add((tile_x, tile_y))

    # Object creators
    creators = {
        objects.ID.Campfire: _get_campfire,
        objects.ID.Scholar: _get_scholar,
        objects.ID.Treasure_Chest: _get_treasure_chest,
        objects.ID.Sea_Chest: _get_sea_chest,
        objects.ID.Flotsam: _get_flotsam,
        objects.ID.Shipwreck_Survivor: _get_shipwreck_survivor,
    }

    hota_creators = {
        objects.HotA_Collectible.Sea_Barrel: _get_sea_barrel,
        objects.HotA_Collectible.Jetsam: _get_jetsam,
        objects.HotA_Collectible.Vial_of_Mana: _get_vial_of_mana,
    }

    levels = [0, 1] if has_underground else [0]
    added = 0
    attempts_per_obj = 0
    placed_coords = set()  # Track coordinates where we've placed treasures during this run
    current_level_index = 0  # Track which level we're currently trying

    while added < 1000 and attempts_per_obj < 1000:
        z = levels[current_level_index]  # Use current level
        coords = (random.randint(0, size - 1), random.randint(0, size - 1), z)

        # Check if coordinate is already taken (existing object or newly placed)
        if any(obj["coords"] == coords for obj in map_data["object_data"]) or coords in placed_coords:
            attempts_per_obj += 1
            continue

        # Check if coordinate is on a blocked tile
        if (coords[0], coords[1]) in blocked_tiles[coords[2]]:
            attempts_per_obj += 1
            continue

        # Check terrain
        if coords[2] == 0:  # Overworld
            terrain_layer = map_data["terrain"][: size * size] if has_underground else map_data["terrain"]
        else:  # Underground
            terrain_layer = map_data["terrain"][size * size :]

        idx = coords[1] * size + coords[0]
        terrain_type = terrain_layer[idx]["terrain_type_int"]

        # Create object
        if terrain_type == 8:  # Water
            if not sea_treasures:
                attempts_per_obj += 1
                continue
            id = random.choice(sea_treasures)
            if id == objects.ID.HotA_Collectible:
                sub_id = random.choice(sea_hota_available)
                def_id = def_ids[(objects.ID.HotA_Collectible, sub_id)]
                # Always get correct def_id for each sub_id; no fallback
                new_obj = hota_creators[sub_id](coords, def_id)
                new_obj["sub_id"] = sub_id
            else:
                def_id = def_ids[(id, 0)]
                new_obj = creators[id](coords, def_id)
        else:  # Land
            if not land_treasures:
                attempts_per_obj += 1
                continue
            id = random.choice(land_treasures)
            def_id = def_ids[(id, 0)]
            new_obj = creators[id](coords, def_id)

        # Log
        obj_name = objects.ID(id).name if id != objects.ID.HotA_Collectible else objects.HotA_Collectible(sub_id).name
        xprint(
            type=MsgType.INFO,
            text=f"{Color.GREEN}{obj_name}{Color.CYAN} added at {Color.GREEN}{coords}{Color.CYAN} in {attempts_per_obj + 1} attempts",
        )

        map_data["object_data"].append(new_obj)
        placed_coords.add(coords)  # Track this placement
        added += 1
        attempts_per_obj = 0

        # Only alternate levels after successful placement
        current_level_index = (current_level_index + 1) % len(levels)

    xprint()
    xprint(type=MsgType.INFO, text=f"Added {added} treasures.")
    wait_for_keypress()


def _get_base_object(coords, id, def_id):
    """Common object creation logic"""
    zone_type, zone_color = ("", "")
    if has_zone_images:
        zone_type, zone_color = get_zone(coords)

    return {
        "coords": coords,
        "coords_offset": coords,
        "zone_type": zone_type,
        "zone_color": zone_color,
        "def_id": def_id,
        "id": id,
        "sub_id": 0,
    }


def _get_campfire(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Campfire, def_id)
    obj.update(
        {
            "type": "Campfire",
            "subtype": "Campfire",
            "mode": RANDOM_CONTENTS,
            "extra_bytes": b"\xff\xff\xff\xff",
            "resources": {objects.Resource.Gold.value: 1, objects.Resource.Wood.value: 1},
        }
    )
    return obj


def _get_scholar(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Scholar, def_id)
    obj.update(
        {
            "type": "Scholar",
            "subtype": "Scholar",
            "reward_type": 255,
        }
    )
    return obj


def _get_treasure_chest(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Treasure_Chest, def_id)
    obj.update(
        {
            "type": "Treasure Chest",
            "subtype": "Treasure Chest",
            "contents": RANDOM_CONTENTS,
            "artifact": RANDOM_CONTENTS,
        }
    )
    return obj


def _get_sea_chest(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Sea_Chest, def_id)
    obj.update(
        {
            "type": "Sea Chest",
            "subtype": "Sea Chest",
            "contents": RANDOM_CONTENTS,
            "artifact": RANDOM_CONTENTS,
        }
    )
    return obj


def _get_flotsam(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Flotsam, def_id)
    obj.update(
        {
            "type": "Flotsam",
            "subtype": "Flotsam",
            "contents": RANDOM_CONTENTS,
            "trash_bytes": RANDOM_CONTENTS,
        }
    )
    return obj


def _get_shipwreck_survivor(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Shipwreck_Survivor, def_id)
    obj.update(
        {
            "type": "Shipwreck Survivor",
            "subtype": "Shipwreck Survivor",
            "contents": RANDOM_CONTENTS,
            "artifact": RANDOM_CONTENTS,
        }
    )
    return obj


def _get_sea_barrel(coords, def_id):
    obj = _get_base_object(coords, objects.ID.HotA_Collectible, def_id)
    obj.update(
        {
            "sub_id": 1,
            "type": "HotA Collectible",
            "subtype": "Sea Barrel",
            "contents": RANDOM_CONTENTS,
            "trash_bytes": b"\xff\xff\xff\xff",
            "amount": 1,
            "resource": 1,
            "mystery_bytes": b"\x01\x00\x00\x00\x00",
        }
    )
    return obj


def _get_jetsam(coords, def_id):
    obj = _get_base_object(coords, objects.ID.HotA_Collectible, def_id)
    obj.update(
        {
            "sub_id": 2,
            "type": "HotA Collectible",
            "subtype": "Jetsam",
            "contents": RANDOM_CONTENTS,
            "trash_bytes": RANDOM_CONTENTS,
        }
    )
    return obj


def _get_vial_of_mana(coords, def_id):
    obj = _get_base_object(coords, objects.ID.HotA_Collectible, def_id)
    obj.update(
        {
            "sub_id": 3,
            "type": "HotA Collectible",
            "subtype": "Vial of Mana",
            "contents": RANDOM_CONTENTS,
            "trash_bytes": b"\xff\xff\xff\xff",
        }
    )
    return obj
