"""
Flattens and formats sea barrel object data for Excel export.
"""

def flatten_sea_barrel(treasure_objects):
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
        row["Resource"] = obj.get("resource", "")
        row["Amount"] = obj.get("amount", "")
        rows.append(row)
    return rows
