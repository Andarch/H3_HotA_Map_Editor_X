import os
from io import BytesIO
from pathlib import Path

from PIL import Image
from src.common import Keypress, MapLayer, map_data
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import display_image, wait_for_keypress

from .mmdefs import ObjectGroup, ObjectRGB, OtherObjects, TerrainRGB


def view() -> bool:
    while True:
        keypress = xprint(menu=(Menu.MINIMAP_VIEW["name"], Menu.MINIMAP_VIEW["menus"][0]))
        if keypress == Keypress.ESC:
            return

        xprint(overwrite=len(Menu.MINIMAP_VIEW["menus"][0]) + 4)

        match keypress:
            case "1":
                minimaps = _generate_standard_minimap()

        _display_minimap(minimaps)
        wait_for_keypress()


def export() -> bool:
    pass


def _generate_standard_minimap() -> list:
    map_size = map_data["general"]["map_size"]
    if map_data["general"]["has_underground"]:
        half = map_size * map_size
        terrain_layers = [map_data["terrain"][:half], map_data["terrain"][half:]]
    else:
        terrain_layers = [map_data["terrain"]]
    owners = {
        layer: [[None for _ in range(map_size)] for _ in range(map_size)]
        for layer in [MapLayer.Ground, MapLayer.Underground]
    }
    blocked_tiles = {layer: set() for layer in [MapLayer.Ground, MapLayer.Underground]}
    for obj in map_data["object_data"]:
        def_ = map_data["object_defs"][obj["def_id"]]
        blockMask = def_["red_squares"]
        interactiveMask = def_["yellow_squares"]
        owner = None
        if "owner" in obj and obj["id"] not in ObjectGroup.IGNORED_STANDARD:
            owner = obj["owner"]
        if owner is None and _should_skip_object(blockMask, interactiveMask):
            continue
        _process_object(obj, blockMask, interactiveMask, blocked_tiles, owners, owner, png_layer="standard")
    minimaps = []
    for layer_index, layer in enumerate(terrain_layers):
        img = Image.new("RGB", (map_size, map_size))
        for i, tile in enumerate(layer):
            x = i % map_size
            y = i // map_size
            owner = owners[layer_index][y][x]
            if owner is not None:
                if owner in ObjectRGB.player:
                    color = ObjectRGB.player[owner]
            elif (x, y) in blocked_tiles[layer_index]:
                color = TerrainRGB.blocked[tile["terrain_type"]]
            else:
                color = TerrainRGB.passable[tile["terrain_type"]]
            img.putpixel((x, y), color)
        minimaps.append(img)
    return minimaps


# def export(export_type: str) -> None:
#     if export_type == "Standard":
#         _process_image(export_type, None, None, None, None)
#     elif export_type == "Extended":
#         _process_image(export_type, Decor.IDS, None, 1, "base1")
#         _process_image(export_type, None, None, 2, "base2")
#         _process_image(export_type, border_objects, None, 3, "border")
#         _process_image(export_type, {Objects.Keymasters_Tent}, None, 4, "tents")
#         _process_image(export_type, {Objects.Monolith_One_Way_Entrance}, None, 5, "portals1en")
#         _process_image(export_type, {Objects.Monolith_One_Way_Exit}, None, 6, "portals1ex")
#         _process_image(export_type, {Objects.Two_Way_Monolith}, two_way_land_portals, 7, "portals2land")
#         _process_image(export_type, {Objects.Two_Way_Monolith}, two_way_sea_portals, 8, "portals2water")
#         _process_image(export_type, {Objects.Whirlpool}, None, 9, "whirlpools")
#         _process_image(export_type, {Objects.Prison}, None, 10, "prisons")
#         _process_image(export_type, monster_objects, None, 11, "monsters")
#         _process_image(export_type, {Objects.Spell_Scroll}, None, 12, "spellscrolls")
#         _process_image(export_type, {Objects.Shrines}, {Shrines.Shrine_of_Magic_Incantation}, 13, "shrine1")
#         _process_image(export_type, {Objects.Shrine_of_Magic_Gesture}, None, 14, "shrine2")
#         _process_image(export_type, {Objects.Shrine_of_Magic_Thought}, None, 15, "shrine3")
#         _process_image(export_type, {Objects.Shrines}, {Shrines.Shrine_of_Magic_Mystery}, 16, "shrine4")
#         _process_image(export_type, {Objects.Pyramid}, None, 17, "pyramids")
#         _process_image(export_type, {Objects.Artifact}, None, 18, "artifacts")
#         _process_image(export_type, {Objects.Random_Artifact}, None, 19, "randomartifacts")
#         _process_image(export_type, {Objects.Random_Treasure_Artifact}, None, 20, "randomtreasureartifacts")
#         _process_image(export_type, {Objects.Random_Minor_Artifact}, None, 21, "randomminorartifacts")
#         _process_image(export_type, {Objects.Random_Major_Artifact}, None, 22, "randommajorartifacts")
#         _process_image(export_type, {Objects.Random_Relic}, None, 23, "randomrelics")
#         _process_image(export_type, resource_objects, None, 24, "resources")
#         _process_image(export_type, {Objects.Treasure_Chest}, None, 25, "treasurechests")
#         _process_image(export_type, {Objects.Event}, None, 26, "eventobjects")
#     return True


