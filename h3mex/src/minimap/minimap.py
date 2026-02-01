import msvcrt
import os
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageEnhance
from src.common import Keypress, MapZ, TextAlign, TextType, map_data
from src.defs import groups, objects
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import display_image, wait_for_keypress

from .mm_layers import MM_LAYERS
from .mm_support import (
    BLOCKED_TERRAIN_ID_OFFSET,
    KM_ID_OFFSET,
    MM_BASE2_IGNORED_OBJECTS,
    MM_OBJECT_COLORS,
    MM_STANDARD_IGNORED_OBJECTS,
    MM_TERRAIN_COLORS,
    MM_TERRAIN_COLORS_ALT,
    MP1_ID_OFFSET,
    MP2_ID_OFFSET,
    MMAction,
    MMObjectID,
    MMTerrainID,
    MMType,
    ObjectMask,
)

base_layers = {"base1g": None, "base1u": None, "base2g": None, "base2u": None}


def view() -> None:
    if os.environ.get("TERM_PROGRAM") == "vscode":
        xprint(type=TextType.ERROR, text="Minimap viewing is not supported in the VS Code terminal.")
        wait_for_keypress()
        return

    while True:
        keypress = xprint(menu=(Menu.VIEW_MINIMAP["name"], Menu.VIEW_MINIMAP["menus"][0]))
        if keypress == Keypress.ESC:
            return

        xprint(overwrite=len(Menu.VIEW_MINIMAP["menus"][0]) + 4)

        match keypress:
            case "1":
                generate(MMAction.VIEW, MMType.STANDARD, None)
            case "2":
                generate(MMAction.VIEW, MMType.EXTENDED, None)
            case "3":
                mm_overlay = {
                    "name": "types",
                    "ground": Path(os.getcwd()).parent
                    / "maps"
                    / "images"
                    / f"{map_data["filename"][:-4]}_zonetypes_g.png",
                    "underground": (
                        Path(os.getcwd()).parent / "maps" / "images" / f"{map_data["filename"][:-4]}_zonetypes_u.png"
                        if map_data["general"]["has_underground"]
                        else None
                    ),
                }
                generate(MMAction.VIEW, MMType.EXTENDED, mm_overlay)
            case "4":
                mm_overlay = {
                    "name": "players",
                    "ground": Path(os.getcwd()).parent
                    / "maps"
                    / "images"
                    / f"{map_data["filename"][:-4]}_zoneplayers_g.png",
                    "underground": (
                        Path(os.getcwd()).parent / "maps" / "images" / f"{map_data["filename"][:-4]}_zoneplayers_u.png"
                        if map_data["general"]["has_underground"]
                        else None
                    ),
                }
                generate(MMAction.VIEW, MMType.EXTENDED, mm_overlay)
        while True:
            keypress = msvcrt.getwch()
            if keypress == Keypress.ESC:
                break


def generate(mm_action: MMAction, mm_type: MMType, mm_overlay: dict | None) -> None:
    match mm_type:
        case MMType.STANDARD:
            mm_key = "standard"
            _process_image(
                mm_action,
                mm_type,
                None,
                None,
                None,
                None,
                mm_key,
                None,
                MM_LAYERS[mm_key]["display_name"],
            )
        case MMType.EXTENDED:
            for mm_number, mm_key in enumerate(MM_LAYERS.keys()):
                if mm_key == "standard":
                    continue
                mm_layer = MM_LAYERS[mm_key]
                mm_filter = mm_layer.get("filter", None)
                mm_subfilter = mm_layer.get("subfilter", None)
                mm_combofilter = mm_layer.get("combofilter", None)
                _process_image(
                    mm_action,
                    mm_type,
                    mm_filter,
                    mm_subfilter,
                    mm_combofilter,
                    mm_number,
                    mm_key,
                    mm_overlay,
                    mm_layer["display_name"],
                )


