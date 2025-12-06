import os
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageEnhance
from src.common import Keypress, Layer, TextAlign, TextType, map_data
from src.defs import groups, objects
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import display_image, wait_for_keypress

from .mmsupport import (
    BLOCKED_TERRAIN_ID_OFFSET,
    IGNORED_OBJECTS_EXTENDED_MM_BASE2,
    IGNORED_OBJECTS_STANDARD_MM,
    OBJECT_COLORS,
    TERRAIN_COLORS,
    TERRAIN_COLORS_ALT,
    MaskSize,
    MinimapObjectID,
    MinimapTerrainID,
)


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
                generate("View", "Standard")
            case "2":
                generate("View", "Extended")

        wait_for_keypress()


def generate(generate_type: str, minimap_type: str) -> None:
    if minimap_type == "Standard":
        _process_image(generate_type, minimap_type, None, None, None, None)
    elif minimap_type == "Extended":
        num = 1
        _process_image(generate_type, minimap_type, groups.DECOR, None, num, "base1")

        num += 1
        _process_image(generate_type, minimap_type, None, None, num, "base2")

        num += 1
        _process_image(generate_type, minimap_type, groups.BORDER, None, num, "border")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Keymasters_Tent}, None, num, "tents")

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.One_Way_MonolithPortal_Entrance},
            groups.ONE_WAY_MONOLITHS,
            num,
            "monoliths1_en",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.One_Way_MonolithPortal_Exit},
            groups.ONE_WAY_MONOLITHS,
            num,
            "monoliths1_ex",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.One_Way_MonolithPortal_Entrance},
            groups.ONE_WAY_PORTALS,
            num,
            "portals1_en",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.One_Way_MonolithPortal_Exit},
            groups.ONE_WAY_PORTALS,
            num,
            "portals1_ex",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Two_Way_MonolithPortal},
            groups.TWO_WAY_MONOLITHS,
            num,
            "monoliths2",
        )

        num += 1
        _process_image(
            generate_type, minimap_type, {objects.ID.Two_Way_MonolithPortal}, groups.TWO_WAY_PORTALS, num, "portals2"
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Two_Way_MonolithPortal},
            groups.TWO_WAY_SEA_PORTALS,
            num,
            "portals2_sea",
        )

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Whirlpool}, None, num, "whirlpools")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Prison}, None, num, "prisons")

        num += 1
        _process_image(generate_type, minimap_type, groups.MONSTERS, None, num, "monsters")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Spell_Scroll}, None, num, "spellscrolls")

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Shrine_1_and_4},
            {objects.SubID.Shrine_1_and_4.Shrine_of_Magic_Incantation},
            num,
            "shrine1",
        )

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Shrine_of_Magic_Gesture}, None, num, "shrine2")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Shrine_of_Magic_Thought}, None, num, "shrine3")

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Shrine_1_and_4},
            {objects.SubID.Shrine_1_and_4.Shrine_of_Magic_Mystery},
            num,
            "shrine4",
        )

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Pyramid}, None, num, "pyramids")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Artifact}, None, num, "artifacts")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Random_Artifact}, None, num, "randomartifacts")

        num += 1
        _process_image(
            generate_type, minimap_type, {objects.ID.Random_Treasure_Artifact}, None, num, "randomtreasureartifacts"
        )

        num += 1
        _process_image(
            generate_type, minimap_type, {objects.ID.Random_Minor_Artifact}, None, num, "randomminorartifacts"
        )

        num += 1
        _process_image(
            generate_type, minimap_type, {objects.ID.Random_Major_Artifact}, None, num, "randommajorartifacts"
        )

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Random_Relic}, None, num, "randomrelics")

        num += 1
        _process_image(generate_type, minimap_type, groups.RESOURCES, None, num, "resources")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Treasure_Chest}, None, num, "treasurechests")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Scholar}, None, num, "scholars")

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Event}, None, num, "eventobjects")

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Trading_Post, objects.ID.Trading_Post_Snow},
            None,
            num,
            "tradingposts",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.HotA_Visitable_1},
            {objects.SubID.HotAVisitable1.Warlocks_Lab},
            num,
            "warlockslabs",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Redwood_Observatory},
            None,
            num,
            "redwoodobservatories",
        )

        num += 1
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Cover_of_Darkness},
            None,
            num,
            "coversofdarkness",
        )

        num += 1
        _process_image(generate_type, minimap_type, {objects.ID.Ocean_Bottle}, None, num, "oceanbottles")


