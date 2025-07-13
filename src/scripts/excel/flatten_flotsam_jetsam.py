"""
Flattens and formats flotsam & jetsam object data for Excel export.
"""

def flatten_flotsam_jetsam(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        contents = obj.get("contents", "")
        if contents == 4294967295:
            row["Contents"] = "Random"
        else:
            row["Contents"] = contents
        rows.append(row)
    return rows
