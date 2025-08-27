import os
from enum import IntEnum

from core.h3m import objects
from PIL import Image
from src.common import DONE, MsgType, map_data, xprint

OVERWORLD = 0
UNDERGROUND = 1
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


class OWNER(IntEnum):
    RED = 0
    BLUE = 1
    TAN = 2
    GREEN = 3
    ORANGE = 4
    PURPLE = 5
    TEAL = 6
    PINK = 7
    NEUTRAL = 255


class KEYMASTER(IntEnum):
    LIGHTBLUE = 0
    GREEN = 1
    RED = 2
    DARKBLUE = 3
    BROWN = 4
    PURPLE = 5
    WHITE = 6
    BLACK = 7
    GARRISON = 255
    QUEST = 1000


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


# owner_colors = {
#     OWNER.RED:     (0xff, 0x00, 0x00),
#     OWNER.BLUE:    (0x31, 0x52, 0xff),
#     OWNER.TAN:     (0x9c, 0x73, 0x52),
#     OWNER.GREEN:   (0x42, 0x94, 0x29),
#     OWNER.ORANGE:  (0xff, 0x84, 0x00),
#     OWNER.PURPLE:  (0x8c, 0x29, 0xa5),
#     OWNER.TEAL:    (0x08, 0x9c, 0xa5),
#     OWNER.PINK:    (0xc6, 0x7b, 0x8c),
#     OWNER.NEUTRAL: (0x84, 0x84, 0x84)
# }


# keymaster_colors = {
#     KEYMASTER.LIGHTBLUE: (0x00, 0xb7, 0xff),
#     KEYMASTER.GREEN:     (0x06, 0xc6, 0x2f),
#     KEYMASTER.RED:       (0xCE, 0x19, 0x1A),
#     KEYMASTER.DARKBLUE:  (0x14, 0x14, 0xfe),
#     KEYMASTER.BROWN:     (0xc8, 0x82, 0x46),
#     KEYMASTER.PURPLE:    (0xa8, 0x43, 0xe0),
#     KEYMASTER.WHITE:     (0xf7, 0xf7, 0xf7),
#     KEYMASTER.BLACK:     (0x12, 0x12, 0x12),
#     KEYMASTER.GARRISON:  (0x9c, 0x9a, 0x8b),
#     KEYMASTER.QUEST:     (0xff, 0xff, 0x00)
# }


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
    objects.ID.HotA_Collectible,
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
    objects.Two_Way_Monolith.Small_Green,
    objects.Two_Way_Monolith.Small_Brown,
    objects.Two_Way_Monolith.Small_Violet,
    objects.Two_Way_Monolith.Small_Orange,
    objects.Two_Way_Monolith.Big_Green,
    objects.Two_Way_Monolith.Big_Yellow,
    objects.Two_Way_Monolith.Big_Red,
    objects.Two_Way_Monolith.Big_Cyan,
    objects.Two_Way_Monolith.Small_Pink,
    objects.Two_Way_Monolith.Small_Turquoise,
    objects.Two_Way_Monolith.Small_Yellow,
    objects.Two_Way_Monolith.Small_Black,
    objects.Two_Way_Monolith.Big_Chartreuse,
    objects.Two_Way_Monolith.Big_Turquoise,
    objects.Two_Way_Monolith.Big_Violet,
    objects.Two_Way_Monolith.Big_Orange,
    objects.Two_Way_Monolith.Small_Blue,
    objects.Two_Way_Monolith.Small_Red,
    objects.Two_Way_Monolith.Big_Pink,
    objects.Two_Way_Monolith.Big_Blue,
}


