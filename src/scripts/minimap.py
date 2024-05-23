#!/usr/bin/env python3

from enum import Enum
from PIL import Image

import data.objects as od # Object details

#############################
## GENERATE MINIMAP IMAGES ##
#############################

class OWNER(Enum):
    RED = 0
    BLUE = 1
    TAN = 2
    GREEN = 3
    ORANGE = 4
    PURPLE = 5
    TEAL = 6
    PINK = 7
    NEUTRAL = 255
    
class TILETYPE(Enum):
    FREE = 0
    ACCESSIBLE = 1
    BLOCKED = 2
    USED = 3

class TERRAIN:
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

def main(general, terrain, objects, defs):
    size = general.get("map_size")
    half = size * size
    layers = [terrain[:half]]  # overworld
    if general.get("is_two_level", False):
        layers.append(terrain[half:])  # underground

    # initialize ownership lists
    ownership_overworld = [[None for _ in range(size)] for _ in range(size)]
    ownership_underground = [[None for _ in range(size)] for _ in range(size)]

    for obj in objects:
        print(f"Processing object {obj}")

        # Get the correct definition using obj["def_id"]
        def_ = defs[obj["def_id"]]

        print(f'Object type: {obj["type"]}')
        print(f'Object subtype: {obj["subtype"]}')
        print(f'Definition type: {def_["type"]}')
        print(f'Definition subtype: {def_["subtype"]}')

        # Get blockMask and visitMask from the definition
        blockMask = def_.get("red_squares", None)
        visitMask = def_.get("yellow_squares", None)

        # Print the blockMask bits for debugging
        if blockMask is not None:
            for i, mask in enumerate(blockMask):
                print(f"blockMask bit {i}: {bin(mask)}")

        # Skip interactive objects
        if visitMask and any(mask != 0 for mask in visitMask):
            print("Skipping interactive object")
            continue

        # Skip objects that don't have blockMask
        if not blockMask:
            print("Skipping object without blockMask")
            print(f"Object: {obj}")  # Print the entire object
            continue

        x, y, z = obj["coords"]
        print(f"Object coordinates: ({x}, {y}, {z})")

        print(f"Entire blockMask: {blockMask}")

        for r in range(6):  # 6 rows y-axis, from top to bottom
            for c in range(8):  # 8 columns x-axis, from left to right
                index = r * 8 + c  # Calculate the index into blockMask
                print(f"blockMask[{index}]: {blockMask[index]}")
                if blockMask[index] == 1:  # Check if the value at index in blockMask is 1
                    print(f"Bit is passable at position ({r}, {c}) in blockMask")
                    # Draw regular terrain
                else:
                    print(f"Bit is blocked at position ({r}, {c}) in blockMask")
                    if 0 <= x - 7 + c < size and 0 <= y - 5 + r < size:  # Adjust the coordinates here
                        print(f"Drawing obstacle at coordinates: ({x - 7 + c}, {y - 5 + r}, {z})")
                        if z == 0:  # overworld
                            ownership_overworld[y - 5 + r][x - 7 + c] = TILETYPE.BLOCKED.value  # And here
                        elif z == 1:  # underground
                            ownership_underground[y - 5 + r][x - 7 + c] = TILETYPE.BLOCKED.value  # And here

    # create images for each layer
    ownership_layers = [ownership_overworld]
    if general.get("is_two_level", False):
        ownership_layers.append(ownership_underground)

    for layer_index, (layer, ownership) in enumerate(zip(layers, ownership_layers)):
        img = Image.new('RGB', (size, size))  # create an image with the same size as the map
        for i, tile in enumerate(layer):
            x = i % size
            y = i // size
            color = determine_color(tile[0], ownership[y][x])  # determine color based on terrain type and owner
            img.putpixel((x, y), color)
        img = img.resize((1024, 1024), Image.HAMMING)  # resize the image to 1024x1024 using the HAMMING filter
        img.save(f".\\images\\{general.get('name')}_layer_{layer_index}.png")

def determine_color(tile_value, owner):
    color_mapping = {
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
        # Player colors
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

    # If there's an obstacle on the tile, return the color associated with the blocked terrain
    if owner is not None:
        return color_mapping[getattr(TERRAIN, 'B' + tile_value.name.upper())]

    # If there's no obstacle on the tile, return the color associated with the tile_value
    return color_mapping[tile_value]