def _process_image(
    generate_type: str, minimap_type: str, filter: set, subfilter: set | None, png_number: int, png_name: str
) -> None:
    if generate_type == "Export":
        if minimap_type == "Standard":
            xprint(type=TextType.ACTION, text="Generating minimap…")
        elif minimap_type == "Extended":
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
        for map_layer in [Layer.Ground, Layer.Underground]
    }
    blocked_tiles = {map_layer: set() for map_layer in [Layer.Ground, Layer.Underground]}
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
            obj["id"] in IGNORED_OBJECTS_EXTENDED_MM_BASE2
            or (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == 1001)
        ):
            continue
        elif png_name == "border" and (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == 1001):
            continue
        # Get object masks
        def_ = map_data["object_defs"][obj["def_id"]]
        blockMask = def_["red_squares"]
        interactiveMask = def_["yellow_squares"]
        # Determine if object has owner and/or should be skipped (hidden on minimap).
        # If object is valid (should be shown on minimap), process it to determine blocked tiles and set tile ownership.
        owner = _determine_owner(minimap_type, obj)
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
    if generate_type == "View":
        _view_minimap_images(minimap_type, map_layers, blocked_tiles, ownership, png_number, png_name)
    if generate_type == "Export":
        _export_minimap_images(minimap_type, map_layers, blocked_tiles, ownership, png_number, png_name)
        xprint(type=TextType.DONE)


