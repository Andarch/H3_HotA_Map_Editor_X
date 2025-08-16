import data.objects as objects

from ...common import DONE, Text, map_data, xprint


def modify_towns(events: bool = False) -> None:
    if not events:
        msg = "Enabling spell research, spells, and buildings for all towns..."
    else:
        msg = "Enabling spell research, spells, buildings, and events for all towns..."
    xprint(type=Text.ACTION, text=msg)

    for obj in map_data["object_data"]:
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
