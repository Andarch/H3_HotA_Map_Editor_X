#!/usr/bin/env python3

import data.objects   as od # Object details

###################
## TOWN SETTINGS ##
###################

def main(obj_data: dict) -> dict:
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