def _determine_owner(export_type: str, obj: dict) -> int | tuple | None:
    if (
        export_type == "Standard" and "owner" in obj and obj["id"] not in IGNORED_OBJECTS_STANDARD_MM
    ):  # Check if object has "owner" key and should not be ignored
        return obj["owner"]
    elif export_type == "Extended":
        if (
            (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] != 1001)
            or obj["id"] == objects.ID.Border_Guard
            or obj["id"] == objects.ID.Keymasters_Tent
        ):
            return obj["sub_id"] + 1000
        elif obj["id"] == objects.ID.Garrison or obj["id"] == objects.ID.Garrison_Vertical:
            return (1999, obj["owner"])
        elif obj["id"] == objects.ID.Quest_Guard:
            return 2000
        elif (
            obj["id"] == objects.ID.One_Way_MonolithPortal_Entrance
            or obj["id"] == objects.ID.One_Way_MonolithPortal_Exit
        ):
            return obj["sub_id"] + 3000
        elif obj["id"] == objects.ID.Two_Way_MonolithPortal:
            return obj["sub_id"] + 3500
        elif obj["id"] not in groups.DECOR:
            return 10000
    else:
        return None


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
    ownership: dict,
    owner: int | tuple | None,
    png_layer="",
) -> None:
    obj_x, obj_y, obj_z = obj["coords"]  # Get the object's coordinates
    for r in range(MaskSize.ROWS):  # 6 rows y-axis, from top to bottom
        for c in range(MaskSize.COLUMNS):  # 8 columns x-axis, from left to right
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
                        if ownership[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if png_layer == "base2" and interactiveMask[index] == 1:
                                ownership[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = None
                            elif png_layer == "border" and isinstance(owner, tuple):
                                if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    ownership[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    ownership[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        0
                                    ]  # Set to garrison color
                            else:
                                ownership[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    owner if owner is not None else None
                                )
                    elif obj_z == Layer.Underground:
                        blocked_tiles[Layer.Underground].add(
                            (blocked_tile_x, blocked_tile_y)
                        )  # Add the coordinates of the blocked tile to the underground set
                        if ownership[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] is None:
                            if png_layer == "base2" and interactiveMask[index] == 1:
                                ownership[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = None
                            elif png_layer == "border" and isinstance(owner, tuple):
                                if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                    ownership[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        1
                                    ]  # Set to owner color
                                else:  # Outer tiles
                                    ownership[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                        0
                                    ]  # Set to garrison color
                            else:
                                ownership[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = (
                                    owner if owner is not None else None
                                )


def _view_minimap_images(
    minimap_type: str,
    map_layers: list,
    blocked_tiles: dict,
    ownership: dict,
    png_number: int,
    png_name: str,
) -> None:
    xprint(text="Loading minimap…")

    IMAGE_SIZE = 756
    GAP_SIZE = 45

    map_size = map_data["general"]["map_size"]
    transparent = (0, 0, 0, 0)

    minimap_images = []
    for layer_index, layer in enumerate(map_layers):
        img = Image.new("RGBA", (map_size, map_size))
        for i, tile in enumerate(layer):
            x = i % map_size
            y = i // map_size
            owner = ownership[layer_index][y][x]
            color = _get_pixel_color(
                minimap_type,
                png_name,
                tile,
                owner,
                blocked_tiles,
                layer_index,
                x,
                y,
                transparent,
            )
            img.putpixel((x, y), color)

        minimap_images.append(img)

    base_layers = {"base1g": None, "base1u": None, "base2g": None, "base2u": None}

    for layer in range(len(minimap_images)):
        minimap_images[layer] = minimap_images[layer].resize(
            (IMAGE_SIZE, IMAGE_SIZE), resample=Image.Resampling.NEAREST
        )

        if png_name == "base1":
            if layer == 0:
                base_layers["base1g"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base1g"].paste(minimap_images[layer], (0, 0))
                base_layers["base1g"] = ImageEnhance.Brightness(base_layers["base1g"]).enhance(0.75)
            elif layer == 1:
                base_layers["base1u"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base1u"].paste(minimap_images[layer], (0, 0))
                base_layers["base1u"] = ImageEnhance.Brightness(base_layers["base1u"]).enhance(0.75)
        if png_name == "base2":
            if layer == 0:
                base_layers["base2g"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base2g"].paste(minimap_images[layer], (0, 0))
                base_layers["base2g"] = ImageEnhance.Brightness(base_layers["base2g"]).enhance(0.75)
            elif layer == 1:
                base_layers["base2u"] = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
                base_layers["base2u"].paste(minimap_images[layer], (0, 0))
                base_layers["base2u"] = ImageEnhance.Brightness(base_layers["base2u"]).enhance(0.75)

        canvas = Image.new("RGBA", minimap_images[layer].size)
        if minimap_type == "Extended" and png_name not in {"base1", "base2"}:
            if layer == 0:
                canvas.paste(base_layers["base1g"], (0, 0), base_layers["base1g"])
                canvas.paste(base_layers["base2g"], (0, 0), base_layers["base2g"])
            elif layer == 1:
                canvas.paste(base_layers["base1u"], (0, 0), base_layers["base1u"])
                canvas.paste(base_layers["base2u"], (0, 0), base_layers["base2u"])
        canvas.paste(minimap_images[layer], (0, 0), minimap_images[layer])
        minimap_images[layer] = canvas.convert("RGB")

    bg = Image.open(Path(os.getcwd()).parent / "h3mex" / "res" / "graphics" / "minimap_bg.png")
    minimap = bg.copy()
    minimap.paste(minimap_images[0], (GAP_SIZE, GAP_SIZE))
    if len(minimap_images) > 1:
        minimap.paste(minimap_images[1], (IMAGE_SIZE + (GAP_SIZE * 2), GAP_SIZE))

    buffer = BytesIO()
    minimap.save(buffer, format="PNG")

    xprint()
    if minimap_type == "Standard":
        xprint(text="STANDARD MINIMAP", align=TextAlign.CENTER, overwrite=2)
    else:
        xprint(text=f"EXTENDED MINIMAP - {png_number:02d}_{png_name}", align=TextAlign.CENTER, overwrite=2)
    xprint()

    display_image(buffer)
    xprint()


def _export_minimap_images(
    minimap_type: str,
    map_layers: list,
    blocked_tiles: dict,
    ownership: dict,
    png_number: int,
    png_name: str,
) -> None:

    export_path = os.path.join("exports/minimap", map_data["filename"][:-4])
    if not os.path.isdir(export_path):
        os.mkdir(export_path)
    if minimap_type == "Extended" and not os.path.isdir(export_path + "/extended"):
        os.mkdir(export_path + "/extended")

    map_size = map_data["general"]["map_size"]
    mode = "RGB" if png_name == "base1" else "RGBA"
    transparent = (0, 0, 0, 0)

    # Determine if we're creating a combined image
    is_combined = minimap_type == "Extended" and len(map_layers) > 1

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
                minimap_type,
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

        # Save layer image(s)
        if minimap_type == "Standard":
            layer_letter = "g" if map_layer_index == 0 else "u"
            img.save(os.path.join(f"{export_path}", f"{map_data["filename"][:-4]}_{layer_letter}.png"))
        elif minimap_type == "Extended":
            img.save(
                os.path.join(
                    f"{export_path}/extended",
                    f"{png_number:02d}_{png_name}.png",
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
            return OBJECT_COLORS[owner]
        elif (x, y) in blocked_tiles[map_layer_index]:
            return TERRAIN_COLORS[MinimapTerrainID(tile["terrain_type"]) + BLOCKED_TERRAIN_ID_OFFSET]
        else:
            return TERRAIN_COLORS[tile["terrain_type"]]
    elif export_type == "Extended":
        if png_name == "base1":
            if (x, y) in blocked_tiles[map_layer_index]:
                return TERRAIN_COLORS_ALT[MinimapTerrainID(tile["terrain_type"]) + BLOCKED_TERRAIN_ID_OFFSET]
            else:
                return TERRAIN_COLORS_ALT[tile["terrain_type"]]
        elif png_name == "base2":
            if owner == MinimapObjectID.ALL_OTHERS:
                color = TERRAIN_COLORS_ALT[MinimapTerrainID(tile["terrain_type"]) + BLOCKED_TERRAIN_ID_OFFSET]
                if color == TERRAIN_COLORS_ALT[MinimapTerrainID.BROCK]:
                    return transparent
                return color
            else:
                return transparent
        else:
            if owner is not None:
                return OBJECT_COLORS[owner] + (255,)
            else:
                return transparent
