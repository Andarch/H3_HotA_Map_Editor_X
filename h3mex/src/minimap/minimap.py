import os
from io import BytesIO
from pathlib import Path

from PIL import Image
from src.common import Keypress, Layer, TextType, map_data
from src.defs import groups, objects
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import display_image, wait_for_keypress

from .mmdefs import ObjectRGB, OtherObjects, TerrainRGB


def view() -> bool:
    while True:
        keypress = xprint(menu=(Menu.VIEW_MINIMAP["name"], Menu.VIEW_MINIMAP["menus"][0]))
        if keypress == Keypress.ESC:
            return

        xprint(overwrite=len(Menu.VIEW_MINIMAP["menus"][0]) + 4)

        match keypress:
            case "1":
                minimaps = _generate_minimap_images("Standard")
            case "2":
                minimaps = _generate_minimap_images("Extended")

        _display_minimap(minimaps)
        wait_for_keypress()


def export() -> bool:
    pass


def _generate_minimap_images(export_type: str) -> list:
    xprint(text="Loading minimap…")

    map_size = map_data["general"]["map_size"]
    if map_data["general"]["has_underground"]:
        half = map_size * map_size
        terrain_layers = [map_data["terrain"][:half], map_data["terrain"][half:]]
    else:
        terrain_layers = [map_data["terrain"]]

    owners = {
        layer: [[None for _ in range(map_size)] for _ in range(map_size)] for layer in [Layer.Ground, Layer.Underground]
    }
    blocked_tiles = {layer: set() for layer in [Layer.Ground, Layer.Underground]}

    for obj in map_data["object_data"]:
        obj_def = map_data["object_defs"][obj["def_id"]]
        block_mask = obj_def["red_squares"]
        interactive_mask = obj_def["yellow_squares"]
        owner = obj["owner"] if "owner" in obj else None

        obj_color = _get_obj_color(export_type, obj)
        if obj_color is None and _should_skip_object(block_mask, interactive_mask):
            continue
        _process_object(obj, block_mask, interactive_mask, blocked_tiles, owners, obj_color, png_layer="standard")

    minimap_images = []
    for layer_index, layer in enumerate(terrain_layers):
        img = Image.new("RGB", (map_size, map_size))
        for i, tile in enumerate(layer):
            x = i % map_size
            y = i // map_size
            obj_color = owners[layer_index][y][x]

            if obj_color is not None:
                if obj_color in ObjectRGB.player:
                    color = ObjectRGB.player[obj_color]
            elif (x, y) in blocked_tiles[layer_index]:
                color = TerrainRGB.blocked[tile["terrain_type"]]
            else:
                color = TerrainRGB.passable[tile["terrain_type"]]
            img.putpixel((x, y), color)

        minimap_images.append(img)
    return minimap_images


def _get_obj_color(mode: str, obj: dict) -> int | tuple | None:
    match mode:
        case "Standard":
            if "owner" in obj and obj["id"] not in groups.HEROES:
                return obj["owner"]
            else:
                return None
        case "Extended":
            if (
                (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] != objects.SubID.Border.Grave)
                or obj["id"] == objects.ID.Border_Guard
                or obj["id"] == objects.ID.Keymasters_Tent
            ):
                return obj["sub_id"] + 1000
            elif obj["id"] == objects.ID.Garrison or obj["id"] == objects.ID.Garrison_Vertical:
                return (1999, obj["owner"])
            elif obj["id"] == objects.ID.Quest_Guard:
                return 2000
            elif obj["id"] == objects.ID.One_Way_Portal_Entrance or obj["id"] == objects.ID.One_Way_Portal_Exit:
                return obj["sub_id"] + 3000
            elif obj["id"] == objects.ID.Two_Way_Portal:
                return obj["sub_id"] + 3500
            elif obj["id"] not in groups.DECOR:
                return 10000
            else:
                return None


"""
def _should_skip_object(blockMask: list, interactiveMask: list) -> bool:
    isInteractive = False
    yellowTilesOnly = True
    allPassable = True
    for b, i in zip(blockMask, interactiveMask):  # Iterate through the mask bits
        if i == 1:  # If there is an interactive tile
            isInteractive = True
        if b == i:  # If the elements are the same, then one is not the inverse of the other
            yellowTilesOnly = False
        if b != 1:  # If there is a blocked tile
            allPassable = False
        if isInteractive and not yellowTilesOnly and not allPassable:
            break
    return isInteractive and yellowTilesOnly
"""


