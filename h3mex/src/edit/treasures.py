import random

import src.file.m8_objects as m8_objects
from src.common import TextType, map_data
from src.defs import artifacts, objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress

RANDOM_CONTENTS = 4294967295


def modify_treasure_rewards() -> None:
    xprint(type=TextType.ACTION, text="Modifying treasure rewards…")

    TREASURE_OBJECTS = {
        # objects.ID.Campfire,
        # objects.ID.Treasure_Chest,
        # objects.ID.Resource,
        # objects.ID.Random_Resource,
        # objects.ID.Sea_Chest,
        # objects.ID.Flotsam,
        objects.ID.HotA_Pickup,
    }

    modified_count = 0

    for obj in map_data["object_data"]:
        if obj["id"] in TREASURE_OBJECTS:
            modified_count += 1
            match obj["id"]:
                case objects.ID.Campfire:
                    zone_type = obj.get("zone_type", "")
                    if zone_type in {"P1"}:
                        gold = random.randint(400, 1000)
                        other = random.randint(6, 10)
                    elif zone_type in {"P2", "P3", "L1", "W1"}:
                        gold = random.randint(1000, 3000)
                        other = random.randint(11, 15)
                    elif zone_type in {"P4", "L2", "W2"}:
                        gold = random.randint(3000, 5000)
                        other = random.randint(16, 20)
                    elif zone_type in {"L3", "W3"}:
                        gold = random.randint(5000, 7000)
                        other = random.randint(21, 25)
                    elif zone_type in {"L4", "W4", "R1", "R2", "R3", "R4"}:
                        gold = random.randint(7000, 10000)
                        other = random.randint(25, 30)
                    else:
                        xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                        break
                    secondary_resource = random.randint(0, 5)
                    obj["mode"] = 0
                    obj["resources"] = {6: gold, secondary_resource: other}

                case objects.ID.Treasure_Chest:
                    zone_type = obj.get("zone_type", "")
                    if zone_type in {"P1"}:
                        # 60% chance 0, 30% chance 1, 10% chance 2
                        rand = random.random()
                        if rand < 0.6:
                            obj["contents"] = 0
                        elif rand < 0.9:
                            obj["contents"] = 1
                        else:
                            obj["contents"] = 2
                    elif zone_type in {"P2", "P3", "L1", "W1"}:
                        # 20% chance 0, 40% chance 1, 40% chance 2
                        rand = random.random()
                        if rand < 0.2:
                            obj["contents"] = 0
                        elif rand < 0.6:
                            obj["contents"] = 1
                        else:
                            obj["contents"] = 2
                    elif zone_type in {"P4", "L2", "W2"}:
                        # 10% chance 0, 20% chance 1, 70% chance 2
                        rand = random.random()
                        if rand < 0.1:
                            obj["contents"] = 0
                        elif rand < 0.3:
                            obj["contents"] = 1
                        else:
                            obj["contents"] = 2
                    elif zone_type in {"L3", "W3", "L4", "W4", "R1", "R2", "R3", "R4"}:
                        obj["contents"] = 2
                    else:
                        xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                        break

                case objects.ID.Resource | objects.ID.Random_Resource:
                    zone_type = obj.get("zone_type", "")
                    if zone_type in {"P1"}:
                        obj["amount"] = random.randint(5, 10)
                    elif zone_type in {"P2", "P3", "L1", "W1"}:
                        obj["amount"] = random.randint(15, 20)
                    elif zone_type in {"P4", "L2", "W2"}:
                        obj["amount"] = random.randint(25, 30)
                    elif zone_type in {"L3", "W3"}:
                        obj["amount"] = random.randint(35, 40)
                    elif zone_type in {"L4", "W4", "R1", "R2", "R3", "R4"}:
                        obj["amount"] = random.randint(45, 50)
                    else:
                        xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                        break

                case objects.ID.Sea_Chest:
                    obj["contents"] = 1

                case objects.ID.Flotsam:
                    obj["trash_bytes"] = RANDOM_CONTENTS
                    zone_type = obj.get("zone_type", "")
                    if zone_type in {"P1"}:
                        # 60% chance 1, 30% chance 2, 10% chance 3
                        rand = random.random()
                        if rand < 0.6:
                            obj["contents"] = 1
                        elif rand < 0.9:
                            obj["contents"] = 2
                        else:
                            obj["contents"] = 3
                    elif zone_type in {"P2", "P3", "L1", "W1"}:
                        # 20% chance 1, 40% chance 2, 40% chance 3
                        rand = random.random()
                        if rand < 0.2:
                            obj["contents"] = 1
                        elif rand < 0.6:
                            obj["contents"] = 2
                        else:
                            obj["contents"] = 3
                    elif zone_type in {"P4", "L2", "W2"}:
                        # 10% chance 1, 20% chance 2, 70% chance 3
                        rand = random.random()
                        if rand < 0.1:
                            obj["contents"] = 1
                        elif rand < 0.3:
                            obj["contents"] = 2
                        else:
                            obj["contents"] = 3
                    elif zone_type in {"L3", "W3", "L4", "W4", "R1", "R2", "R3", "R4"}:
                        obj["contents"] = 3
                    else:
                        xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                        break

                case objects.ID.HotA_Pickup:
                    match obj["sub_id"]:
                        case objects.SubID.HotAPickups.Ancient_Lamp:
                            obj["contents"] = 0
                            obj["amount"] = random.randint(25, 150)

                        case objects.SubID.HotAPickups.Sea_Barrel:
                            obj["contents"] = 0
                            obj["resource"] = random.choice(
                                [
                                    objects.SubID.Resource.Mercury,
                                    objects.SubID.Resource.Sulfur,
                                    objects.SubID.Resource.Crystal,
                                    objects.SubID.Resource.Gems,
                                ]
                            )
                            zone_type = obj.get("zone_type", "")
                            if zone_type in {"P1"}:
                                obj["amount"] = random.randint(5, 10)
                            elif zone_type in {"P2", "P3", "L1", "W1"}:
                                obj["amount"] = random.randint(15, 20)
                            elif zone_type in {"P4", "L2", "W2"}:
                                obj["amount"] = random.randint(25, 30)
                            elif zone_type in {"L3", "W3"}:
                                obj["amount"] = random.randint(35, 40)
                            elif zone_type in {"L4", "W4", "R1", "R2", "R3", "R4"}:
                                obj["amount"] = random.randint(45, 50)
                            else:
                                xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                                break

                        case objects.SubID.HotAPickups.Jetsam:
                            obj["trash_bytes"] = RANDOM_CONTENTS
                            zone_type = obj.get("zone_type", "")
                            if zone_type in {"P1"}:
                                # 60% chance 1, 30% chance 2, 10% chance 3
                                rand = random.random()
                                if rand < 0.6:
                                    obj["contents"] = 1
                                elif rand < 0.9:
                                    obj["contents"] = 2
                                else:
                                    obj["contents"] = 3
                            elif zone_type in {"P2", "P3", "L1", "W1"}:
                                # 20% chance 1, 40% chance 2, 40% chance 3
                                rand = random.random()
                                if rand < 0.2:
                                    obj["contents"] = 1
                                elif rand < 0.6:
                                    obj["contents"] = 2
                                else:
                                    obj["contents"] = 3
                            elif zone_type in {"P4", "L2", "W2"}:
                                # 10% chance 1, 20% chance 2, 70% chance 3
                                rand = random.random()
                                if rand < 0.1:
                                    obj["contents"] = 1
                                elif rand < 0.3:
                                    obj["contents"] = 2
                                else:
                                    obj["contents"] = 3
                            elif zone_type in {"L3", "W3", "L4", "W4", "R1", "R2", "R3", "R4"}:
                                obj["contents"] = 3
                            else:
                                xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                                break

                        case objects.SubID.HotAPickups.Vial_of_Mana:
                            zone_type = obj.get("zone_type", "")
                            if zone_type in {"P1"}:
                                # 40% chance 0, 30% chance 1, 20% chance 2, 10% chance 3
                                rand = random.random()
                                if rand < 0.4:
                                    obj["contents"] = 0
                                elif rand < 0.7:
                                    obj["contents"] = 1
                                elif rand < 0.9:
                                    obj["contents"] = 2
                                else:
                                    obj["contents"] = 3
                            elif zone_type in {"P2", "P3", "L1", "W1"}:
                                # 25% chance 0, 25% chance 1, 25% chance 2, 25% chance 3
                                rand = random.random()
                                if rand < 0.25:
                                    obj["contents"] = 0
                                elif rand < 0.5:
                                    obj["contents"] = 1
                                elif rand < 0.75:
                                    obj["contents"] = 2
                                else:
                                    obj["contents"] = 3
                            elif zone_type in {"P4", "L2", "W2"}:
                                # 10% chance 0, 20% chance 1, 30% chance 2, 40% chance 3
                                rand = random.random()
                                if rand < 0.1:
                                    obj["contents"] = 0
                                elif rand < 0.3:
                                    obj["contents"] = 1
                                elif rand < 0.6:
                                    obj["contents"] = 2
                                else:
                                    obj["contents"] = 3
                            elif zone_type in {"L3", "W3", "L4", "W4", "R1", "R2", "R3", "R4"}:
                                obj["contents"] = 3
                            else:
                                xprint(type=TextType.ERROR, text=f"Unknown zone type: {zone_type}")
                                break

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Modified {modified_count} treasures.",
    )
    wait_for_keypress()