# def _process_image(export_type: str, filter: set, subfilter: set | None, png_number: int, png_name: str) -> bool:
#     if export_type == "Standard":
#         xprint(type=MsgType.ACTION, text="Generating minimap…")
#     elif export_type == "Extended":
#         xprint(
#             type=MsgType.ACTION,
#             text=f"Generating minimap_{png_number:02d}_{png_name}…",
#         )
#     # Get map size
#     map_size = map_data["general"]["map_size"]
#     # Initialize map layer list
#     if map_data["general"]["has_underground"]:
#         half = map_size * map_size
#         map_layers = [map_data["terrain"][:half]]  # overworld
#         map_layers.append(map_data["terrain"][half:])  # underground
#     else:
#         map_layers = [map_data["terrain"]]  # overworld only
#     # Initialize tile dictionaries
#     ownership = {
#         map_layer: [[None for _ in range(map_size)] for _ in range(map_size)] for map_layer in [MapLayer.GROUND, MapLayer.Underground]
#     }
#     blocked_tiles = {map_layer: set() for map_layer in [MapLayer.GROUND, MapLayer.Underground]}
#     # Filter objects if a filter is provided
#     if filter is None:
#         filtered_objects = map_data["object_data"]
#     else:
#         filtered_objects = [obj for obj in map_data["object_data"] if obj["id"] in filter]
#     # Apply subfilter if provided
#     if subfilter is not None:
#         filtered_objects = [obj for obj in filtered_objects if obj["sub_id"] in subfilter]
#     # Iterate through objects
#     for obj in filtered_objects:
#         if png_name == "base2" and (
#             obj["id"] in ignored_objects_base2 or (obj["id"] == Objects.Border_Gate and obj["sub_id"] == 1001)
#         ):
#             continue
#         elif png_name == "border" and (obj["id"] == Objects.Border_Gate and obj["sub_id"] == 1001):
#             continue
#         # Get object masks
#         def_ = map_data["object_defs"][obj["def_id"]]
#         blockMask = def_["red_squares"]
#         interactiveMask = def_["yellow_squares"]
#         # Determine if object has owner and/or should be skipped (hidden on minimap).
#         # If object is valid (should be shown on minimap), process it to determine blocked tiles and set tile ownership.
#         owner = _determine_owner(export_type, obj)
#         if owner is None and _should_skip_object(blockMask, interactiveMask):
#             continue
#         _process_object(
#             obj,
#             blockMask,
#             interactiveMask,
#             blocked_tiles,
#             ownership,
#             owner,
#             png_name,
#         )
#     # Generate and save minimap images
#     _generate_images(export_type, map_layers, blocked_tiles, ownership, png_number, png_name)
#     xprint(type=MsgType.DONE)
#     return True


# def _determine_owner(export_type: str, obj: dict) -> int | tuple | None:
#     if (
#         export_type == "Standard" and "owner" in obj and obj["id"] not in ignored_objects_standard
#     ):  # Check if object has "owner" key and should not be ignored
#         return obj["owner"]
#     elif export_type == "Extended":
#         if (
#             (obj["id"] == Objects.Border_Gate and obj["sub_id"] != 1001)
#             or obj["id"] == Objects.Border_Guard
#             or obj["id"] == Objects.Keymasters_Tent
#         ):
#             return obj["sub_id"] + 1000
#         elif obj["id"] == Objects.Garrison or obj["id"] == Objects.Garrison_Vertical:
#             return (1999, obj["owner"])
#         elif obj["id"] == Objects.Quest_Guard:
#             return 2000
#         elif obj["id"] == Objects.Monolith_One_Way_Entrance or obj["id"] == Objects.Monolith_One_Way_Exit:
#             return obj["sub_id"] + 3000
#         elif obj["id"] == Objects.Two_Way_Monolith:
#             return obj["sub_id"] + 3500
#         elif obj["id"] not in Decor.IDS:
#             return 10000
#     else:
#         return None


def _should_skip_object(blockMask: list, interactiveMask: list) -> bool:
    isInteractive = False
    yellowSquaresOnly = True
    allPassable = True
    for b, i in zip(blockMask, interactiveMask):  # Iterate through the mask bits
        if i == 1:  # If there is an interactive tile
            isInteractive = True
        if b == i:  # If the elements are the same, then one is not the inverse of the other
            yellowSquaresOnly = False
        if b != 1:  # If there is a blocked tile
            allPassable = False
        if isInteractive and not yellowSquaresOnly and not allPassable:
            break
    return isInteractive and yellowSquaresOnly


