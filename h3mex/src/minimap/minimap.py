import os
from enum import IntEnum
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageEnhance
from src.common import Keypress, Layer, TextAlign, TextType, map_data
from src.defs import groups, objects
from src.ui.menus import Menu
from src.ui.xprint import xprint
from src.utilities import display_image, wait_for_keypress

ROWS = 6
COLUMNS = 8
BLOCKED_OFFSET = 20


class TERRAIN(IntEnum):
    # normal
    DIRT = 0
    SAND = 1
    GRASS = 2
    SNOW = 3
    SWAMP = 4
    ROUGH = 5
    SUBTERRANEAN = 6
    LAVA = 7
    WATER = 8
    ROCK = 9
    HIGHLANDS = 10
    WASTELAND = 11

    # blocked
    BDIRT = 20
    BSAND = 21
    BGRASS = 22
    BSNOW = 23
    BSWAMP = 24
    BROUGH = 25
    BSUBTERRANEAN = 26
    BLAVA = 27
    BWATER = 28
    BROCK = 29
    BHIGHLANDS = 30
    BWASTELAND = 31


class OBJECTS(IntEnum):
    RED = 0
    BLUE = 1
    TAN = 2
    GREEN = 3
    ORANGE = 4
    PURPLE = 5
    TEAL = 6
    PINK = 7
    NEUTRAL = 255

    KM_LIGHTBLUE = 1000
    KM_GREEN = 1001
    KM_RED = 1002
    KM_DARKBLUE = 1003
    KM_BROWN = 1004
    KM_PURPLE = 1005
    KM_WHITE = 1006
    KM_BLACK = 1007
    GARRISON = 1999
    QUEST = 2000

    M1_BLUE = 3000
    M1_PINK = 3001
    M1_ORANGE = 3002
    M1_YELLOW = 3003
    P1_PURPLE = 3004
    P1_ORANGE = 3005
    P1_RED = 3006
    P1_CYAN = 3007
    M1_TURQUOISE = 3008
    M1_VIOLET = 3009
    M1_CHARTREUSE = 3010
    M1_WHITE = 3011
    M2_GREEN = 3500
    M2_BROWN = 3501
    M2_VIOLET = 3502
    M2_ORANGE = 3503
    P2_GREEN = 3504
    P2_YELLOW = 3505
    P2_RED = 3506
    P2_CYAN = 3507
    S2_WHITE = 3508
    M2_PINK = 3509
    M2_TURQUOISE = 3510
    M2_YELLOW = 3511
    M2_BLACK = 3512
    P2_CHARTREUSE = 3513
    P2_TURQUOISE = 3514
    P2_VIOLET = 3515
    P2_ORANGE = 3516
    M2_BLUE = 3517
    M2_RED = 3518
    P2_PINK = 3519
    P2_BLUE = 3520
    S2_RED = 3521
    S2_BLUE = 3522
    S2_CHARTREUSE = 3523
    S2_YELLOW = 3524

    INTERACTIVE = 9999
    ALL_OTHERS = 10000


