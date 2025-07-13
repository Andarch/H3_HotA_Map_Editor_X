"""
Flattens and formats treasure chest object data for Excel export.
"""

def flatten_treasure_chest(treasure_objects):
    """
    Flatten treasure chest object data for Excel export.
    Columns: Coords, Subtype, Contents, Artifact, Resource, Amount (in this order).
    Fills missing columns with empty strings for consistency.
    Replaces 4294967295 in Contents with 'Random'.
    """
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
        row["Artifact"] = obj.get("artifact", "")
        rows.append(row)
    return rows
