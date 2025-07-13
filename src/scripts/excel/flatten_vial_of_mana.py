import data.objects as objects

def flatten_vial_of_mana(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        row["Contents"] = objects.Vial_of_Mana_Reward(obj.get("contents", "")).name.replace('_', ' ')
        rows.append(row)
    return rows