def _process_object(
    obj: dict,
    blockMask: list,
    interactiveMask: list,
    blocked_tiles: dict,
    ownership: dict,
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
                    if obj_z == MapLayer.Ground:
                        blocked_tiles[MapLayer.Ground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the overworld set
                        if ownership[MapLayer.Ground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if png_layer == "base2" and interactiveMask[index] == 1:
                                ownership[MapLayer.Ground][obj_y - 5 + r][obj_x - 7 + c] = OtherObjects.Interactive
                            elif png_layer == "border" and isinstance(owner, tuple):
                                if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    ownership[MapLayer.Ground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    ownership[MapLayer.Ground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        0
                                    ]  # Set to garrison color
                            else:
                                ownership[MapLayer.Ground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    owner if owner is not None else None
                                )
                    elif obj_z == MapLayer.Underground:
                        blocked_tiles[MapLayer.Underground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the underground set
                        if ownership[MapLayer.Underground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if png_layer == "base2" and interactiveMask[index] == 1:
                                ownership[MapLayer.Underground][obj_y - 5 + r][obj_x - 7 + c] = OtherObjects.Interactive
                            elif png_layer == "border" and isinstance(owner, tuple):
                                if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    ownership[MapLayer.Underground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    ownership[MapLayer.Underground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        0
                                    ]  # Set to garrison color
                            else:
                                ownership[MapLayer.Underground][obj_y - 5 + r][obj_x - 7 + c] = (
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
    display_image(buffer)


# def _generate_images(
#     export_type: str,
#     map_layers: list,
#     blocked_tiles: dict,
#     ownership: dict,
#     png_number: int,
#     png_name: str,
# ) -> None:
#     IMAGES_PATH = "exports/minimap"

#     map_size = map_data["general"]["map_size"]
#     mode = "RGB" if png_name == "base1" else "RGBA"
#     transparent = (0, 0, 0, 0)
#     map_name = map_data["filename"][:-4] if map_data["filename"].endswith(".h3m") else map_data["filename"]

#     # Determine if we're creating a combined image
#     is_combined = export_type == "Extended" and len(map_layers) > 1

#     if is_combined:
#         # Create single combined image for multiple layers
#         combined_width = map_size * 2 + 2
#         img = Image.new(
#             mode,
#             (combined_width, map_size),
#             None if png_name == "base1" else transparent,
#         )

#     for map_layer_index, map_layer in enumerate(map_layers):
#         if not is_combined:
#             # Create separate image for each layer
#             img = Image.new(
#                 mode,
#                 (map_size, map_size),
#                 None if png_name == "base1" else transparent,
#             )

#         # Calculate x offset for combined images (0 for ground, map_size + 2 for underground)
#         x_offset = (map_size + 2) * map_layer_index if is_combined else 0

#         # Process each pixel in the layer
#         for i, tile in enumerate(map_layer):
#             x = i % map_size
#             y = i // map_size
#             owner = ownership[map_layer_index][y][x]
#             color = _get_pixel_color(
#                 export_type,
#                 png_name,
#                 tile,
#                 owner,
#                 blocked_tiles,
#                 map_layer_index,
#                 x,
#                 y,
#                 transparent,
#             )
#             img.putpixel((x + x_offset, y), color)

#         if not is_combined:
#             # Save individual layer image
#             layer_letter = "g" if map_layer_index == 0 else "u"
#             if export_type == "Standard":
#                 img.save(os.path.join(IMAGES_PATH, f"{map_name}_{layer_letter}.png"))
#             elif export_type == "Extended":
#                 img.save(
#                     os.path.join(
#                         IMAGES_PATH,
#                         f"{map_name}_{layer_letter}_{png_number:02d}_{png_name}.png",
#                     )
#                 )

#     if is_combined:
#         # Save combined image
#         img.save(
#             os.path.join(
#                 IMAGES_PATH,
#                 f"{map_name}_{png_number:02d}_{png_name}.png",
#             )
#         )


# def _get_pixel_color(
#     export_type: str,
#     png_name: str,
#     tile: tuple,
#     owner: int,
#     blocked_tiles: dict,
#     map_layer_index: int,
#     x: int,
#     y: int,
#     transparent: tuple,
# ) -> tuple:
#     if export_type == "Standard":
#         if owner is not None:
#             return object_colors[owner]
#         elif (x, y) in blocked_tiles[map_layer_index]:
#             return terrain_colors[TERRAIN(tile["terrain_type"]) + 20]
#         else:
#             return terrain_colors[tile["terrain_type"]]
#     elif export_type == "Extended":
#         if png_name == "base1":
#             if (x, y) in blocked_tiles[map_layer_index]:
#                 return terrain_colors_alt[TERRAIN(tile["terrain_type"]) + 20]
#             else:
#                 return terrain_colors_alt[tile["terrain_type"]]
#         elif png_name == "base2":
#             if owner == OBJECTS.ALL_OTHERS:
#                 color = terrain_colors_alt[TERRAIN(tile["terrain_type"]) + 20]
#                 if color == TERRAIN.BROCK:
#                     return transparent
#                 return color
#             else:
#                 return transparent
#         else:
#             if owner is not None:
#                 return object_colors[owner] + (255,)
#             else:
#                 return transparent