def _should_skip_object(blockMask: list, interactiveMask: list) -> bool:
    # Skip objects that should not appear as blocked tiles on minimap:
    # - Pickups/monsters (all yellow tiles - disappear when interacted with)
    # - Magical terrain (all clear tiles - no physical presence)
    hasYellowTiles = False
    hasRedTiles = False
    hasRedOrYellowTiles = False

    for b, i in zip(blockMask, interactiveMask):
        if i == 1:  # Interactive (yellow) tile
            hasYellowTiles = True
        if b == 0 and i == 0:  # Red (blocked, non-interactive) tile
            hasRedTiles = True
        if b == 0:  # Any blocked tile (red or yellow)
            hasRedOrYellowTiles = True

        # Early exit: if we found a red tile, it's a permanent structure
        if hasRedTiles:
            return False

    # Skip if: (all yellow with no red) OR (all clear tiles)
    return (hasYellowTiles and not hasRedTiles) or not hasRedOrYellowTiles


def _process_object(
    obj: dict,
    blockMask: list,
    interactiveMask: list,
    blocked_tiles: dict,
    owners: dict,
    owner: int | tuple | None,
    png_layer="",
) -> None:
    obj_x, obj_y, obj_z = obj["coords"]  # Get the object's coordinates
    for r in range(6):  # 6 rows y-axis, from top to bottom
        for c in range(8):  # 8 columns x-axis, from left to right
            index = r * 8 + c  # Calculate the index into blockMask/interactiveMask
            if blockMask[index] != 1:
                blocked_tile_x = obj_x - 7 + c
                blocked_tile_y = obj_y - 5 + r
                if (
                    0 <= blocked_tile_x < map_data["general"]["map_size"]
                    and 0 <= blocked_tile_y < map_data["general"]["map_size"]
                ):  # Check if the blocked tile is within the map
                    if obj_z == Layer.Ground:
                        blocked_tiles[Layer.Ground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the overworld set
                        if owners[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if png_layer == "base2" and interactiveMask[index] == 1:
                                owners[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = OtherObjects.Interactive
                            elif png_layer == "border" and isinstance(owner, tuple):
                                if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    owners[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = owner[1]  # Set to owner color
                                else:  # Outer tiles
                                    owners[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        0
                                    ]  # Set to garrison color
                            else:
                                owners[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    owner if owner is not None else None
                                )
                    elif obj_z == Layer.Underground:
                        blocked_tiles[Layer.Underground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the underground set
                        if owners[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if png_layer == "base2" and interactiveMask[index] == 1:
                                owners[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = OtherObjects.Interactive
                            elif png_layer == "border" and isinstance(owner, tuple):
                                if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    owners[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    owners[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        0
                                    ]  # Set to garrison color
                            else:
                                owners[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    owner if owner is not None else None
                                )


def _display_minimap(minimaps: list) -> None:
    for layer in range(len(minimaps)):
        minimaps[layer] = minimaps[layer].resize((370, 370), resample=Image.Resampling.NEAREST)
        if minimaps[layer].mode == "RGBA":
            canvas = Image.new("RGB", minimaps[layer].size)
            canvas.paste(minimaps[layer], (0, 0))
            minimaps[layer] = canvas

    bg = Image.open(Path(os.getcwd()).parent / "h3mex" / "res" / "graphics" / "minimap_bg.png")
    minimap = bg.copy()
    minimap.paste(minimaps[0], (20, 20))
    if len(minimaps) > 1:
        minimap.paste(minimaps[1], (410, 20))

    buffer = BytesIO()
    minimap.save(buffer, format="PNG")

    xprint(overwrite=2)
    display_image(buffer)


"""
def export(export_type: str) -> None:
    if export_type == "Standard":
        _process_image(export_type, None, None, None, None)
    elif export_type == "Extended":
        _process_image(export_type, Decor.IDS, None, 1, "base1")
        _process_image(export_type, None, None, 2, "base2")
        _process_image(export_type, border_objects, None, 3, "border")
        _process_image(export_type, {Objects.Keymasters_Tent}, None, 4, "tents")
        _process_image(export_type, {Objects.Monolith_One_Way_Entrance}, None, 5, "portals1en")
        _process_image(export_type, {Objects.Monolith_One_Way_Exit}, None, 6, "portals1ex")
        _process_image(export_type, {Objects.Two_Way_Monolith}, two_way_land_portals, 7, "portals2land")
        _process_image(export_type, {Objects.Two_Way_Monolith}, two_way_sea_portals, 8, "portals2water")
        _process_image(export_type, {Objects.Whirlpool}, None, 9, "whirlpools")
        _process_image(export_type, {Objects.Prison}, None, 10, "prisons")
        _process_image(export_type, monster_objects, None, 11, "monsters")
        _process_image(export_type, {Objects.Spell_Scroll}, None, 12, "spellscrolls")
        _process_image(export_type, {Objects.Shrines}, {Shrines.Shrine_of_Magic_Incantation}, 13, "shrine1")
        _process_image(export_type, {Objects.Shrine_of_Magic_Gesture}, None, 14, "shrine2")
        _process_image(export_type, {Objects.Shrine_of_Magic_Thought}, None, 15, "shrine3")
        _process_image(export_type, {Objects.Shrines}, {Shrines.Shrine_of_Magic_Mystery}, 16, "shrine4")
        _process_image(export_type, {Objects.Pyramid}, None, 17, "pyramids")
        _process_image(export_type, {Objects.Artifact}, None, 18, "artifacts")
        _process_image(export_type, {Objects.Random_Artifact}, None, 19, "randomartifacts")
        _process_image(export_type, {Objects.Random_Treasure_Artifact}, None, 20, "randomtreasureartifacts")
        _process_image(export_type, {Objects.Random_Minor_Artifact}, None, 21, "randomminorartifacts")
        _process_image(export_type, {Objects.Random_Major_Artifact}, None, 22, "randommajorartifacts")
        _process_image(export_type, {Objects.Random_Relic}, None, 23, "randomrelics")
        _process_image(export_type, resource_objects, None, 24, "resources")
        _process_image(export_type, {Objects.Treasure_Chest}, None, 25, "treasurechests")
        _process_image(export_type, {Objects.Event}, None, 26, "eventobjects")
    return True
"""


def _process_image(export_type: str, filter: set, subfilter: set | None, png_number: int, png_name: str) -> bool:
    if export_type == "Standard":
        xprint(type=TextType.ACTION, text="Generating minimap…")
    elif export_type == "Extended":
        xprint(
            type=TextType.ACTION,
            text=f"Generating minimap_{png_number:02d}_{png_name}…",
        )
    # Get map size
    map_size = map_data["general"]["map_size"]
    # Initialize map layer list
    if map_data["general"]["has_underground"]:
        half = map_size * map_size
        map_layers = [map_data["terrain"][:half]]  # overworld
        map_layers.append(map_data["terrain"][half:])  # underground
    else:
        map_layers = [map_data["terrain"]]  # overworld only
    # Initialize tile dictionaries
    ownership = {
        map_layer: [[None for _ in range(map_size)] for _ in range(map_size)]
        for map_layer in [Layer.GROUND, Layer.Underground]
    }
    blocked_tiles = {map_layer: set() for map_layer in [Layer.GROUND, Layer.Underground]}
    # Filter objects if a filter is provided
    if filter is None:
        filtered_objects = map_data["object_data"]
    else:
        filtered_objects = [obj for obj in map_data["object_data"] if obj["id"] in filter]
    # Apply subfilter if provided
    if subfilter is not None:
        filtered_objects = [obj for obj in filtered_objects if obj["sub_id"] in subfilter]
    # Iterate through objects
    for obj in filtered_objects:
        if png_name == "base2" and (
            obj["id"] in ObjectGroups.IGNORED_EXT_BASE2
            or (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == 1001)
        ):
            continue
        elif png_name == "border" and (
            obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == objects.SubID.Border.Grave
        ):
            continue
        # Get object masks
        def_ = map_data["object_defs"][obj["def_id"]]
        blockMask = def_["red_squares"]
        interactiveMask = def_["yellow_squares"]
        # Determine if object has owner and/or should be skipped (hidden on minimap).
        # If object is valid (should be shown on minimap), process it to determine blocked tiles and set tile ownership.
        owner = _get_obj_color(export_type, obj)
        if owner is None and _should_skip_object(blockMask, interactiveMask):
            continue
        _process_object(
            obj,
            blockMask,
            interactiveMask,
            blocked_tiles,
            ownership,
            owner,
            png_name,
        )
    # Generate and save minimap images
    # _generate_images(export_type, map_layers, blocked_tiles, ownership, png_number, png_name)
    xprint(type=TextType.DONE)
    return True


"""
def _generate_images(
    export_type: str,
    map_layers: list,
    blocked_tiles: dict,
    ownership: dict,
    png_number: int,
    png_name: str,
) -> None:
    IMAGES_PATH = "exports/minimap"

    map_size = map_data["general"]["map_size"]
    mode = "RGB" if png_name == "base1" else "RGBA"
    transparent = (0, 0, 0, 0)
    map_name = map_data["filename"][:-4] if map_data["filename"].endswith(".h3m") else map_data["filename"]

    # Determine if we're creating a combined image
    is_combined = export_type == "Extended" and len(map_layers) > 1

    if is_combined:
        # Create single combined image for multiple layers
        combined_width = map_size * 2 + 2
        img = Image.new(
            mode,
            (combined_width, map_size),
            None if png_name == "base1" else transparent,
        )

    for map_layer_index, map_layer in enumerate(map_layers):
        if not is_combined:
            # Create separate image for each layer
            img = Image.new(
                mode,
                (map_size, map_size),
                None if png_name == "base1" else transparent,
            )

        # Calculate x offset for combined images (0 for ground, map_size + 2 for underground)
        x_offset = (map_size + 2) * map_layer_index if is_combined else 0

        # Process each pixel in the layer
        for i, tile in enumerate(map_layer):
            x = i % map_size
            y = i // map_size
            owner = ownership[map_layer_index][y][x]
            color = _get_pixel_color(
                export_type,
                png_name,
                tile,
                owner,
                blocked_tiles,
                map_layer_index,
                x,
                y,
                transparent,
            )
            img.putpixel((x + x_offset, y), color)

        if not is_combined:
            # Save individual layer image
            layer_letter = "g" if map_layer_index == 0 else "u"
            if export_type == "Standard":
                img.save(os.path.join(IMAGES_PATH, f"{map_name}_{layer_letter}.png"))
            elif export_type == "Extended":
                img.save(
                    os.path.join(
                        IMAGES_PATH,
                        f"{map_name}_{layer_letter}_{png_number:02d}_{png_name}.png",
                    )
                )

    if is_combined:
        # Save combined image
        img.save(
            os.path.join(
                IMAGES_PATH,
                f"{map_name}_{png_number:02d}_{png_name}.png",
            )
        )


def _get_pixel_color(
    export_type: str,
    png_name: str,
    tile: tuple,
    owner: int,
    blocked_tiles: dict,
    map_layer_index: int,
    x: int,
    y: int,
    transparent: tuple,
) -> tuple:
    if export_type == "Standard":
        if owner is not None:
            return object_colors[owner]
        elif (x, y) in blocked_tiles[map_layer_index]:
            return terrain_colors[TERRAIN(tile["terrain_type"]) + 20]
        else:
            return terrain_colors[tile["terrain_type"]]
    elif export_type == "Extended":
        if png_name == "base1":
            if (x, y) in blocked_tiles[map_layer_index]:
                return terrain_colors_alt[TERRAIN(tile["terrain_type"]) + 20]
            else:
                return terrain_colors_alt[tile["terrain_type"]]
        elif png_name == "base2":
            if owner == OBJECTS.ALL_OTHERS:
                color = terrain_colors_alt[TERRAIN(tile["terrain_type"]) + 20]
                if color == TERRAIN.BROCK:
                    return transparent
                return color
            else:
                return transparent
        else:
            if owner is not None:
                return object_colors[owner] + (255,)
            else:
                return transparent
"""
