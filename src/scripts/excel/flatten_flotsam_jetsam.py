import data.objects as objects

def flatten_flotsam_jetsam(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}

        row["Zone"] = ""

        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        row["Contents"] = objects.Flotsam_Jetsam_Reward(obj.get("contents", "")).name.replace('_', ' ')
        rows.append(row)
    return rows
