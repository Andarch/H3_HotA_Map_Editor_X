#!/usr/bin/env python3

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
