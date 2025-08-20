from .....core.data import objects
from .. import sort


def process(treasure_objects):
    rows = []

    for obj in treasure_objects:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        row["contents"] = objects.Sea_Chest_Reward(obj.get("contents", "")).name.replace("_", " ")

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
