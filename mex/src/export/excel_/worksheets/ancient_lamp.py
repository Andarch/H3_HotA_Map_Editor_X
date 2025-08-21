from core.h3 import objects

from .. import sort


def process(treasure_objects):
    rows = []

    for obj in treasure_objects:
        row = {}
        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        row["contents"] = objects.Ancient_Lamp_Reward(obj.get("contents", "")).name.replace("_", " ")
        if row["contents"] == "Custom":
            row["amount"] = obj.get("amount", "")
        else:
            row["amount"] = ""
        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
