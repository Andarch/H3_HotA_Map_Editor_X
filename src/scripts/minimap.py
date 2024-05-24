#!/usr/bin/env python3

from enum import IntEnum
from PIL import Image
import data.objects as od # Object details

# Constants
OVERWORLD = 0
UNDERGROUND = 1
IMAGE_SIZE = 1024

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

owner_colors = {
    OWNER.RED: (0xff, 0x00, 0x00),
    OWNER.BLUE: (0x31, 0x52, 0xff),
    OWNER.TAN: (0x9c, 0x73, 0x52),
    OWNER.GREEN: (0x42, 0x94, 0x29),
    OWNER.ORANGE: (0xff, 0x84, 0x00),
    OWNER.PURPLE: (0x8c, 0x29, 0xa5),
    OWNER.TEAL: (0x08, 0x9c, 0xa5),
    OWNER.PINK: (0xc6, 0x7b, 0x8c),
    OWNER.NEUTRAL: (0x84, 0x84, 0x84),
}

############################################################################
#                                  MAIN                                    #
############################################################################

def main(general, terrain, objects, defs):
    size = general["map_size"]
    half = size * size
    layers = [terrain[:half]]  # overworld
    if general["is_two_level"]:
        layers.append(terrain[half:])  # underground

    # Initialize ownership lists
    ownership_layers = [
        [[None for _ in range(size)] for _ in range(size)],  # overworld
        [[None for _ in range(size)] for _ in range(size)]  # underground
    ]
    ownership_overworld, ownership_underground = ownership_layers

    # Create sets to store the indices of all blocked tiles
    blocked_tiles_overworld = set()
    blocked_tiles_underground = set()

    ######################################
    #          Process objects           #
    ######################################

    for obj in objects:
        # Determine the object's owner
        if "owner" in obj and obj["type"] not in {od.ID.Hero, od.ID.Prison, od.ID.Random_Hero, od.ID.Hero_Placeholder}:
            owner = obj["owner"]
        else:
            owner = None

        # Get masks for blocked and interactive tiles
        def_ = defs[obj["def_id"]]
        blockMask = def_["red_squares"]
        interactiveMask = def_["yellow_squares"]

        # End this iteration of the loop (skip the object) under conditions where we don't want to draw the object on the minimap
        if owner is None:
            isInteractive = False
            yellowSquaresOnly = True
            allPassable = True
            for b, i in zip(blockMask, interactiveMask):
                if i == 1:  # If there is an interactive tile
                    isInteractive = True
                if b == i:  # If the elements are the same, then one is not the inverse of the other
                    yellowSquaresOnly = False
                if b != 1:  # If there is a blocked tile
                    allPassable = False
                if not yellowSquaresOnly and isInteractive and not allPassable:
                    break
            if isInteractive and yellowSquaresOnly:
                continue
            if allPassable:
                continue
        
        # Complete object processing to determine blocked tiles and ownership
        obj_x, obj_y, obj_z = obj["coords"]
        for r in range(6):  # 6 rows y-axis, from top to bottom
            for c in range(8):  # 8 columns x-axis, from left to right
                index = r * 8 + c  # Calculate the index into blockMask/interactiveMask
                if blockMask[index] != 1:  # If tile is blocked
                    blocked_tile_x = obj_x - 7 + c
                    blocked_tile_y = obj_y - 5 + r
                    if 0 <= blocked_tile_x < size and 0 <= blocked_tile_y < size:  # Check if the blocked tile is within the map
                        if obj_z == OVERWORLD:
                            blocked_tiles_overworld.add((blocked_tile_x, blocked_tile_y))  # Add the coordinates of the blocked tile to the overworld set
                            if ownership_overworld[obj_y - 5 + r][obj_x - 7 + c] is None:
                                ownership_overworld[obj_y - 5 + r][obj_x - 7 + c] = owner if owner is not None else None
                        elif obj_z == UNDERGROUND:
                            blocked_tiles_underground.add((blocked_tile_x, blocked_tile_y))  # Add the coordinates of the blocked tile to the underground set
                            if ownership_underground[obj_y - 5 + r][obj_x - 7 + c] is None:
                                ownership_underground[obj_y - 5 + r][obj_x - 7 + c] = owner if owner is not None else None

    ####################################
    #          Create images           #
    ####################################

    # Create images for each layer
    for layer_index, (layer, ownership) in enumerate(zip(layers, ownership_layers)):
        img = Image.new('RGB', (size, size))  # create an image with the same size as the map
        for i, tile in enumerate(layer):
            x = i % size
            y = i // size
            owner = ownership[y][x]
            if owner is not None:  # If there's an owner, use the owner's color
                color = owner_colors[OWNER(owner)]
            elif layer_index == 0 and (x, y) in blocked_tiles_overworld:  # If tile coordinates are in the blocked_tiles set for overworld, use the blocked terrain color
                color = terrain_colors[TERRAIN(tile[0]) + 20]
            elif layer_index == 1 and (x, y) in blocked_tiles_underground:  # If tile coordinates are in the blocked_tiles set for underground, use the blocked terrain color
                color = terrain_colors[TERRAIN(tile[0]) + 20]
            else:
                color = terrain_colors[tile[0]]  # Use the terrain color

            img.putpixel((x, y), color)

        img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.NEAREST)  # resize the image
        img.save(f".\\images\\{general.get('name')}_layer_{layer_index}.png")