terrain_colors = {
    # Terrain
    TERRAIN.DIRT: (0x52, 0x39, 0x08),
    TERRAIN.SAND: (0xDE, 0xCE, 0x8C),
    TERRAIN.GRASS: (0x00, 0x42, 0x00),
    TERRAIN.SNOW: (0xB5, 0xC6, 0xC6),
    TERRAIN.SWAMP: (0x4A, 0x84, 0x6B),
    TERRAIN.ROUGH: (0x84, 0x73, 0x31),
    TERRAIN.SUBTERRANEAN: (0x84, 0x31, 0x00),
    TERRAIN.LAVA: (0x4A, 0x4A, 0x4A),
    TERRAIN.WATER: (0x08, 0x52, 0x94),
    TERRAIN.ROCK: (0x00, 0x00, 0x00),
    TERRAIN.HIGHLANDS: (0x29, 0x73, 0x18),
    TERRAIN.WASTELAND: (0xBD, 0x5A, 0x08),
    # Blocked Terrain
    TERRAIN.BDIRT: (0x39, 0x29, 0x08),
    TERRAIN.BSAND: (0xA5, 0x9C, 0x6B),
    TERRAIN.BGRASS: (0x00, 0x31, 0x00),
    TERRAIN.BSNOW: (0x8C, 0x9C, 0x9C),
    TERRAIN.BSWAMP: (0x21, 0x5A, 0x42),
    TERRAIN.BROUGH: (0x63, 0x52, 0x21),
    TERRAIN.BSUBTERRANEAN: (0x5A, 0x08, 0x00),
    TERRAIN.BLAVA: (0x29, 0x29, 0x29),
    TERRAIN.BWATER: (0x00, 0x29, 0x6B),
    TERRAIN.BROCK: (0x00, 0x00, 0x00),
    TERRAIN.BHIGHLANDS: (0x21, 0x52, 0x10),
    TERRAIN.BWASTELAND: (0x9C, 0x42, 0x08),
}


terrain_colors_alt = {
    # Terrain
    TERRAIN.DIRT: (0x4D, 0x4D, 0x4D),
    TERRAIN.SAND: (0x4D, 0x4D, 0x4D),
    TERRAIN.GRASS: (0x4D, 0x4D, 0x4D),
    TERRAIN.SNOW: (0x4D, 0x4D, 0x4D),
    TERRAIN.SWAMP: (0x4D, 0x4D, 0x4D),
    TERRAIN.ROUGH: (0x4D, 0x4D, 0x4D),
    TERRAIN.SUBTERRANEAN: (0x4D, 0x4D, 0x4D),
    TERRAIN.LAVA: (0x4D, 0x4D, 0x4D),
    TERRAIN.WATER: (0x4B, 0x56, 0x5E),
    TERRAIN.ROCK: (0x00, 0x00, 0x00),
    TERRAIN.HIGHLANDS: (0x4D, 0x4D, 0x4D),
    TERRAIN.WASTELAND: (0x4D, 0x4D, 0x4D),
    # Blocked Terrain
    TERRAIN.BDIRT: (0x3D, 0x3D, 0x3D),
    TERRAIN.BSAND: (0x3D, 0x3D, 0x3D),
    TERRAIN.BGRASS: (0x3D, 0x3D, 0x3D),
    TERRAIN.BSNOW: (0x3D, 0x3D, 0x3D),
    TERRAIN.BSWAMP: (0x3D, 0x3D, 0x3D),
    TERRAIN.BROUGH: (0x3D, 0x3D, 0x3D),
    TERRAIN.BSUBTERRANEAN: (0x3D, 0x3D, 0x3D),
    TERRAIN.BLAVA: (0x3D, 0x3D, 0x3D),
    TERRAIN.BWATER: (0x3C, 0x45, 0x4D),
    TERRAIN.BROCK: (0x00, 0x00, 0x00),
    TERRAIN.BHIGHLANDS: (0x3D, 0x3D, 0x3D),
    TERRAIN.BWASTELAND: (0x3D, 0x3D, 0x3D),
}