def remove_sea_treasures():
    xprint(type=TextType.ACTION, text="Removing sea treasures with land on either side…")

    # Remove sea treasures as defined in add_treasures() if the tile directly to the left or right is a land tile
    # For HotA_Pickup, only sub_ids 1-3 are sea treasures (Ancient Lamp sub_id 0 is land-only)
    size = map_data["general"]["map_size"]

    # Build set of objects to remove
    objects_to_remove = set()

    for obj in map_data["object_data"]:
        is_sea_treasure = obj["id"] in {objects.ID.Sea_Chest, objects.ID.Flotsam, objects.ID.Shipwreck_Survivor} or (
            obj["id"] == objects.ID.HotA_Pickup and obj["sub_id"] in {1, 2, 3}
        )
        if is_sea_treasure:
            x, y, z = obj["coords"]

            # Determine terrain layer
            if z == 0:  # Overworld
                terrain_layer = (
                    map_data["terrain"][: size * size]
                    if map_data["general"]["has_underground"]
                    else map_data["terrain"]
                )
            else:  # Underground
                terrain_layer = map_data["terrain"][size * size :]

            # Check left tile
            left_x = x - 1
            if 0 <= left_x < size:
                idx_left = y * size + left_x
                terrain_type_left = terrain_layer[idx_left]["terrain_type"]
                if terrain_type_left != 8:  # Not sea
                    objects_to_remove.add(id(obj))
                    continue

            # Check right tile
            right_x = x + 1
            if 0 <= right_x < size:
                idx_right = y * size + right_x
                terrain_type_right = terrain_layer[idx_right]["terrain_type"]
                if terrain_type_right != 8:  # Not sea
                    objects_to_remove.add(id(obj))
                    continue

    # Rebuild object_data excluding removed treasures
    removed_count = len(objects_to_remove)
    map_data["object_data"] = [obj for obj in map_data["object_data"] if id(obj) not in objects_to_remove]

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Removed {removed_count} sea treasures.",
    )
    wait_for_keypress()


