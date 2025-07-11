import data.objects as objects
from ..common import *

def modify_towns(obj_data: dict) -> bool:
    xprint(type=Text.ACTION, text="Enabling all buildings/spells and spell research for all towns...")

    for obj in obj_data:
        if obj["id"] == objects.ID.Town or obj["id"] == objects.ID.Random_Town:
            # Enable spell research
            obj["spell_research"] = True

            # Enable all spells
            for i in range(len(obj["spells_must_appear"])):
                obj["spells_must_appear"][i] = 0
            for i in range(len(obj["spells_cant_appear"])):
                obj["spells_cant_appear"][i] = 0

            # Enable all buildings
            if "buildings_disabled" in obj:
                for i in range(len(obj["buildings_disabled"])):
                    obj["buildings_disabled"][i] = 0
            else:
                obj["has_fort"] = True

    xprint(type=Text.SPECIAL, text=DONE)
    return True
