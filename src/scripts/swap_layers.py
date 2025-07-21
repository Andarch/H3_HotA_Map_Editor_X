from ..common import *

def swap_layers(terrain, object_data, player_specs, has_underground, conditions):
    if not has_underground:
        print_error("Error: This map does not have an underground layer to swap with the overworld.")
        return

    print_action("Swapping layers...")

    # Swap terrain tiles between the two layers
    half = len(terrain) // 2
    terrain[:half], terrain[half:] = \
        terrain[half:], terrain[:half]

    # Update the z-coordinate for objects to swap layers
    for obj in object_data:
        if obj["coords"][2] == 0:
            obj["coords"][2] = 1  # Move to underground
        elif obj["coords"][2] == 1:
            obj["coords"][2] = 0  # Move to overworld

    # Change main town coords in player data
    for player in player_specs:
        if "town_coords" in player and player["town_coords"] is not None:
            player["town_coords"][2] = 1 if player["town_coords"][2] == 0 else 0

    # Swap victory condition coordinates
    if "objective_coords" in conditions:
        conditions["objective_coords"][2] = \
            1 if conditions["objective_coords"][2] == 0 else 0

    # Swap loss condition coordinates
    if "loss_coords" in conditions:
        conditions["loss_coords"][2] = \
            1 if conditions["loss_coords"][2] == 0 else 0

    print_done()
