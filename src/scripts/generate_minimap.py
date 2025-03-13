
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'data'))

from enum import IntEnum
from PIL  import Image

from ..common import *
from ..menus import *
from data import objects

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

terrain_colors = {
    # Terrain
    TERRAIN.DIRT: (0x52, 0x39, 0x08),
    TERRAIN.SAND: (0xde, 0xce, 0x8c),
    TERRAIN.GRASS: (0x00, 0x42, 0x00),
    TERRAIN.SNOW: (0xb5, 0xc6, 0xc6),
    TERRAIN.SWAMP: (0x4a, 0x84, 0x6b),
    TERRAIN.ROUGH: (0x84, 0x73, 0x31),
    TERRAIN.SUBTERRANEAN: (0x84, 0x31, 0x00),
    TERRAIN.LAVA: (0x4a, 0x4a, 0x4a),
    TERRAIN.WATER: (0x08, 0x52, 0x94),
    TERRAIN.ROCK: (0x00, 0x00, 0x00),
    TERRAIN.HIGHLANDS: (0x29, 0x73, 0x18),
    TERRAIN.WASTELAND: (0xbd, 0x5a, 0x08),
    # Blocked Terrain
    TERRAIN.BDIRT: (0x39, 0x29, 0x08),
    TERRAIN.BSAND: (0xa5, 0x9c, 0x6b),
    TERRAIN.BGRASS: (0x00, 0x31, 0x00),
    TERRAIN.BSNOW: (0x8c, 0x9c, 0x9c),
    TERRAIN.BSWAMP: (0x21, 0x5a, 0x42),
    TERRAIN.BROUGH: (0x63, 0x52, 0x21),
    TERRAIN.BSUBTERRANEAN: (0x5a, 0x08, 0x00),
    TERRAIN.BLAVA: (0x29, 0x29, 0x29),
    TERRAIN.BWATER: (0x00, 0x29, 0x6b),
    TERRAIN.BROCK: (0x00, 0x00, 0x00),
    TERRAIN.BHIGHLANDS: (0x21, 0x52, 0x10),
    TERRAIN.BWASTELAND: (0x9c, 0x42, 0x08),
}

terrain_colors_alt = {
    # Terrain
    TERRAIN.DIRT:  (0x4d, 0x4d, 0x4d),
    TERRAIN.SAND:  (0x4d, 0x4d, 0x4d),
    TERRAIN.GRASS:  (0x4d, 0x4d, 0x4d),
    TERRAIN.SNOW:  (0x4d, 0x4d, 0x4d),
    TERRAIN.SWAMP:  (0x4d, 0x4d, 0x4d),
    TERRAIN.ROUGH:  (0x4d, 0x4d, 0x4d),
    TERRAIN.SUBTERRANEAN:  (0x4d, 0x4d, 0x4d),
    TERRAIN.LAVA:  (0x4d, 0x4d, 0x4d),
    TERRAIN.WATER: (0x4b, 0x56, 0x5e),
    TERRAIN.ROCK: (0x00, 0x00, 0x00),
    TERRAIN.HIGHLANDS:  (0x4d, 0x4d, 0x4d),
    TERRAIN.WASTELAND:  (0x4d, 0x4d, 0x4d),
    # Blocked Terrain
    TERRAIN.BDIRT: (0x3d, 0x3d, 0x3d),
    TERRAIN.BSAND: (0x3d, 0x3d, 0x3d),
    TERRAIN.BGRASS: (0x3d, 0x3d, 0x3d),
    TERRAIN.BSNOW: (0x3d, 0x3d, 0x3d),
    TERRAIN.BSWAMP: (0x3d, 0x3d, 0x3d),
    TERRAIN.BROUGH: (0x3d, 0x3d, 0x3d),
    TERRAIN.BSUBTERRANEAN: (0x3d, 0x3d, 0x3d),
    TERRAIN.BLAVA: (0x3d, 0x3d, 0x3d),
    TERRAIN.BWATER: (0x3c, 0x45, 0x4d),
    TERRAIN.BROCK: (0x00, 0x00, 0x00),
    TERRAIN.BHIGHLANDS: (0x3d, 0x3d, 0x3d),
    TERRAIN.BWASTELAND: (0x3d, 0x3d, 0x3d),
}