def _process_image(
    mm_action: MMAction,
    mm_type: MMType,
    mm_filter: set | None,
    mm_subfilter: set | None,
    mm_combofilter: list | None,
    mm_number: int,
    mm_key: str,
    mm_overlay: dict | None,
    mm_display_name: str,
) -> None:
    if mm_action == MMAction.EXPORT:
        if mm_type == MMType.STANDARD:
            xprint(type=TextType.ACTION, text="Generating minimap…")
        elif mm_type == MMType.EXTENDED:
            xprint(
                type=TextType.ACTION,
                text=f"Generating minimap_{mm_number:02d}_{mm_key}…",
            )

    # Get map size
    map_size = map_data["general"]["map_size"]

    # Initialize map layer list
    if map_data["general"]["has_underground"]:
        half = map_size * map_size
        terrain_data = [map_data["terrain"][:half]]  # overworld
        terrain_data.append(map_data["terrain"][half:])  # underground
    else:
        terrain_data = [map_data["terrain"]]  # overworld only

    # Initialize tile dictionaries
    tile_ownership = {
        map_z: [[None for _ in range(map_size)] for _ in range(map_size)] for map_z in [MapZ.Ground, MapZ.Underground]
    }
    blocked_tiles = {map_z: set() for map_z in [MapZ.Ground, MapZ.Underground]}

    # Filter objects if a filter is provided
    if mm_filter is not None:
        filtered_objects = [obj for obj in map_data["object_data"] if obj["id"] in mm_filter]
        if mm_subfilter is not None:
            filtered_objects = [obj for obj in filtered_objects if obj["sub_id"] in mm_subfilter]
    elif mm_combofilter is not None:
        filtered_objects = []
        for obj_id, sub_ids in mm_combofilter:
            filtered_objects.extend(
                [obj for obj in map_data["object_data"] if obj["id"] == obj_id and obj["sub_id"] in sub_ids]
            )
    else:
        filtered_objects = map_data["object_data"]

    # Iterate through objects
    for obj in filtered_objects:
        if mm_key == "base2" and (
            obj["id"] in MM_BASE2_IGNORED_OBJECTS or (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == 1001)
        ):
            continue
        elif mm_key == "border" and (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == 1001):
            continue
        # Get object masks
        def_ = map_data["object_defs"][obj["def_id"]]
        blockmask = def_["red_squares"]
        interactivemask = def_["yellow_squares"]
        # Determine if object has owner and/or should be skipped (hidden on minimap).
        # If object is valid (should be shown on minimap), process it to determine blocked tiles and set tile ownership.
        mm_objectid = _determine_owner(mm_type, obj)
        if mm_objectid is None and _should_skip_object(blockmask, interactivemask):
            continue
        _process_object(
            obj,
            blockmask,
            interactivemask,
            blocked_tiles,
            tile_ownership,
            mm_objectid,
            mm_key,
        )

    # Generate and save minimap images
    if mm_action == MMAction.VIEW:
        _view_minimap_images(mm_type, terrain_data, blocked_tiles, tile_ownership, mm_key, mm_overlay, mm_display_name)
    if mm_action == MMAction.EXPORT:
        _export_minimap_images(mm_type, terrain_data, blocked_tiles, tile_ownership, mm_number, mm_key)
        xprint(type=TextType.DONE)


