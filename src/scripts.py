#!/usr/bin/env python3

from random import choice, randint
from enum import Enum
from PIL import Image

import data.creatures as cd # Creature details
import data.objects   as od # Object details
import json

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

    # # players
    # RED = 40
    # BLUE = 41
    # TAN = 42
    # GREEN = 43
    # ORANGE = 44
    # PURPLE = 45
    # TEAL = 46
    # PINK = 47
    # NEUTRAL = 48

def generate_minimap_images(general, terrain, objects, defs):
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
    }

    # If there's an obstacle on the tile, return the color associated with the blocked terrain
    if owner is not None:
        return color_mapping[getattr(TERRAIN, 'B' + tile_value.name.upper())]

    # If there's no obstacle on the tile, return the color associated with the tile_value
    return color_mapping[tile_value]

#################
## JSON EXPORT ##
#################

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('latin-1')
        return json.JSONEncoder.default(self, obj)

def export_to_json(map_data: dict, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(map_data, f, cls=CustomEncoder, indent=4)

###################
## TOWN SETTINGS ##
###################

def town_settings(obj_data: dict) -> dict:
    for obj in obj_data:
        if obj["type"] == od.ID.Town or obj["type"] == od.ID.Random_Town:
            # Enable spell research
            obj["spell_research"] = True

            # Enable all spells

            for i in range(len(obj["spells_cant_appear"])):
                obj["spells_cant_appear"][i] = 0

            # Enable all buildings
            if "buildings_disabled" in obj:
                for i in range(len(obj["buildings_disabled"])):
                    obj["buildings_disabled"][i] = 0
            else:
                obj["has_fort"] = True

            print(f"Enabled all settings for town at {obj['coords']}")
    return obj_data

#################
## SWAP LAYERS ##
#################

def swap_layers(terrain, object_data, player_specs, is_two_level, conditions):
    if not is_two_level:
        print("Error: This map does not have an underground layer to swap with the overworld.")
        return
    
    print("Swapping terrain...")

    # Swap terrain tiles between the two layers
    half = len(terrain) // 2
    terrain[:half], terrain[half:] = \
        terrain[half:], terrain[:half]
    
    print("Swapping objects...")

    # Update the z-coordinate for objects to swap layers
    for obj in object_data:
        if obj["coords"][2] == 0:
            obj["coords"][2] = 1  # Move to underground
        elif obj["coords"][2] == 1:
            obj["coords"][2] = 0  # Move to overworld
    
    print("Swapping main town coords...")

    # Change main town coords in player data
    for player in player_specs:
        if "town_coords" in player and player["town_coords"] is not None:
            player["town_coords"][2] = 1 if player["town_coords"][2] == 0 else 0
    
    print("Swapping win/loss conditions...")

    # Swap victory condition coordinates
    if "objective_coords" in conditions:
        conditions["objective_coords"][2] = \
            1 if conditions["objective_coords"][2] == 0 else 0

    # Swap loss condition coordinates
    if "loss_coords" in conditions:
        conditions["loss_coords"][2] = \
            1 if conditions["loss_coords"][2] == 0 else 0

    print("Layers swapped successfully.")

###################
## COUNT OBJECTS ##
###################

def count_objects(obj_data: dict) -> None:
    print("\n---[ Counting objects (v.101) ]---")
    print("\n[ Amount ] (Type, Subtype)\n")

    obj_list = {}

    for obj in obj_data:
        key = (obj["type"], obj["subtype"])
        if key in obj_list:
            obj_list[key] += 1
        else: obj_list[key] = 1

    for k,v in sorted(obj_list.items()):
        print(f"{v} {'.'*(9-len(str(v)))}", k)

    print("\n---[ Finished counting objects ]---")

#####################
## GENERATE GUARDS ##
#####################

AMOUNT = [
    [    5, "a few ({1-4}) "           ],
    [   10, "several ({5-9}) "         ],
    [   20, "a pack ({10-19}) of "     ],
    [   50, "lots ({20-49}) of "       ],
    [  100, "a horde ({50-99}) of "    ],
    [  250, "a throng ({100-249}) of " ],
    [  500, "a swarm ({250-499}) of "  ],
    [ 1000, "zounds ({500-999}) of "   ]
]

FACTIONS = {
    "Castle"    : [   0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13 ],
    "Rampart"   : [  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27 ],
    "Tower"     : [  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41 ],
    "Inferno"   : [  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55 ],
    "Necropolis": [  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69, 141 ],
    "Dungeon"   : [  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83 ],
    "Stronghold": [  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97 ],
    "Fortress"  : [  98,  99, 100, 101, 106, 107, 104, 105, 102, 103, 108, 109, 110, 111 ],
    "Conflux"   : [ 118, 119, 112, 127, 115, 123, 114, 129, 113, 125, 120, 121, 130, 131 ],
    "Cove"      : [ 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 151 ],
    "Factory"   : [ 138, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185 ],
    "Neutral"   : [ 139, 143, 140, 169, 142, 167, 137, 170, 116, 117, 168, 144, 136, 135, 134, 133, 132 ]
}

def get_creature_text(creature: int, amount: int) -> str:
    text = "a legion ({1000+}) of "
    for pair in AMOUNT:
        if amount < pair[0]:
            text = pair[1]
            break
    return text + cd.NAME[creature]

def generate_guards(obj_data: dict) -> dict:
    print("\n---[ Generating guards (v.110) ]---\n")

    valid_types = {
        od.ID.Pandoras_Box            : "{Pandora's Box}\n",
        od.ID.Artifact                : "{Artifact}\n",
        od.ID.Random_Artifact         : "{Artifact}\n",
        od.ID.Random_Treasure_Artifact: "{Artifact}\n",
        od.ID.Random_Minor_Artifact   : "{Artifact}\n",
        od.ID.Random_Major_Artifact   : "{Artifact}\n",
        od.ID.Random_Relic            : "{Artifact}\n",
        od.ID.Event                   : "",
        od.ID.Resource                : "{Resources}\n",
        od.ID.Spell_Scroll            : "{Spell Scroll}\n",
    }

    for obj in obj_data:
        if obj["type"] not in valid_types.keys() or not "message" in obj:
            continue

        # Split the message box into a list of separate lines
        # and check if the last line contains "-guards xxx".
        obj_message = obj["message"].split('\n')
        last_line = obj_message[-1].split(' ')

        if last_line[0] != "-guards":
            continue

        if not last_line[1].isdigit():
            continue

        # If there's no message for the object (other than the desired AI
        # value), then we generate a simple title and a yes/no prompt later.
        add_prompt = len(obj_message) == 1

        desired_guard_value = int(last_line[1])

        # Make sure that the desired guard value is large enough.
        if desired_guard_value < 1000:
            print("\nThe guard value for", obj["type"], "at", obj["coords"],
                f"is too low! ({desired_guard_value}). Min value is 1000.\n")
            continue

        # Limit the number of stacks so that the minimum
        # AI value of a single stack is at least 5000.
        max_num = max(min(round(desired_guard_value / 5000), 7), 3)
        creature_num = randint(2, max_num)
        max_creature_value = desired_guard_value / creature_num

        # Get a list of creatures from two random factions.
        creature_list = []
        creature_list += choice(list(FACTIONS.values()))
        creature_list += choice(list(FACTIONS.values()))

        obj["guards"] = []
        generated_ai_value = 0

        # Generate random creatures from the list.
        for _ in range(creature_num):
            temp_id = 65535
            temp_amount = 0

            while temp_amount == 0:
                temp_id = choice(creature_list)
                temp_amount = round(max_creature_value / cd.AI_VALUE[temp_id])

            obj["guards"].append({ "id": temp_id, "amount": temp_amount })
            generated_ai_value += cd.AI_VALUE[temp_id] * temp_amount

        if obj["type"] != od.ID.Event:
            # Get the total amount of each creature (necessary if
            # there's more than one stack of a type of creature).
            total_guards = {}
            for c in obj["guards"]:
                if c["id"] in total_guards:
                    total_guards[c["id"]] += c["amount"]
                else: total_guards[c["id"]] = c["amount"]

            # Create a sentence describing all the guards.
            guard_list = []
            for k, v in total_guards.items():
                guard_list.append(get_creature_text(k, v))

            guard_text = "Guarded by "
            last_guard = " and " + guard_list.pop()
            guard_text += ", ".join(guard_list) + last_guard

            # Reconstruct the message box of the object.
            if add_prompt:
                obj_message.insert(0, valid_types[obj["type"]])

            obj_message[-1] = guard_text
            obj["message"] = "\n".join(obj_message)

            # No yes/no prompt for a Pandora's Box since it always has one.
            if add_prompt and obj["type"] != od.ID.Pandoras_Box:
                obj["message"] += "\n\nDo you wish to fight the guards?"

        # Fill remaining guard slots (up to 7) with correct blank data.
        for _ in range(7-creature_num):
            obj["guards"].append({ "id": 65535, "amount": 65535 })

        print(f"Generated guards for", obj["type"], "at", obj["coords"],
              "for a total AI value of", generated_ai_value,
              f"({desired_guard_value} desired)")

    print("\n---[ Finished generating guards ]---")
    return obj_data