object_colors = {
    OBJECTS.RED: (0xFF, 0x00, 0x00),
    OBJECTS.BLUE: (0x31, 0x52, 0xFF),
    OBJECTS.TAN: (0x9C, 0x73, 0x52),
    OBJECTS.GREEN: (0x42, 0x94, 0x29),
    OBJECTS.ORANGE: (0xFF, 0x84, 0x00),
    OBJECTS.PURPLE: (0x8C, 0x29, 0xA5),
    OBJECTS.TEAL: (0x08, 0x9C, 0xA5),
    OBJECTS.PINK: (0xC6, 0x7B, 0x8C),
    OBJECTS.NEUTRAL: (0x84, 0x84, 0x84),
    OBJECTS.KM_LIGHTBLUE: (0x00, 0xB7, 0xFF),
    OBJECTS.KM_GREEN: (0x06, 0xC6, 0x2F),
    OBJECTS.KM_RED: (0xCE, 0x19, 0x1A),
    OBJECTS.KM_DARKBLUE: (0x14, 0x14, 0xFE),
    OBJECTS.KM_BROWN: (0xC8, 0x82, 0x46),
    OBJECTS.KM_PURPLE: (0xA8, 0x43, 0xE0),
    OBJECTS.KM_WHITE: (0xF7, 0xF7, 0xF7),
    OBJECTS.KM_BLACK: (0x12, 0x12, 0x12),
    OBJECTS.GARRISON: (0x9C, 0x9A, 0x8B),
    OBJECTS.QUEST: (0xFF, 0xFF, 0x00),
    OBJECTS.M1_BLUE: (0x1E, 0x40, 0xCF),
    OBJECTS.M1_PINK: (0xF7, 0x38, 0xA6),
    OBJECTS.M1_ORANGE: (0xFF, 0x8C, 0x1A),
    OBJECTS.M1_YELLOW: (0xFF, 0xF7, 0x1A),
    OBJECTS.P1_PURPLE: (0x8E, 0x44, 0xAD),
    OBJECTS.P1_ORANGE: (0xFF, 0xB3, 0x47),
    OBJECTS.P1_RED: (0xE7, 0x2B, 0x2B),
    OBJECTS.P1_CYAN: (0x1A, 0xE6, 0xE6),
    OBJECTS.M1_TURQUOISE: (0x1A, 0xC6, 0xB7),
    OBJECTS.M1_VIOLET: (0x7C, 0x3C, 0xBD),
    OBJECTS.M1_CHARTREUSE: (0x7D, 0xFF, 0x1A),
    OBJECTS.M1_WHITE: (0xF7, 0xF7, 0xF7),
    OBJECTS.M2_GREEN: (0x1A, 0xB5, 0x3B),
    OBJECTS.M2_BROWN: (0x8B, 0x5C, 0x2B),
    OBJECTS.M2_VIOLET: (0xB0, 0x5D, 0xE6),
    OBJECTS.M2_ORANGE: (0xFF, 0x6F, 0x00),
    OBJECTS.P2_GREEN: (0x3B, 0xE6, 0x1A),
    OBJECTS.P2_YELLOW: (0xFF, 0xE6, 0x1A),
    OBJECTS.P2_RED: (0xD9, 0x2B, 0x2B),
    OBJECTS.P2_CYAN: (0x1A, 0xB5, 0xE6),
    OBJECTS.S2_WHITE: (0xFF, 0xFF, 0xFF),
    OBJECTS.M2_PINK: (0xFF, 0x69, 0xB4),
    OBJECTS.M2_TURQUOISE: (0x40, 0xE0, 0xD0),
    OBJECTS.M2_YELLOW: (0xFF, 0xFF, 0x99),
    OBJECTS.M2_BLACK: (0x22, 0x22, 0x22),
    OBJECTS.P2_CHARTREUSE: (0x7F, 0xFF, 0x00),
    OBJECTS.P2_TURQUOISE: (0x00, 0xFF, 0xFF),
    OBJECTS.P2_VIOLET: (0xEE, 0x82, 0xEE),
    OBJECTS.P2_ORANGE: (0xFF, 0xA5, 0x00),
    OBJECTS.M2_BLUE: (0x00, 0x7F, 0xFF),
    OBJECTS.M2_RED: (0xFF, 0x45, 0x00),
    OBJECTS.P2_PINK: (0xFF, 0xC0, 0xCB),
    OBJECTS.P2_BLUE: (0x00, 0x00, 0xFF),
    OBJECTS.S2_RED: (0xB2, 0x22, 0x22),
    OBJECTS.S2_BLUE: (0x41, 0x69, 0xE1),
    OBJECTS.S2_CHARTREUSE: (0xAD, 0xFF, 0x2F),
    OBJECTS.S2_YELLOW: (0xFF, 0xFA, 0xCD),
    OBJECTS.INTERACTIVE: (0xFF, 0x00, 0x00),
    OBJECTS.ALL_OTHERS: (0xFF, 0xFF, 0xFF),
}