two_way_water_portals = {
    objects.Two_Way_Monolith.Water_White,
    objects.Two_Way_Monolith.Water_Red,
    objects.Two_Way_Monolith.Water_Blue,
    objects.Two_Way_Monolith.Water_Chartreuse,
    objects.Two_Way_Monolith.Water_Yellow,
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


def export(keypress: int) -> bool:
    def main():
        if keypress == 1:
            process_image(keypress, None, None, None, None)
        elif keypress == 2:
            process_image(keypress, objects.Decor.IDS, None, 1, "base1")
            process_image(keypress, None, None, 2, "base2")
            process_image(keypress, border_objects, None, 3, "border")
            process_image(keypress, {objects.ID.Keymasters_Tent}, None, 4, "tents")
            process_image(
                keypress,
                {objects.ID.Monolith_One_Way_Entrance},
                None,
                5,
                "portals1en",
            )
            process_image(keypress, {objects.ID.Monolith_One_Way_Exit}, None, 6, "portals1ex")
            process_image(
                keypress,
                {objects.ID.Two_Way_Monolith},
                two_way_land_portals,
                7,
                "portals2land",
            )
            process_image(
                keypress,
                {objects.ID.Two_Way_Monolith},
                two_way_water_portals,
                8,
                "portals2water",
            )
            process_image(keypress, {objects.ID.Whirlpool}, None, 9, "whirlpools")
            process_image(keypress, {objects.ID.Prison}, None, 10, "prisons")
            process_image(keypress, monster_objects, None, 11, "monsters")
            process_image(keypress, {objects.ID.Spell_Scroll}, None, 12, "spellscrolls")
            process_image(
                keypress,
                {objects.ID.Shrine_1_and_4},
                {objects.Shrine_1_and_4.Shrine_of_Magic_Incantation},
                13,
                "spellshrine1",
            )
            process_image(
                keypress,
                {objects.ID.Shrine_of_Magic_Gesture},
                None,
                14,
                "spellshrine2",
            )
            process_image(
                keypress,
                {objects.ID.Shrine_of_Magic_Thought},
                None,
                15,
                "spellshrine3",
            )
            process_image(
                keypress,
                {objects.ID.Shrine_1_and_4},
                {objects.Shrine_1_and_4.Shrine_of_Magic_Mystery},
                16,
                "spellshrine4",
            )
            process_image(keypress, {objects.ID.Pyramid}, None, 17, "pyramids")
            process_image(keypress, {objects.ID.Artifact}, None, 18, "artifacts")
            process_image(keypress, {objects.ID.Random_Artifact}, None, 19, "randomartifacts")
            process_image(
                keypress,
                {objects.ID.Random_Treasure_Artifact},
                None,
                20,
                "randomtreasureartifacts",
            )
            process_image(
                keypress,
                {objects.ID.Random_Minor_Artifact},
                None,
                21,
                "randomminorartifacts",
            )
            process_image(
                keypress,
                {objects.ID.Random_Major_Artifact},
                None,
                22,
                "randommajorartifacts",
            )
            process_image(keypress, {objects.ID.Random_Relic}, None, 23, "randomrelics")
            process_image(keypress, resource_objects, None, 24, "resources")
            process_image(keypress, {objects.ID.Treasure_Chest}, None, 25, "treasurechests")
        return True

    def process_image(keypress, filter, subfilter, png_number, png_name) -> bool:
        if keypress == 1:
            xprint(type=MsgType.ACTION, text="Generating minimap…")
        elif keypress == 2:
            xprint(
                type=MsgType.ACTION,
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
            for map_layer in [OVERWORLD, UNDERGROUND]
        }
        blocked_tiles = {map_layer: set() for map_layer in [OVERWORLD, UNDERGROUND]}
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
            owner = determine_owner(keypress, obj)
            if owner is None and should_skip_object(blockMask, interactiveMask):
                continue
            process_object(
                obj,
                blockMask,
                interactiveMask,
                blocked_tiles,
                ownership,
                owner,
                png_name,
            )
        # Generate and save minimap images
        generate_images(keypress, map_layers, blocked_tiles, ownership, png_number, png_name)
        xprint(type=MsgType.SPECIAL, text=DONE)
        return True

    def determine_owner(keypress: int, obj: dict) -> int | tuple | None:
        if (
            keypress == 1 and "owner" in obj and obj["id"] not in ignored_owned_objects
        ):  # Check if object has "owner" key and should not be ignored
            return obj["owner"]
        elif keypress == 2:
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
            elif obj["id"] == objects.ID.Monolith_One_Way_Entrance or obj["id"] == objects.ID.Monolith_One_Way_Exit:
                return obj["sub_id"] + 3000
            elif obj["id"] == objects.ID.Two_Way_Monolith:
                return obj["sub_id"] + 3500
            elif obj["id"] not in objects.Decor.IDS:
                return 10000
        else:
            return None

    def should_skip_object(blockMask: list, interactiveMask: list) -> bool:
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
            if not yellowSquaresOnly and isInteractive and not allPassable:
                break
        return isInteractive and yellowSquaresOnly

    def process_object(
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
                        if obj_z == OVERWORLD:
                            blocked_tiles[OVERWORLD].add(
                                (blocked_tile_x, blocked_tile_y)
                            )  # Add the coordinates of the blocked tile to the overworld set
                            if ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] is None:
                                if png_layer == "base2" and interactiveMask[index] == 1:
                                    ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = OBJECTS.INTERACTIVE
                                elif png_layer == "border" and isinstance(owner, tuple):
                                    if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                        ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                            1
                                        ]  # Set to owner color
                                    else:  # Outer tiles
                                        ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                            0
                                        ]  # Set to garrison color
                                else:
                                    ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = (
                                        owner if owner is not None else None
                                    )
                        elif obj_z == UNDERGROUND:
                            blocked_tiles[UNDERGROUND].add(
                                (blocked_tile_x, blocked_tile_y)
                            )  # Add the coordinates of the blocked tile to the underground set
                            if ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] is None:
                                if png_layer == "base2" and interactiveMask[index] == 1:
                                    ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = OBJECTS.INTERACTIVE
                                elif png_layer == "border" and isinstance(owner, tuple):
                                    if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                        ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                            1
                                        ]  # Set to owner color
                                    else:  # Outer tiles
                                        ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = owner[
                                            0
                                        ]  # Set to garrison color
                                else:
                                    ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = (
                                        owner if owner is not None else None
                                    )

    def generate_images(
        keypress: int,
        map_layers: list,
        blocked_tiles: dict,
        ownership: dict,
        png_number: int,
        png_name: str,
    ) -> None:
        IMAGES_PATH = ".../maps/exports/minimap"

        map_size = map_data["general"]["map_size"]
        mode = "RGB" if png_name == "base1" else "RGBA"
        transparent = (0, 0, 0, 0)
        map_name = map_data["filename"][:-4] if map_data["filename"].endswith(".h3m") else map_data["filename"]

        # Determine if we're creating a combined image
        is_combined = keypress == 2 and len(map_layers) > 1

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
                color = get_pixel_color(
                    keypress,
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
                if keypress == 1:
                    img.save(os.path.join(IMAGES_PATH, f"{map_name}_{layer_letter}.png"))
                elif keypress == 2:
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

    def get_pixel_color(
        keypress: int,
        png_name: str,
        tile: tuple,
        owner: int,
        blocked_tiles: dict,
        map_layer_index: int,
        x: int,
        y: int,
        transparent: tuple,
    ) -> tuple:
        if keypress == 1:
            if owner is not None:
                return object_colors[owner]
            elif (x, y) in blocked_tiles[map_layer_index]:
                return terrain_colors[TERRAIN(tile["terrain_type_int"]) + BLOCKED_OFFSET]
            else:
                return terrain_colors[tile["terrain_type_int"]]
        elif keypress == 2:
            if png_name == "base1":
                if (x, y) in blocked_tiles[map_layer_index]:
                    return terrain_colors_alt[TERRAIN(tile["terrain_type_int"]) + BLOCKED_OFFSET]
                else:
                    return terrain_colors_alt[tile["terrain_type_int"]]
            elif png_name == "base2":
                if owner == OBJECTS.ALL_OTHERS:
                    color = terrain_colors_alt[TERRAIN(tile["terrain_type_int"]) + BLOCKED_OFFSET]
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

    return main()
