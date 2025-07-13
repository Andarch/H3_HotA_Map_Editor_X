import data.objects as objects

def flatten_sea_barrel(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        row["Contents"] = objects.Sea_Barrel_Reward(obj.get("contents", "")).name.replace('_', ' ')
        if row["Contents"] == "Custom":
            row["Resource"] = objects.Resource(obj.get("resource", "")).name
            row["Amount"] = obj.get("amount", "")
        else:
            row["Resource"] = ""
            row["Amount"] = ""
        rows.append(row)
    return rows