ignored_owned_objects = {
    objects.ID.Hero,
    objects.ID.Prison,
    objects.ID.Random_Hero,
    objects.ID.Hero_Placeholder,
}


ignored_pickups = {
    objects.ID.Treasure_Chest,
    objects.ID.Scholar,
    objects.ID.Campfire,
    objects.ID.Flotsam,
    objects.ID.Sea_Chest,
    objects.ID.Shipwreck_Survivor,
    objects.ID.Ocean_Bottle,
    objects.ID.Grail,
    objects.ID.Monster,
    objects.ID.Event,
    objects.ID.Artifact,
    objects.ID.Pandoras_Box,
    objects.ID.Spell_Scroll,
    objects.ID.HotA_Pickup,
    objects.ID.Random_Artifact,
    objects.ID.Random_Treasure_Artifact,
    objects.ID.Random_Minor_Artifact,
    objects.ID.Random_Major_Artifact,
    objects.ID.Random_Relic,
    objects.ID.Random_Monster,
    objects.ID.Random_Monster_1,
    objects.ID.Random_Monster_2,
    objects.ID.Random_Monster_3,
    objects.ID.Random_Monster_4,
    objects.ID.Random_Monster_5,
    objects.ID.Random_Monster_6,
    objects.ID.Random_Monster_7,
    objects.ID.Random_Resource,
    objects.ID.Resource,
    objects.ID.Boat,
}


border_objects = {
    objects.ID.Border_Gate,
    objects.ID.Border_Guard,
    objects.ID.Garrison,
    objects.ID.Garrison_Vertical,
    objects.ID.Quest_Guard,
}


two_way_land_portals = {
    objects.SubID.Portal.TwoWay.Small_Green,
    objects.SubID.Portal.TwoWay.Small_Brown,
    objects.SubID.Portal.TwoWay.Small_Violet,
    objects.SubID.Portal.TwoWay.Small_Orange,
    objects.SubID.Portal.TwoWay.Big_Green,
    objects.SubID.Portal.TwoWay.Big_Yellow,
    objects.SubID.Portal.TwoWay.Big_Red,
    objects.SubID.Portal.TwoWay.Big_Cyan,
    objects.SubID.Portal.TwoWay.Small_Pink,
    objects.SubID.Portal.TwoWay.Small_Turquoise,
    objects.SubID.Portal.TwoWay.Small_Yellow,
    objects.SubID.Portal.TwoWay.Small_Black,
    objects.SubID.Portal.TwoWay.Big_Chartreuse,
    objects.SubID.Portal.TwoWay.Big_Turquoise,
    objects.SubID.Portal.TwoWay.Big_Violet,
    objects.SubID.Portal.TwoWay.Big_Orange,
    objects.SubID.Portal.TwoWay.Small_Blue,
    objects.SubID.Portal.TwoWay.Small_Red,
    objects.SubID.Portal.TwoWay.Big_Pink,
    objects.SubID.Portal.TwoWay.Big_Blue,
}


two_way_water_portals = {
    objects.SubID.Portal.TwoWay.Water_White,
    objects.SubID.Portal.TwoWay.Water_Red,
    objects.SubID.Portal.TwoWay.Water_Blue,
    objects.SubID.Portal.TwoWay.Water_Chartreuse,
    objects.SubID.Portal.TwoWay.Water_Yellow,
}


monster_objects = {
    objects.ID.Monster,
    objects.ID.Random_Monster,
    objects.ID.Random_Monster_1,
    objects.ID.Random_Monster_2,
    objects.ID.Random_Monster_3,
    objects.ID.Random_Monster_4,
    objects.ID.Random_Monster_5,
    objects.ID.Random_Monster_6,
    objects.ID.Random_Monster_7,
}