def remove_scholars():
    xprint(type=TextType.ACTION, text="Removing scholars…")

    # Protected coordinates
    protected_coords = [
        [48, 10, 0],
        [49, 10, 0],
        [50, 10, 0],
        [51, 10, 0],
        [48, 11, 0],
        [49, 11, 0],
        [50, 11, 0],
        [51, 11, 0],
        [102, 38, 0],
        [103, 38, 0],
        [102, 39, 0],
        [102, 40, 0],
        [7, 133, 0],
        [8, 133, 0],
        [9, 133, 0],
        [7, 134, 0],
        [8, 134, 0],
        [9, 134, 0],
        [7, 137, 0],
        [8, 137, 0],
        [9, 137, 0],
        [7, 138, 0],
        [8, 138, 0],
        [9, 138, 0],
        [76, 186, 1],
        [77, 186, 1],
        [78, 186, 1],
        [79, 186, 1],
        [80, 186, 1],
        [81, 186, 1],
        [82, 186, 1],
        [83, 186, 1],
        [84, 186, 1],
        [160, 142, 1],
        [161, 142, 1],
        [162, 142, 1],
        [161, 143, 1],
        [162, 143, 1],
        [163, 143, 1],
        [208, 134, 1],
        [208, 135, 1],
        [209, 135, 1],
        [210, 135, 1],
        [211, 135, 1],
        [212, 135, 1],
        [213, 135, 1],
        [212, 136, 1],
        [213, 136, 1],
        [214, 136, 1],
        [215, 136, 1],
        [218, 140, 1],
        [155, 114, 1],
        [155, 115, 1],
        [155, 116, 1],
        [87, 121, 1],
        [87, 123, 1],
        [87, 125, 1],
        [87, 127, 1],
    ]

    # Separate scholars into removable and protected
    scholars = [obj for obj in map_data["object_data"] if obj["id"] == objects.ID.Scholar]
    removable_scholars = [s for s in scholars if s["coords"] not in protected_coords]
    protected_scholars = [s for s in scholars if s["coords"] in protected_coords]

    # Remove all removable scholars
    removed_count = len(removable_scholars)
    removed_set = set(id(s) for s in removable_scholars)
    map_data["object_data"] = [
        obj for obj in map_data["object_data"] if not (obj["id"] == objects.ID.Scholar and id(obj) in removed_set)
    ]

    xprint(type=TextType.DONE)
    xprint()
    xprint(
        type=TextType.INFO,
        text=f"Removed {removed_count} scholars. Protected {len(protected_scholars)} scholars.",
    )
    wait_for_keypress()


