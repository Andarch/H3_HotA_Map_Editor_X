import random

from src.common import MsgType, map_data
from src.defs import objects
from src.file.m8_objects import get_zone, has_zone_images
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def add_explorer_bonuses():
    xprint(text="Adding explorer bonuses…")

    # Get map size
    size = map_data["general"]["map_size"]
    has_underground = map_data["general"]["has_underground"]

    # Get event object def_id
    def_id = None
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Event:
            def_id = obj["def_id"]
    if def_id is None:
        xprint(type=MsgType.ERROR, text="No event objects found on map. Unable to get def_id.")
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

    levels = [0, 1] if has_underground else [0]
    added = 0
    attempts_per_obj = 0
    placed_coords = set()  # Track coordinates where we've placed treasures during this run

    amount_to_add = 300

    # Divide map into 81 quadrants (9x9 grid)
    quadrant_size = size // 9
    total_quadrants = 81 * len(levels)  # 81 per level
    current_quadrant_index = 0
    max_attempts_per_quadrant = 100  # Move to next quadrant if we can't place after this many tries

    while added < amount_to_add and current_quadrant_index < total_quadrants * 10:
        # Determine which level and quadrant
        quadrant_in_cycle = current_quadrant_index % total_quadrants
        z = levels[quadrant_in_cycle // 81]
        quadrant_on_level = quadrant_in_cycle % 81

        # Calculate quadrant bounds
        quadrant_row = quadrant_on_level // 9
        quadrant_col = quadrant_on_level % 9
        x_min = quadrant_col * quadrant_size
        x_max = (quadrant_col + 1) * quadrant_size - 1
        y_min = quadrant_row * quadrant_size
        y_max = (quadrant_row + 1) * quadrant_size - 1

        # Generate random coordinates within the quadrant
        coords = (random.randint(x_min, x_max), random.randint(y_min, y_max), z)

        # Skip to next quadrant if too many failed attempts
        if attempts_per_obj >= max_attempts_per_quadrant:
            current_quadrant_index += 1
            attempts_per_obj = 0
            continue

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
        if terrain_type != 9 and terrain_type != 8:  # Not void or water
            new_obj = _get_explorer_bonus(coords, def_id)
        else:
            attempts_per_obj += 1
            continue

        if (added + 1) % 100 == 0:
            xprint(text=f"Adding explorer bonuses… {added + 1}/{amount_to_add}", overwrite=1)

        map_data["object_data"].append(new_obj)

        # Track this placement and surrounding 8 tiles
        placed_coords.add(coords)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_x = coords[0] + dx
                neighbor_y = coords[1] + dy
                if 0 <= neighbor_x < size and 0 <= neighbor_y < size:
                    placed_coords.add((neighbor_x, neighbor_y, coords[2]))

        added += 1
        attempts_per_obj = 0

        # Move to next quadrant after successful placement
        current_quadrant_index += 1

    xprint()
    xprint(type=MsgType.INFO, text=f"Added {added} explorer bonuses.")
    wait_for_keypress()


def _get_explorer_bonus(coords, def_id):
    zone_type, zone_color = ("", "")
    if has_zone_images:
        zone_type, zone_color = get_zone(coords)

    # Always add 1 to one random primary skill
    primary_skills = [0, 0, 0, 0]
    random_skill_index = random.randint(0, 3)
    primary_skills[random_skill_index] = 1

    # Default values (no bonus)
    experience = 0
    spell_points = 0
    morale = 0
    luck = 0
    movement_points = 0

    # 50% chance to have an additional bonus
    if random.random() < 0.5:
        bonus_type = random.choice(["experience", "spell_points", "morale", "luck", "movement_points"])
        if bonus_type == "experience":
            experience = random.choice([3000, 4000, 5000])
        elif bonus_type == "spell_points":
            spell_points = random.choice([100, 200, 300])
        elif bonus_type == "morale":
            morale = random.choice([1, 2, 3])
        elif bonus_type == "luck":
            luck = random.choice([1, 2, 3])
        elif bonus_type == "movement_points":
            movement_points = random.choice([500, 1000, 1500])

    return {
        "coords": coords,
        "coords_offset": coords,
        "zone_type": zone_type,
        "zone_color": zone_color,
        "def_id": def_id,
        "id": objects.ID.Event,
        "sub_id": 0,
        "type": "Event",
        "subtype": "Event",
        "has_common": 1,
        "message": "Explorer Bonus",
        "common_garbage_bytes": b"\x00\x00\x00\x00",
        "contents": {
            "Experience": experience,
            "Spell_Points": spell_points,
            "Morale": morale,
            "Luck": luck,
            "Resources": [0, 0, 0, 0, 0, 0, 0],
            "Primary_Skills": primary_skills,
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": movement_points,
        },
        "allowed_players": [0, 1, 1, 1, 1, 1, 1, 1],
        "allow_ai": False,
        "cancel_event": True,
        "garbage_bytes": b"\x00\x00\x00\x00",
        "allow_human": True,
        "difficulty": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
