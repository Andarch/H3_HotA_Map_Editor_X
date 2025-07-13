import data.objects as objects

def flatten_ancient_lamp(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        row["Contents"] = objects.Ancient_Lamp_Reward(obj.get("contents", "")).name.replace('_', ' ')
        if row["Contents"] == "Custom":
            row["Amount"] = obj.get("amount", "")
        else:
            row["Amount"] = ""
        rows.append(row)
    return rows