def fix_empty_contents() -> None:
    xprint(type=TextType.ACTION, text="Fixing empty contents in objects…")

    target_ids = {
        objects.ID.Sea_Chest,
        objects.ID.Shipwreck_Survivor,
        objects.ID.Treasure_Chest,
        objects.ID.Warriors_Tomb,
    }
    empty_markers = {
        artifacts.ID.Empty_1_Byte,
        artifacts.ID.Empty_2_Bytes,
        artifacts.ID.Empty_Unknown,
        artifacts.ID.Empty_4_Bytes,
    }

    def enum_name_by_value(enum_cls, value: int) -> str:
        try:
            return enum_cls(value).name
        except ValueError:
            return f"0x{value:08X}"

    count = 0
    for obj in map_data["object_data"]:
        id = obj.get("id")
        if id in target_ids:
            contents = obj.get("contents")
            if contents in empty_markers:
                obj["artifact"] = contents
                count += 1
                xprint(
                    type=TextType.INFO,
                    text=f"{obj.get('type')} at {obj.get('coords')} contains {enum_name_by_value(artifacts.ID, contents)}",
                )
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def add_scholars():
    xprint(type=TextType.ACTION, text="Adding scholars…")

    # Distribution by zone_type
    zone_distribution = {
        "L1": 25,
        "L2": 50,
    }

    size = map_data["general"]["map_size"]
    has_underground = map_data["general"]["has_underground"]

    # Get scholar def_id
    scholar_def_id = None
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Scholar:
            scholar_def_id = obj["def_id"]
            break

    if scholar_def_id is None:
        xprint(type=TextType.ERROR, text="No scholar definition found on map. Cannot add scholars.")
        return

    # Build zone tile lookup tables
    zone_tiles = {0: {}, 1: {}}  # {level: {(x, y): zone_type}}

    # Create reverse mapping: zone_type -> RGB color
    zone_colors = {}
    if hasattr(objects, "ZoneInfo") and hasattr(objects.ZoneInfo, "TYPES"):
        # Reverse the TYPES dict: zone_type -> color tuple
        for color_tuple, zone_type in objects.ZoneInfo.TYPES.items():
            if zone_type in zone_distribution:
                zone_colors[zone_type] = color_tuple

    if not zone_colors:
        xprint(type=TextType.ERROR, text="Could not map zone types to colors.")
        return

    # Scan ground zone image (compare RGB only; images are RGBA)
    if m8_objects.zonetypes_img_g:
        for y in range(size):
            for x in range(size):
                pixel = m8_objects.zonetypes_img_g.getpixel((x, y))
                # pixel may be (r,g,b,a); compare only RGB
                rgb = pixel[0:3] if len(pixel) >= 3 else pixel
                for zone_type, color in zone_colors.items():
                    if rgb == color:
                        zone_tiles[0][(x, y)] = zone_type
                        break

    # Scan underground zone image (compare RGB only)
    if m8_objects.zonetypes_img_u and has_underground:
        for y in range(size):
            for x in range(size):
                pixel = m8_objects.zonetypes_img_u.getpixel((x, y))
                rgb = pixel[0:3] if len(pixel) >= 3 else pixel
                for zone_type, color in zone_colors.items():
                    if rgb == color:
                        zone_tiles[1][(x, y)] = zone_type
                        break

    # Calculate blocked tiles
    blocked_tiles = {0: set(), 1: set()}

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
                    if b != 1 or i == 1:
                        blocked_tiles[obj_z].add((tile_x, tile_y))

    # Add scholars
    levels = [0, 1] if has_underground else [0]
    added = 0
    placed_coords = set()
    existing_coords = {tuple(obj["coords"]) for obj in map_data["object_data"]}
    current_level_index = 0
    total_to_add = sum(zone_distribution.values())
    zone_added_count = {zone: 0 for zone in zone_distribution}
    attempts = 0
    # Increase attempts multiplier to reduce premature exhaustion on busy maps
    max_attempts = total_to_add * 500  # Increased from *50 to *500

    while added < total_to_add and attempts < max_attempts:
        attempts += 1
        z = levels[current_level_index]
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        coords_tuple = (x, y, z)

        # Check if coordinate is already taken
        if coords_tuple in placed_coords or coords_tuple in existing_coords:
            current_level_index = (current_level_index + 1) % len(levels)
            continue

        # Check if coordinate is on a blocked tile
        if (x, y) in blocked_tiles[z]:
            current_level_index = (current_level_index + 1) % len(levels)
            continue

        # Get zone type from lookup table
        current_zone_type = zone_tiles[z].get((x, y))
        if current_zone_type is None or current_zone_type not in zone_distribution:
            current_level_index = (current_level_index + 1) % len(levels)
            continue

        # Check if we've met quota for this zone
        if zone_added_count[current_zone_type] >= zone_distribution[current_zone_type]:
            current_level_index = (current_level_index + 1) % len(levels)
            continue

        # Get zone color
        current_zone_color = zone_colors.get(current_zone_type, "")

        # Create scholar
        coords = list(coords_tuple)
        scholar = {
            "coords": coords,
            "coords_offset": coords,
            "zone_type": current_zone_type,
            "zone_owner": current_zone_color,
            "def_id": scholar_def_id,
            "id": objects.ID.Scholar,
            "sub_id": 0,
            "type": "Scholar",
            "subtype": "Scholar",
            "reward_type": 255,
        }

        map_data["object_data"].append(scholar)
        existing_coords.add(coords_tuple)
        placed_coords.add(coords_tuple)
        zone_added_count[current_zone_type] += 1
        added += 1

        current_level_index = (current_level_index + 1) % len(levels)

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Added {added} scholars.")
    wait_for_keypress()


