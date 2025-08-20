from .....core.data import artifacts, objects
from .. import format, sort


def process(treasure_objects):
    rows = []

    for obj in treasure_objects:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        contents = obj.get("contents", "")
        row["contents"] = objects.Treasure_Chest_Reward(contents).name

        if contents == 3:
            art = artifacts.ID(obj.get("artifact", "")).name.replace("_", " ")

            if art == "Empty 4 Bytes":
                art = "Random"

            row["artifact"] = format.ARTIFACT_SPECIAL_CASES.get(art, art)
        else:
            row["artifact"] = ""

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
