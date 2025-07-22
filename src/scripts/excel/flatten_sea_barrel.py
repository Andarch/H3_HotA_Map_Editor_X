import data.objects as objects

from . import sort


def flatten_sea_barrel(treasure_objects):
    rows = []

    for obj in treasure_objects:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        row["contents"] = objects.Sea_Barrel_Reward(obj.get("contents", "")).name.replace("_", " ")

        if row["contents"] == "Custom":
            row["resource"] = objects.Resource(obj.get("resource", "")).name
            row["amount"] = obj.get("amount", "")
        else:
            row["resource"] = ""
            row["amount"] = ""

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