owner_colors = {
    OWNER.RED: (0xff, 0x00, 0x00),
    OWNER.BLUE: (0x31, 0x52, 0xff),
    OWNER.TAN: (0x9c, 0x73, 0x52),
    OWNER.GREEN: (0x42, 0x94, 0x29),
    OWNER.ORANGE: (0xff, 0x84, 0x00),
    OWNER.PURPLE: (0x8c, 0x29, 0xa5),
    OWNER.TEAL: (0x08, 0x9c, 0xa5),
    OWNER.PINK: (0xc6, 0x7b, 0x8c),
    OWNER.NEUTRAL: (0x84, 0x84, 0x84)
}

keymaster_colors = {
    KEYMASTER.LIGHTBLUE: (0x00, 0xb7, 0xff),
    KEYMASTER.GREEN: (0x06, 0xc6, 0x2f),
    KEYMASTER.RED: (0xCE, 0x19, 0x1A),
    KEYMASTER.DARKBLUE: (0x14, 0x14, 0xfe),
    KEYMASTER.BROWN: (0xc8, 0x82, 0x46),
    KEYMASTER.PURPLE: (0xa8, 0x43, 0xe0),
    KEYMASTER.WHITE: (0xf7, 0xf7, 0xf7),
    KEYMASTER.BLACK: (0x12, 0x12, 0x12),
    KEYMASTER.GARRISON: (0x9c, 0x9a, 0x8b),
    KEYMASTER.QUEST: (0xff, 0xff, 0x00)
}

object_colors = {
    OBJECTS.RED: (0xff, 0x00, 0x00),
    OBJECTS.BLUE: (0x31, 0x52, 0xff),
    OBJECTS.TAN: (0x9c, 0x73, 0x52),
    OBJECTS.GREEN: (0x42, 0x94, 0x29),
    OBJECTS.ORANGE: (0xff, 0x84, 0x00),
    OBJECTS.PURPLE: (0x8c, 0x29, 0xa5),
    OBJECTS.TEAL: (0x08, 0x9c, 0xa5),
    OBJECTS.PINK: (0xc6, 0x7b, 0x8c),
    OBJECTS.NEUTRAL: (0x84, 0x84, 0x84),
    OBJECTS.KM_LIGHTBLUE: (0x00, 0xb7, 0xff),
    OBJECTS.KM_GREEN: (0x06, 0xc6, 0x2f),
    OBJECTS.KM_RED: (0xCE, 0x19, 0x1A),
    OBJECTS.KM_DARKBLUE: (0x14, 0x14, 0xfe),
    OBJECTS.KM_BROWN: (0xc8, 0x82, 0x46),
    OBJECTS.KM_PURPLE: (0xa8, 0x43, 0xe0),
    OBJECTS.KM_WHITE: (0xf7, 0xf7, 0xf7),
    OBJECTS.KM_BLACK: (0x12, 0x12, 0x12),
    OBJECTS.GARRISON: (0x9c, 0x9a, 0x8b),
    OBJECTS.QUEST: (0xff, 0xff, 0x00)
}

ignored_owned_objects = {
    objects.ID.Hero,
    objects.ID.Prison,
    objects.ID.Random_Hero,
    objects.ID.Hero_Placeholder
}