resource_objects = {objects.ID.Resource, objects.ID.Random_Resource}

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
                generate("View", "Standard")
            case "2":
                generate("View", "Extended")

        wait_for_keypress()


def generate(generate_type: str, minimap_type: str) -> None:
    if minimap_type == "Standard":
        _process_image(generate_type, minimap_type, None, None, None, None)
    elif minimap_type == "Extended":
        _process_image(generate_type, minimap_type, groups.DECOR, None, 1, "base1")
        _process_image(generate_type, minimap_type, None, None, 2, "base2")
        _process_image(generate_type, minimap_type, border_objects, None, 3, "border")
        _process_image(generate_type, minimap_type, {objects.ID.Keymasters_Tent}, None, 4, "tents")
        _process_image(generate_type, minimap_type, {objects.ID.One_Way_Portal_Entrance}, None, 5, "portals1en")
        _process_image(generate_type, minimap_type, {objects.ID.One_Way_Portal_Exit}, None, 6, "portals1ex")
        _process_image(
            generate_type, minimap_type, {objects.ID.Two_Way_Portal}, two_way_land_portals, 7, "portals2land"
        )
        _process_image(
            generate_type, minimap_type, {objects.ID.Two_Way_Portal}, two_way_water_portals, 8, "portals2water"
        )
        _process_image(generate_type, minimap_type, {objects.ID.Whirlpool}, None, 9, "whirlpools")
        _process_image(generate_type, minimap_type, {objects.ID.Prison}, None, 10, "prisons")
        _process_image(generate_type, minimap_type, monster_objects, None, 11, "monsters")
        _process_image(generate_type, minimap_type, {objects.ID.Spell_Scroll}, None, 12, "spellscrolls")
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Shrine_1_and_4},
            {objects.SubID.Shrine_1_and_4.Shrine_of_Magic_Incantation},
            13,
            "shrine1",
        )
        _process_image(generate_type, minimap_type, {objects.ID.Shrine_of_Magic_Gesture}, None, 14, "shrine2")
        _process_image(generate_type, minimap_type, {objects.ID.Shrine_of_Magic_Thought}, None, 15, "shrine3")
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Shrine_1_and_4},
            {objects.SubID.Shrine_1_and_4.Shrine_of_Magic_Mystery},
            16,
            "shrine4",
        )
        _process_image(generate_type, minimap_type, {objects.ID.Pyramid}, None, 17, "pyramids")
        _process_image(generate_type, minimap_type, {objects.ID.Artifact}, None, 18, "artifacts")
        _process_image(generate_type, minimap_type, {objects.ID.Random_Artifact}, None, 19, "randomartifacts")
        _process_image(
            generate_type, minimap_type, {objects.ID.Random_Treasure_Artifact}, None, 20, "randomtreasureartifacts"
        )
        _process_image(
            generate_type, minimap_type, {objects.ID.Random_Minor_Artifact}, None, 21, "randomminorartifacts"
        )
        _process_image(
            generate_type, minimap_type, {objects.ID.Random_Major_Artifact}, None, 22, "randommajorartifacts"
        )
        _process_image(generate_type, minimap_type, {objects.ID.Random_Relic}, None, 23, "randomrelics")
        _process_image(generate_type, minimap_type, resource_objects, None, 24, "resources")
        _process_image(generate_type, minimap_type, {objects.ID.Treasure_Chest}, None, 25, "treasurechests")
        _process_image(generate_type, minimap_type, {objects.ID.Scholar}, None, 26, "scholars")
        _process_image(generate_type, minimap_type, {objects.ID.Event}, None, 27, "eventobjects")
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Trading_Post, objects.ID.Trading_Post_Snow},
            None,
            28,
            "tradingposts",
        )
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.HotA_Visitable_1},
            {objects.SubID.HotAVisitable1.Warlocks_Lab},
            29,
            "warlockslabs",
        )
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Redwood_Observatory},
            None,
            30,
            "redwoodobservatories",
        )
        _process_image(
            generate_type,
            minimap_type,
            {objects.ID.Cover_of_Darkness},
            None,
            31,
            "coversofdarkness",
        )


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
            obj["id"] in ignored_pickups or (obj["id"] == objects.ID.Border_Gate and obj["sub_id"] == 1001)
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
        export_type == "Standard" and "owner" in obj and obj["id"] not in ignored_owned_objects
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
        elif obj["id"] == objects.ID.One_Way_Portal_Entrance or obj["id"] == objects.ID.One_Way_Portal_Exit:
            return obj["sub_id"] + 3000
        elif obj["id"] == objects.ID.Two_Way_Portal:
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
    for r in range(ROWS):  # 6 rows y-axis, from top to bottom
        for c in range(COLUMNS):  # 8 columns x-axis, from left to right
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
                                ownership[Layer.Ground][obj_y - 5 + r][obj_x - 7 + c] = OBJECTS.INTERACTIVE
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
                                ownership[Layer.Underground][obj_y - 5 + r][obj_x - 7 + c] = OBJECTS.INTERACTIVE
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

    for layer in range(len(minimap_images)):
        minimap_images[layer] = minimap_images[layer].resize((370, 370), resample=Image.Resampling.NEAREST)

        if png_name == "base1":
            if layer == 0:
                base_layers["base1g"] = Image.new("RGBA", (370, 370))
                base_layers["base1g"].paste(minimap_images[layer], (0, 0))
                base_layers["base1g"] = ImageEnhance.Brightness(base_layers["base1g"]).enhance(0.75)
            elif layer == 1:
                base_layers["base1u"] = Image.new("RGBA", (370, 370))
                base_layers["base1u"].paste(minimap_images[layer], (0, 0))
                base_layers["base1u"] = ImageEnhance.Brightness(base_layers["base1u"]).enhance(0.75)
        if png_name == "base2":
            if layer == 0:
                base_layers["base2g"] = Image.new("RGBA", (370, 370))
                base_layers["base2g"].paste(minimap_images[layer], (0, 0))
                base_layers["base2g"] = ImageEnhance.Brightness(base_layers["base2g"]).enhance(0.75)
            elif layer == 1:
                base_layers["base2u"] = Image.new("RGBA", (370, 370))
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
    minimap.paste(minimap_images[0], (20, 20))
    if len(minimap_images) > 1:
        minimap.paste(minimap_images[1], (410, 20))

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
    IMAGES_PATH = "exports/minimap"

    map_size = map_data["general"]["map_size"]
    mode = "RGB" if png_name == "base1" else "RGBA"
    transparent = (0, 0, 0, 0)
    map_name = map_data["filename"][:-4] if map_data["filename"].endswith(".h3m") else map_data["filename"]

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

        if not is_combined:
            # Save individual layer image
            layer_letter = "g" if map_layer_index == 0 else "u"
            if minimap_type == "Standard":
                img.save(os.path.join(IMAGES_PATH, f"{map_name}_{layer_letter}.png"))
            elif minimap_type == "Extended":
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
            return terrain_colors[TERRAIN(tile["terrain_type"]) + BLOCKED_OFFSET]
        else:
            return terrain_colors[tile["terrain_type"]]
    elif export_type == "Extended":
        if png_name == "base1":
            if (x, y) in blocked_tiles[map_layer_index]:
                return terrain_colors_alt[TERRAIN(tile["terrain_type"]) + BLOCKED_OFFSET]
            else:
                return terrain_colors_alt[tile["terrain_type"]]
        elif png_name == "base2":
            if owner == OBJECTS.ALL_OTHERS:
                color = terrain_colors_alt[TERRAIN(tile["terrain_type"]) + BLOCKED_OFFSET]
                if color == terrain_colors_alt[TERRAIN.BROCK]:
                    return transparent
                return color
            else:
                return transparent
        else:
            if owner is not None:
                return object_colors[owner] + (255,)
            else:
                return transparent
