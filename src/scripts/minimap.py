#!/usr/bin/env python3

from enum import IntEnum
from PIL import Image
import data.objects as od # Object details

#############################
## GENERATE MINIMAP IMAGES ##
#############################

# Constants
OVERWORLD = 0
UNDERGROUND = 1
IMAGE_SIZE = 1024

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
    
class TILETYPE(IntEnum):
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

def process_object(obj, defs, size, ownership_overworld, ownership_underground):
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

    x, y, z = obj["coords"]

    # Get the owner of the object
    owner = obj.get("owner")
    obj_type = obj.get("type")  # get the type of the object
    obj_name = od.ID(obj_type).name  # get the name of the object type

    # Map raw integer owner value to corresponding OWNER instance
    if owner is not None:
        owner = OWNER(owner)

    # Subtract 1 from x and y to get 0-based indices
    x -= 1
    y -= 1

    if owner is not None:
        # Debug: Print owner, object type and object coordinates
        print(f"Owner: {owner}")
        print(f"Object Name: {obj_name}")
        print(f"Object coordinates: {x}, {y}, {z}")
        print()  # line break
        try:
            if z == 0:  # overworld
                ownership_overworld[y][x] = owner.value
            elif z == 1:  # underground
                ownership_underground[y][x] = owner.value
        except IndexError:
            print(f"IndexError for object at coordinates: {x}, {y}, {z}")

    for r in range(6):  # 6 rows y-axis, from top to bottom
        for c in range(8):  # 8 columns x-axis, from left to right
            index = r * 8 + c  # Calculate the index into blockMask
            if blockMask[index] == 1:  # Check if the value at index in blockMask is 1
                # Draw regular terrain
                pass
            else:
                if 0 <= x - 7 + c < size and 0 <= y - 5 + r < size:  # Adjust the coordinates here
                    if z == 0:  # overworld
                        ownership_overworld[y - 5 + r][x - 7 + c] = owner.value if owner is not None else TILETYPE.BLOCKED.value
                    elif z == 1:  # underground
                        ownership_underground[y - 5 + r][x - 7 + c] = owner.value if owner is not None else TILETYPE.BLOCKED.value

    return blockMask, index

def determine_color(tile_value, owner, blockMask, index):
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

    # If there's an owner, return the owner's color
    if owner is not None:
        owner_enum = OWNER(owner)  # Convert integer to OWNER enum
        print(f"Owner: {owner_enum}, Type: {type(owner_enum)}")  # Debug line
        return color_mapping[owner_enum]

    # If the tile is blocked, return the blocked terrain color
    if blockMask[index] == 0:
        return color_mapping[getattr(TERRAIN, 'B' + tile_value.name.upper())]

    # If the tile is not blocked, return the terrain color
    return color_mapping[tile_value]

def main(general, terrain, objects, defs):
    size = general.get("map_size")
    half = size * size
    layers = [terrain[:half]]  # overworld
    if general.get("is_two_level", False):
        layers.append(terrain[half:])  # underground

    # initialize ownership lists
    ownership_layers = [
        [[None for _ in range(size)] for _ in range(size)],  # overworld
        [[None for _ in range(size)] for _ in range(size)]  # underground
    ]
    ownership_overworld, ownership_underground = ownership_layers

    for obj in objects:
        blockMask, index = process_object(obj, defs, size, ownership_overworld, ownership_underground)

    # create images for each layer
    for layer_index, (layer, ownership) in enumerate(zip(layers, ownership_layers)):
        img = Image.new('RGB', (size, size))  # create an image with the same size as the map
        for i, tile in enumerate(layer):
            x = i % size
            y = i // size
            color = determine_color(tile[0], ownership[y][x], blockMask, index)  # determine color based on terrain type and owner
            img.putpixel((x, y), color)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.HAMMING)  # resize the image to 1024x1024 using the HAMMING filter
        img.save(f".\\images\\{general.get('name')}_layer_{layer_index}.png")