passability_objects = {
    objects.ID.Border_Gate,
    objects.ID.Border_Guard,
    objects.ID.Quest_Guard,
    objects.ID.Garrison,
    objects.ID.Garrison_Vertical,
    objects.ID.Brush,
    objects.ID.Bush,
    objects.ID.Cactus,
    objects.ID.Canyon,
    objects.ID.Crater,
    objects.ID.Dead_Vegetation,
    objects.ID.Flowers,
    objects.ID.Frozen_Lake,
    objects.ID.Hedge,
    objects.ID.Hill,
    objects.ID.Hole,
    objects.ID.Kelp,
    objects.ID.Lake,
    objects.ID.Lava_Flow,
    objects.ID.Lava_Lake,
    objects.ID.Mushrooms,
    objects.ID.Log,
    objects.ID.Mandrake,
    objects.ID.Moss,
    objects.ID.Mound,
    objects.ID.Mountain,
    objects.ID.Oak_Trees,
    objects.ID.Outcropping,
    objects.ID.Pine_Trees,
    objects.ID.Plant,
    objects.ID.HotA_Decoration_1,
    objects.ID.HotA_Decoration_2,
    objects.ID.River_Delta,
    objects.ID.Rock,
    objects.ID.Sand_Dune,
    objects.ID.Sand_Pit,
    objects.ID.Shrub,
    objects.ID.Skull,
    objects.ID.Stalagmite,
    objects.ID.Stump,
    objects.ID.Tar_Pit,
    objects.ID.Trees,
    objects.ID.Vine,
    objects.ID.Volcanic_Vent,
    objects.ID.Volcano,
    objects.ID.Willow_Trees,
    objects.ID.Yucca_Trees,
    objects.ID.Reef,
    objects.ID.Brush_2,
    objects.ID.Bush_2,
    objects.ID.Cactus_2,
    objects.ID.Canyon_2,
    objects.ID.Crater_2,
    objects.ID.Dead_Vegetation_2,
    objects.ID.Flowers_2,
    objects.ID.Frozen_Lake_2,
    objects.ID.Hedge_2,
    objects.ID.Hill_2,
    objects.ID.Hole_2,
    objects.ID.Kelp_2,
    objects.ID.Lake_2,
    objects.ID.Lava_Flow_2,
    objects.ID.Lava_Lake_2,
    objects.ID.Mushrooms_2,
    objects.ID.Log_2,
    objects.ID.Mandrake_2,
    objects.ID.Moss_2,
    objects.ID.Mound_2,
    objects.ID.Mountain_2,
    objects.ID.Oak_Trees_2,
    objects.ID.Outcropping_2,
    objects.ID.Pine_Trees_2,
    objects.ID.Plant_2,
    objects.ID.River_Delta_2,
    objects.ID.Rock_2,
    objects.ID.Sand_Dune_2,
    objects.ID.Sand_Pit_2,
    objects.ID.Shrub_2,
    objects.ID.Skull_2,
    objects.ID.Stalagmite_2,
    objects.ID.Stump_2,
    objects.ID.Tar_Pit_2,
    objects.ID.Trees_2,
    objects.ID.Vine_2,
    objects.ID.Volcanic_Vent_2,
    objects.ID.Volcano_2,
    objects.ID.Willow_Trees_2,
    objects.ID.Yucca_Trees_2,
    objects.ID.Reef_2,
    objects.ID.Desert_Hills,
    objects.ID.Dirt_Hills,
    objects.ID.Grass_Hills,
    objects.ID.Rough_Hills,
    objects.ID.Subterranean_Rocks,
    objects.ID.Swamp_Foliage
}

#################
# MAIN FUNCTION #
#################