def add_treasures():
    xprint(text="Adding treasures…")
    # xprint()

    # Candidate pools
    land_treasures = [
        objects.ID.Scholar,
        objects.ID.Scholar,
        objects.ID.Treasure_Chest,
        objects.ID.Treasure_Chest,
        objects.ID.Treasure_Chest,
        objects.ID.Treasure_Chest,
        objects.ID.Treasure_Chest,
        objects.ID.Random_Resource,
        objects.ID.Random_Resource,
        objects.ID.Random_Resource,
        objects.ID.Campfire,
        objects.ID.Campfire,
    ]

    sea_treasures = [
        objects.ID.Sea_Chest,
        objects.ID.Sea_Chest,
        objects.ID.Sea_Chest,
        objects.ID.Flotsam,
        objects.ID.Flotsam,
        objects.ID.Flotsam,
        objects.ID.Shipwreck_Survivor,
    ]

    sea_hota_collectible = [
        objects.SubID.HotAPickups.Sea_Barrel,
        objects.SubID.HotAPickups.Sea_Barrel,
        objects.SubID.HotAPickups.Sea_Barrel,
        objects.SubID.HotAPickups.Jetsam,
        objects.SubID.HotAPickups.Jetsam,
        objects.SubID.HotAPickups.Jetsam,
        objects.SubID.HotAPickups.Vial_of_Mana,
    ]

    size = map_data["general"]["map_size"]
    has_underground = map_data["general"]["has_underground"]

    # Build def_id map
    def_ids: dict[tuple[int, int], int] = {}
    for obj in map_data["object_data"]:
        def_ids[(obj["id"], obj["sub_id"])] = obj["def_id"]

    # Filter available treasures
    land_treasures = [id for id in land_treasures if (id, 0) in def_ids]
    sea_treasures = [id for id in sea_treasures if id != objects.ID.HotA_Pickup and (id, 0) in def_ids]
    sea_hota_available = [
        int(sub_id) for sub_id in sea_hota_collectible if (objects.ID.HotA_Pickup, int(sub_id)) in def_ids
    ]
    if sea_hota_available:
        sea_treasures.append(objects.ID.HotA_Pickup)
        sea_treasures.append(objects.ID.HotA_Pickup)
        sea_treasures.append(objects.ID.HotA_Pickup)
        sea_treasures.append(objects.ID.HotA_Pickup)
        sea_treasures.append(objects.ID.HotA_Pickup)
        sea_treasures.append(objects.ID.HotA_Pickup)
        sea_treasures.append(objects.ID.HotA_Pickup)

    if not land_treasures and not sea_treasures:
        xprint(type=TextType.ERROR, text="No eligible treasure definitions found on map. Nothing to add.")
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
        objects.ID.Random_Resource: _get_random_resource,
        objects.ID.Campfire: _get_campfire,
        objects.ID.Scholar: _get_scholar,
        objects.ID.Treasure_Chest: _get_treasure_chest,
        objects.ID.Sea_Chest: _get_sea_chest,
        objects.ID.Flotsam: _get_flotsam,
        objects.ID.Shipwreck_Survivor: _get_shipwreck_survivor,
    }

    hota_creators = {
        objects.SubID.HotAPickups.Sea_Barrel: _get_sea_barrel,
        objects.SubID.HotAPickups.Jetsam: _get_jetsam,
        objects.SubID.HotAPickups.Vial_of_Mana: _get_vial_of_mana,
    }

    levels = [0, 1] if has_underground else [0]
    added = 0
    attempts_per_obj = 0
    placed_coords = set()  # Track coordinates where we've placed treasures during this run
    current_level_index = 0  # Track which level we're currently trying

    amount_to_add = 4000

    while added < amount_to_add and attempts_per_obj < 1000:
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
        terrain_type = terrain_layer[idx]["terrain_type"]

        # Create object
        if terrain_type == 8:  # Water
            if not sea_treasures:
                attempts_per_obj += 1
                continue
            id = random.choice(sea_treasures)
            if id == objects.ID.HotA_Pickup:
                sub_id = random.choice(sea_hota_available)
                def_id = def_ids[(objects.ID.HotA_Pickup, sub_id)]
                new_obj = hota_creators[sub_id](coords, def_id)
                new_obj["sub_id"] = sub_id
            else:
                def_id = def_ids[(id, 0)]
                new_obj = creators[id](coords, def_id)
        elif terrain_type != 9:  # Land (except void)
            if not land_treasures:
                attempts_per_obj += 1
                continue
            id = random.choice(land_treasures)
            def_id = def_ids[(id, 0)]
            new_obj = creators[id](coords, def_id)
        else:
            attempts_per_obj += 1
            continue

        # Log
        # obj_name = Object(id).name if id != Object.HotA_Collectible else Object.HotA_Collectible(sub_id).name
        # obj_name = Object(id).name
        # xprint(
        #     type=MsgType.INFO,
        #     text=f"{added + 1}/{max_attempts} {Color.GREEN}{obj_name}{Color.CYAN} added at {Color.GREEN}{coords}{Color.CYAN} in {attempts_per_obj + 1} attempts",
        # )

        if (added + 1) % 100 == 0:
            xprint(text=f"Adding treasures… {added + 1}/{amount_to_add}", overwrite=1)

        map_data["object_data"].append(new_obj)
        placed_coords.add(coords)  # Track this placement
        added += 1
        attempts_per_obj = 0

        # Only alternate levels after successful placement
        current_level_index = (current_level_index + 1) % len(levels)

    xprint()
    xprint(type=TextType.INFO, text=f"Added {added} treasures.")
    wait_for_keypress()