def _determine_owner(mm_type: MMType, obj: dict) -> int | tuple | None:
    if (
        mm_type == MMType.STANDARD and "owner" in obj and obj["id"] not in MM_STANDARD_IGNORED_OBJECTS
    ):  # Check if object has "owner" key and should not be ignored
        return obj["owner"]
    elif mm_type == MMType.EXTENDED:
        if (
            (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] != objects.SubID.Border.Grave)
            or obj["id"] == objects.ID.Border_Guard
            or obj["id"] == objects.ID.Keymasters_Tent
        ):
            return obj["sub_id"] + KM_ID_OFFSET
        elif obj["id"] == objects.ID.Garrison or obj["id"] == objects.ID.Garrison_Vertical:
            return (MMObjectID.GARRISON, obj["owner"])
        elif obj["id"] == objects.ID.Quest_Guard:
            return MMObjectID.QUEST
        elif (
            obj["id"] == objects.ID.One_Way_MonolithPortal_Entrance
            or obj["id"] == objects.ID.One_Way_MonolithPortal_Exit
        ):
            return obj["sub_id"] + MP1_ID_OFFSET
        elif obj["id"] == objects.ID.Two_Way_MonolithPortal:
            return obj["sub_id"] + MP2_ID_OFFSET
        elif (
            obj["id"] == objects.ID.Redwood_Observatory
            and obj["sub_id"] == objects.SubID.Observation.Redwood_Observatory
        ):
            return MMObjectID.REDWOOD
        elif obj["id"] == objects.ID.Pillar_of_Fire:
            return MMObjectID.PILLAR
        elif obj["id"] == objects.ID.Mercenary_Camp:
            return MMObjectID.MERCENARY_CAMP
        elif obj["id"] == objects.ID.Marletto_Tower:
            return MMObjectID.MARLETTO_TOWER
        elif obj["id"] == objects.ID.Star_Axis:
            return MMObjectID.STAR_AXIS
        elif obj["id"] == objects.ID.Garden_of_Revelation:
            return MMObjectID.GARDEN_OF_REVELATION
        elif obj["id"] == objects.ID.School_of_War:
            return MMObjectID.SCHOOL_OF_WAR
        elif obj["id"] == objects.ID.School_of_Magic and obj["sub_id"] == 0:
            return MMObjectID.SCHOOL_OF_MAGIC_LAND
        elif obj["id"] == objects.ID.School_of_Magic and obj["sub_id"] == 1:
            return MMObjectID.SCHOOL_OF_MAGIC_SEA
        elif obj["id"] == objects.ID.Arena:
            return MMObjectID.ARENA
        elif (
            obj["id"] == objects.ID.HotA_Visitable_1
            and obj["sub_id"] == objects.SubID.HotAVisitable1.Colosseum_of_the_Magi
        ):
            return MMObjectID.COLOSSEUM_OF_THE_MAGI
        elif obj["id"] == objects.ID.Library_of_Enlightenment:
            return MMObjectID.LIBRARY_OF_ENLIGHTENMENT
        elif obj["id"] not in groups.DECOR:
            return MMObjectID.ALL_OTHERS
    else:
        return None


