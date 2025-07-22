import data.spells as spells
from . import sort


def flatten_spells(spell_objects):
    flattened = []
    for obj in spell_objects:
        flat = {}

        flat["coords"] = obj.get("coords", "")
        flat["zone_type"] = obj.get("zone_type", "")
        flat["zone_color"] = obj.get("zone_color", "")
        flat["subtype"] = obj.get("subtype", "")
        # Merge "spell" and "contents" into "spell" column
        spell_val = ""
        if "spell" in obj:
            val = obj["spell"]
            if val == spells.ID.Random_1_Byte:
                spell_val = "Default"
            elif hasattr(val, "name"):
                spell_val = val.name.replace("_", " ").title()
            else:
                spell_val = str(val)
        elif "contents" in obj:
            val = obj["contents"]
            if val == 4294967295 or (hasattr(spells.ID, "Random_4_Bytes") and val == spells.ID.Random_4_Bytes):
                spell_val = "Default"
            else:
                spell_val = val
        flat["spell"] = spell_val
        flattened.append(flat)

    flattened = sort.sort_by_zone(flattened)
    return flattened
