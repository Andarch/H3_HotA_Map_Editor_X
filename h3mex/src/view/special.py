from src.common import TextType, map_data
from src.ui.xprint import xprint


def list_unreachable_tiles() -> None:
    xprint(text="Calculating unreachable tiles…", overwrite=7)
    xprint()

    OVERWORLD = 0
    UNDERGROUND = 1

    map_size = map_data["general"]["map_size"]
    has_underground = map_data["general"]["has_underground"]
    terrain = map_data["terrain"]
    object_defs = map_data["object_defs"]
    object_data = map_data["object_data"]

    # Initialize blocked tiles and interactive tiles sets for each layer
    blocked_tiles = {OVERWORLD: set(), UNDERGROUND: set()}
    interactive_tiles = {OVERWORLD: set(), UNDERGROUND: set()}

    # First, add ROCK terrain tiles as blocked tiles
    layers = [OVERWORLD]
    if has_underground:
        layers.append(UNDERGROUND)

    for layer in layers:
        if layer == OVERWORLD:
            terrain_layer = terrain[: map_size * map_size] if has_underground else terrain
        elif layer == UNDERGROUND:
            terrain_layer = terrain[map_size * map_size :]

        for i, tile in enumerate(terrain_layer):
            x = i % map_size
            y = i // map_size
            # Terrain type 9 is ROCK, which is impassable
            if tile["terrain_type"] == 9:  # ROCK terrain type
                blocked_tiles[layer].add((x, y))

    # Process objects to find blocked tiles and interactive tiles
    for obj in object_data:
        # Get object definition and both block mask and interactive mask
        def_ = object_defs[obj["def_id"]]
        blockMask = def_["red_squares"]
        interactiveMask = def_["yellow_squares"]

        obj_x, obj_y, obj_z = obj["coords"]

        # Process each tile in the object's 6x8 mask
        for r in range(6):  # 6 rows y-axis, from top to bottom
            for c in range(8):  # 8 columns x-axis, from left to right
                index = r * 8 + c  # Calculate the index into blockMask
                blocked_tile_x = obj_x - 7 + c
                blocked_tile_y = obj_y - 5 + r

                # Check if the tile is within the map
                if 0 <= blocked_tile_x < map_size and 0 <= blocked_tile_y < map_size:
                    # Track interactive tiles (yellow squares) - these need to be reachable
                    if interactiveMask[index] == 1:
                        if obj_z == OVERWORLD:
                            interactive_tiles[OVERWORLD].add((blocked_tile_x, blocked_tile_y))
                        elif obj_z == UNDERGROUND:
                            interactive_tiles[UNDERGROUND].add((blocked_tile_x, blocked_tile_y))

                    # A tile is truly blocked only if it's a red square AND not a yellow square
                    # Yellow squares are interactive/walkable, so should not be considered blocked
                    if blockMask[index] != 1 and interactiveMask[index] != 1:
                        if obj_z == OVERWORLD:
                            blocked_tiles[OVERWORLD].add((blocked_tile_x, blocked_tile_y))
                        elif obj_z == UNDERGROUND:
                            blocked_tiles[UNDERGROUND].add((blocked_tile_x, blocked_tile_y))

    # Find unreachable tiles for each layer
    unreachable_tiles = []

    layers = [OVERWORLD]
    if has_underground:
        layers.append(UNDERGROUND)

    for layer in layers:
        for y in range(map_size):
            for x in range(map_size):
                # Check both empty tiles and interactive tiles for reachability
                # Skip if this tile is blocked (but not if it's interactive)
                if (x, y) in blocked_tiles[layer]:
                    continue

                # Determine if this is an interactive tile that needs to be reachable
                is_interactive = (x, y) in interactive_tiles[layer]

                # For empty tiles, check if surrounded by blocked tiles
                # For interactive tiles, also check if they're reachable
                if not is_interactive or is_interactive:  # Check all non-blocked tiles
                    # Check all 8 surrounding tiles
                    surrounded = True
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:  # Skip the center tile
                                continue

                            neighbor_x = x + dx
                            neighbor_y = y + dy

                            # If neighbor is out of bounds, treat as blocked
                            if neighbor_x < 0 or neighbor_x >= map_size or neighbor_y < 0 or neighbor_y >= map_size:
                                continue

                            # If any neighbor is not blocked, this tile is not surrounded
                            if (neighbor_x, neighbor_y) not in blocked_tiles[layer]:
                                surrounded = False
                                break

                        if not surrounded:
                            break

                    # If completely surrounded, add to unreachable list
                    if surrounded:
                        layer_name = "Overworld" if layer == OVERWORLD else "Underground"
                        tile_type = " (Interactive)" if is_interactive else ""
                        coords = f"[{x}, {y}, {layer}] ({layer_name}){tile_type}"
                        unreachable_tiles.append(coords)

    if unreachable_tiles:
        xprint(overwrite=3)
        return unreachable_tiles
    else:
        xprint(type=TextType.INFO, text="No unreachable tiles found.")


def list_invalid_zone_objects() -> None:
    xprint(text="Checking for invalid zone objects…", overwrite=6)
    xprint()

    errors = {"Out of Bounds", "Void"}
    invalid_found = False

    for obj in map_data["object_data"]:
        zone_type = obj["zone_type"]
        zone_owner = obj["zone_owner"]

        if zone_type in errors or zone_owner in errors:
            invalid_found = True
            xprint(type=TextType.INFO, text=f"{obj['type']} at {obj['coords']}:")
            xprint(type=TextType.INFO, text=f"  Zone Type: {zone_type}")
            xprint(type=TextType.INFO, text=f"  Zone Owner: {zone_owner}")
            xprint()

    if not invalid_found:
        xprint(type=TextType.INFO, text="No invalid zone objects found.")