def generate_minimap(general, terrain, object_data, defs) -> bool:
    def main(general, terrain, object_data, defs) -> bool:
        input = xprint(menu=Menu.MINIMAP.value)
        if input == KB.ESC.value: return False
        xprint(type=Text.ACTION, text=f"Generating minimap...")
        # Get map size
        size = general["map_size"]
        # Initialize layer list
        if general["is_two_level"]:
            half = size * size
            layers = [terrain[:half]]  # overworld
            layers.append(terrain[half:])  # underground
        else:
            layers = [terrain]  # overworld only
        # Initialize tile dictionaries
        ownership = {layer: [[None for _ in range(size)] for _ in range(size)] for layer in [OVERWORLD, UNDERGROUND]}
        blocked_tiles = {layer: set() for layer in [OVERWORLD, UNDERGROUND]}
        # Iterate through objects
        for obj in object_data:
            if input == 2 and obj["type"] not in passability_objects:
                continue
            # Get object masks
            def_ = defs[obj["def_id"]]
            blockMask = def_["red_squares"]
            interactiveMask = def_["yellow_squares"]
            # Determine if object has owner and/or should be skipped (hidden on minimap).
            # If object is valid (should be shown on minimap), process it to determine blocked tiles and set tile ownership.
            owner = determine_owner(input, obj)
            if owner is None and should_skip_object(blockMask, interactiveMask):
                continue
            process_object(obj, blockMask, size, blocked_tiles, ownership, owner, input)
        # Generate and save minimap images
        generate_images(input, layers, size, blocked_tiles, ownership)
        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def determine_owner(input: int, obj: dict) -> Union[int, tuple]:
        if input == 1 and "owner" in obj and obj["type"] not in ignored_owned_objects:  # Check if object has "owner" key and should not be ignored
            return obj["owner"]
        elif input == 2:
            if (obj["type"] == objects.ID.Border_Gate and obj["subtype"] != 1001) or obj["type"] == objects.ID.Border_Guard:
                return obj["subtype"] + 1000
            elif obj["type"] == objects.ID.Garrison or obj["type"] == objects.ID.Garrison_Vertical:
                return (1999, obj["owner"])
            elif obj["type"] == objects.ID.Quest_Guard:
                return 2000
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

    def process_object(obj: dict, blockMask: list, size: int, blocked_tiles: dict, ownership: dict, owner: Union[int, tuple], input) -> None:
        obj_x, obj_y, obj_z = obj["coords"]  # Get the object's coordinates
        for r in range(ROWS):  # 6 rows y-axis, from top to bottom
            for c in range(COLUMNS):  # 8 columns x-axis, from left to right
                index = r * 8 + c  # Calculate the index into blockMask/interactiveMask
                if blockMask[index] != 1:
                    blocked_tile_x = obj_x - 7 + c
                    blocked_tile_y = obj_y - 5 + r
                    if 0 <= blocked_tile_x < size and 0 <= blocked_tile_y < size:  # Check if the blocked tile is within the map
                        if obj_z == OVERWORLD:
                            blocked_tiles[OVERWORLD].add((blocked_tile_x, blocked_tile_y))  # Add the coordinates of the blocked tile to the overworld set
                            if ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] is None:
                                if input == 2 and isinstance(owner, tuple):
                                    if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                        ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = owner[1]  # Set to owner color
                                    else:  # Outer tiles
                                        ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = owner[0]  # Set to garrison color
                                else:
                                    ownership[OVERWORLD][obj_y - 5 + r][obj_x - 7 + c] = owner if owner is not None else None
                        elif obj_z == UNDERGROUND:
                            blocked_tiles[UNDERGROUND].add((blocked_tile_x, blocked_tile_y))  # Add the coordinates of the blocked tile to the underground set
                            if ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] is None:
                                if input == 2 and isinstance(owner, tuple):
                                    if owner[1] != 255 and (r == 5 and c == 6 or r == 4 and c == 7):  # Middle tiles
                                        ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = owner[1]  # Set to owner color
                                    else:  # Outer tiles
                                        ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = owner[0]  # Set to garrison color
                                else:
                                    ownership[UNDERGROUND][obj_y - 5 + r][obj_x - 7 + c] = owner if owner is not None else None

    def generate_images(input: int, layers: list, size: int, blocked_tiles: dict, ownership: dict) -> None:
        for layer_index, layer in enumerate(layers):  # Iterate through both layers
            img = Image.new('RGB', (size, size))  # Initalize a new image the same dimensions as the map
            for i, tile in enumerate(layer):  # Iterate through each tile on this layer
                x = i % size
                y = i // size
                owner = ownership[layer_index][y][x]  # Check if this tile has an owner
                if owner is not None:
                    color = object_colors[owner]
                elif input == 1 and (x, y) in blocked_tiles[layer_index]:  # If tile coordinates are in the blocked_tiles set, use the blocked terrain color
                    color = terrain_colors[TERRAIN(tile[0]) + BLOCKED_OFFSET]
                elif input == 2 and (x, y) in blocked_tiles[layer_index]:  # If tile coordinates are in the blocked_tiles set, use the alternate blocked terrain color
                    color = terrain_colors_alt[TERRAIN(tile[0]) + BLOCKED_OFFSET]
                elif input == 1:
                    color = terrain_colors[tile[0]]  # Use the terrain color
                elif input == 2:
                    color = terrain_colors_alt[tile[0]]  # Use the alternate terrain color
                img.putpixel((x, y), color)  # Draw the pixel on the image
            img.save(os.path.join("..", "images", f"{general.get('name')}_layer_{layer_index}.png"))  # Save this layer's image in PNG format to the .\images directory

    return main(general, terrain, object_data, defs)