def _get_base_object(coords, id, def_id):
    """Common object creation logic"""
    zone_type, zone_owner = ("", "")
    if m8_objects.has_zone_images:
        zone_type, zone_owner = m8_objects.get_zone(coords)

    return {
        "coords": coords,
        "coords_offset": coords,
        "zone_type": zone_type,
        "zone_owner": zone_owner,
        "def_id": def_id,
        "id": id,
        "sub_id": 0,
    }


def _get_random_resource(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Random_Resource, def_id)
    obj.update(
        {
            "type": "Random Resource",
            "subtype": "Random Resource",
            "has_common": 0,
            "amount": 0,
            "garbage_bytes": b"\x00\x00\x00\x00",
        }
    )
    return obj


def _get_campfire(coords, def_id):
    obj = _get_base_object(coords, objects.ID.Campfire, def_id)
    obj.update(
        {
            "type": "Campfire",
            "subtype": "Campfire",
            "mode": RANDOM_CONTENTS,
            "extra_bytes": b"\xff\xff\xff\xff",
            "resources": {objects.SubID.Resource.Gold.value: 1, objects.SubID.Resource.Wood.value: 1},
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
    obj = _get_base_object(coords, objects.ID.HotA_Pickup, def_id)
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
    obj = _get_base_object(coords, objects.ID.HotA_Pickup, def_id)
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
    obj = _get_base_object(coords, objects.ID.HotA_Pickup, def_id)
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