def _should_skip_object(blockmask: list, interactivemask: list) -> bool:
    # Skip objects that should not appear as blocked tiles on minimap:
    # - Pickups/monsters (all yellow tiles - disappear when interacted with)
    # - Magical terrain (all clear tiles - no physical presence)
    hasYellowTiles = False
    hasRedTiles = False
    hasRedOrYellowTiles = False

    for b, i in zip(blockmask, interactivemask):
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
    blockmask: list,
    interactivemask: list,
    blocked_tiles: dict,
    tile_ownership: dict,
    mm_objectid: int | tuple | None,
    mm_key: str,
) -> None:
    obj_x, obj_y, obj_z = obj["coords"]  # Get the object's coordinates
    for r in range(ObjectMask.ROWS):  # 6 rows y-axis, from top to bottom
        for c in range(ObjectMask.COLUMNS):  # 8 columns x-axis, from left to right
            index = r * 8 + c  # Calculate the index into blockmask/interactivemask
            if blockmask[index] != 1:
                blocked_tile_x = obj_x - 7 + c
                blocked_tile_y = obj_y - 5 + r
                if (
                    0 <= blocked_tile_x < map_data["general"]["map_size"]
                    and 0 <= blocked_tile_y < map_data["general"]["map_size"]
                ):  # Check if the blocked tile is within the map
                    if obj_z == MapZ.Ground:
                        blocked_tiles[MapZ.Ground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the overworld set
                        if tile_ownership[MapZ.Ground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if mm_key == "base2" and interactivemask[index] == 1:
                                tile_ownership[MapZ.Ground][obj_y - 5 + r][obj_x - 7 + c] = None
                            elif mm_key == "border" and isinstance(mm_objectid, tuple):
                                if mm_objectid[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    tile_ownership[MapZ.Ground][obj_y - 5 + r][obj_x - 7 + c] = mm_objectid[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    tile_ownership[MapZ.Ground][obj_y - 5 + r][obj_x - 7 + c] = mm_objectid[
                                        0
                                    ]  # Set to garrison color
                            else:
                                tile_ownership[MapZ.Ground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    mm_objectid if mm_objectid is not None else None
                                )
                    elif obj_z == MapZ.Underground:
                        blocked_tiles[MapZ.Underground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the underground set
                        if tile_ownership[MapZ.Underground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if mm_key == "base2" and interactivemask[index] == 1:
                                tile_ownership[MapZ.Underground][obj_y - 5 + r][obj_x - 7 + c] = None
                            elif mm_key == "border" and isinstance(mm_objectid, tuple):
                                if mm_objectid[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    tile_ownership[MapZ.Underground][obj_y - 5 + r][obj_x - 7 + c] = mm_objectid[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    tile_ownership[MapZ.Underground][obj_y - 5 + r][obj_x - 7 + c] = mm_objectid[
                                        0
                                    ]  # Set to garrison color
                            else:
                                tile_ownership[MapZ.Underground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    mm_objectid if mm_objectid is not None else None
                                )


def _view_minimap_images(
    mm_type: str,
    terrain_data: list,
    blocked_tiles: dict,
    tile_ownership: dict,
    mm_key: str,
    mm_overlay: dict | None,
    mm_display_name: str,
) -> None:
    global base_layers

    if mm_key in {"standard", "base1"}:
        xprint(text="Loading…")
    else:
        xprint(text="Loading…", overwrite=1)

    IMAGE_SIZE = 756
    GAP_SIZE = 45

    map_size = map_data["general"]["map_size"]
    transparent = (0, 0, 0, 0)

    mm_images = []
    for map_layer, terrain_chunk in enumerate(terrain_data):
        img = Image.new("RGBA", (map_size, map_size))
        for i, tile in enumerate(terrain_chunk):
            x = i % map_size
            y = i // map_size
            mm_objectid = tile_ownership[map_layer][y][x]
            color = _get_pixel_color(
                mm_type,
                mm_key,
                tile,
                mm_objectid,
                blocked_tiles,
                map_layer,
                x,
                y,
                transparent,
            )
            img.putpixel((x, y), color)

        mm_images.append(img)

    for map_layer in range(len(mm_images)):
        mm_images[map_layer] = mm_images[map_layer].resize((IMAGE_SIZE, IMAGE_SIZE), resample=Image.Resampling.NEAREST)

        if mm_key == "base1":
            if map_layer == 0:
                base_layers["base1g"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base1g"].paste(mm_images[map_layer], (0, 0))
            elif map_layer == 1:
                base_layers["base1u"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base1u"].paste(mm_images[map_layer], (0, 0))
        if mm_key == "base2":
            if map_layer == 0:
                base_layers["base2g"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base2g"].paste(mm_images[map_layer], (0, 0))
            elif map_layer == 1:
                base_layers["base2u"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base2u"].paste(mm_images[map_layer], (0, 0))

        canvas = Image.new("RGBA", mm_images[map_layer].size)
        if mm_type == MMType.EXTENDED and mm_key not in {"base1", "base2"}:
            if map_layer == 0:
                canvas.paste(base_layers["base1g"], (0, 0), base_layers["base1g"])
                canvas.paste(base_layers["base2g"], (0, 0), base_layers["base2g"])
            elif map_layer == 1:
                canvas.paste(base_layers["base1u"], (0, 0), base_layers["base1u"])
                canvas.paste(base_layers["base2u"], (0, 0), base_layers["base2u"])

        # Paste overlay images if provided
        if mm_overlay is not None and mm_key not in {"base1", "base2"}:
            if map_layer == 0:
                overlay_img = Image.open(mm_overlay["ground"])
                overlay_img = overlay_img.resize((IMAGE_SIZE, IMAGE_SIZE), resample=Image.Resampling.NEAREST)
                canvas.paste(overlay_img, (0, 0), overlay_img)
            elif map_layer == 1:
                overlay_img = Image.open(mm_overlay["underground"])
                overlay_img = overlay_img.resize((IMAGE_SIZE, IMAGE_SIZE), resample=Image.Resampling.NEAREST)
                canvas.paste(overlay_img, (0, 0), overlay_img)

        factor = 0.5 if mm_overlay is None or mm_overlay["name"] == "players" else 0.25
        canvas = ImageEnhance.Brightness(canvas).enhance(factor)

        canvas.paste(mm_images[map_layer], (0, 0), mm_images[map_layer])
        mm_images[map_layer] = canvas.convert("RGB")

    bg = Image.open(Path(os.getcwd()).parent / "h3mex" / "res" / "graphics" / "minimap_bg.png")
    minimap = bg.copy()
    minimap.paste(mm_images[0], (GAP_SIZE, GAP_SIZE))
    if len(mm_images) > 1:
        minimap.paste(mm_images[1], (IMAGE_SIZE + (GAP_SIZE * 2), GAP_SIZE))

    buffer = BytesIO()
    minimap.save(buffer, format="PNG")

    # xprint()
    if mm_type == MMType.STANDARD:
        xprint(text="STANDARD MINIMAP", align=TextAlign.CENTER, overwrite=1)
        xprint()
        display_image(buffer)
    elif mm_key not in {"base1", "base2"}:
        xprint(text=f"EXTENDED MINIMAP - {mm_display_name}", align=TextAlign.CENTER, overwrite=1)
        xprint()
        display_image(buffer)
        xprint()
        xprint()


def _export_minimap_images(
    mm_type: str,
    terrain_data: list,
    blocked_tiles: dict,
    tile_ownership: dict,
    mm_number: int,
    mm_key: str,
) -> None:

    export_path = os.path.join("exports/minimap", map_data["filename"][:-4])
    if not os.path.isdir(export_path):
        os.mkdir(export_path)
    if mm_type == MMType.EXTENDED and not os.path.isdir(export_path + "/extended"):
        os.mkdir(export_path + "/extended")

    map_size = map_data["general"]["map_size"]
    rgb_mode = "RGB" if mm_key == "base1" else "RGBA"
    transparent = (0, 0, 0, 0)

    # Determine if we're creating a combined image
    is_combined = mm_type == MMType.EXTENDED and len(terrain_data) > 1

    if is_combined:
        # Create single combined image for multiple layers
        combined_width = map_size * 2 + 2
        img = Image.new(
            rgb_mode,
            (combined_width, map_size),
            None if mm_key == "base1" else transparent,
        )

    for map_z, terrain_chunk in enumerate(terrain_data):
        if not is_combined:
            # Create separate image for each layer
            img = Image.new(
                rgb_mode,
                (map_size, map_size),
                None if mm_key == "base1" else transparent,
            )

        # Calculate x offset for combined images (0 for ground, map_size + 2 for underground)
        x_offset = (map_size + 2) * map_z if is_combined else 0

        # Process each pixel in the layer
        for i, tile in enumerate(terrain_chunk):
            x = i % map_size
            y = i // map_size
            mm_objectid = tile_ownership[map_z][y][x]
            color = _get_pixel_color(
                mm_type,
                mm_key,
                tile,
                mm_objectid,
                blocked_tiles,
                map_z,
                x,
                y,
                transparent,
            )
            img.putpixel((x + x_offset, y), color)

        # Save layer image(s)
        if mm_type == MMType.STANDARD:
            map_z_letter = "g" if map_z == 0 else "u"
            img.save(os.path.join(f"{export_path}", f"{map_data["filename"][:-4]}_{map_z_letter}.png"))
        elif mm_type == MMType.EXTENDED:
            img.save(
                os.path.join(
                    f"{export_path}/extended",
                    f"{mm_number:02d}_{mm_key}.png",
                )
            )


def _get_pixel_color(
    mm_type: str,
    mm_key: str,
    tile: tuple,
    mm_objectid: int,
    blocked_tiles: dict,
    map_z: int,
    x: int,
    y: int,
    transparent: tuple,
) -> tuple:
    if mm_type == MMType.STANDARD:
        if mm_objectid is not None:
            return MM_OBJECT_COLORS[mm_objectid]
        elif (x, y) in blocked_tiles[map_z]:
            return MM_TERRAIN_COLORS[MMTerrainID(tile["terrain_type"]) + BLOCKED_TERRAIN_ID_OFFSET]
        else:
            return MM_TERRAIN_COLORS[tile["terrain_type"]]
    elif mm_type == MMType.EXTENDED:
        if mm_key == "base1":
            if (x, y) in blocked_tiles[map_z]:
                return MM_TERRAIN_COLORS_ALT[MMTerrainID(tile["terrain_type"]) + BLOCKED_TERRAIN_ID_OFFSET]
            else:
                return MM_TERRAIN_COLORS_ALT[tile["terrain_type"]]
        elif mm_key == "base2":
            if mm_objectid == MMObjectID.ALL_OTHERS:
                color = MM_TERRAIN_COLORS_ALT[MMTerrainID(tile["terrain_type"]) + BLOCKED_TERRAIN_ID_OFFSET]
                if color == MM_TERRAIN_COLORS_ALT[MMTerrainID.BROCK]:
                    return transparent
                return color
            else:
                return transparent
        else:
            if mm_objectid is not None:
                return MM_OBJECT_COLORS[mm_objectid] + (255,)
            else:
                return transparent
