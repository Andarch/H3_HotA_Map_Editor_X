import data.objects as objects

from . import sort


def flatten_vial_of_mana(treasure_objects):
    rows = []

    for obj in treasure_objects:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        row["contents"] = objects.Vial_of_Mana_Reward(obj.get("contents", "")).name.replace("_", " ")

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
