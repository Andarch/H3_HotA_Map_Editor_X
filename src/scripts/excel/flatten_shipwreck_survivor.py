import data.artifacts as artifacts
import data.objects as objects

from . import format, sort


def flatten_shipwreck_survivor(treasure_objects):
    rows = []

    for obj in treasure_objects:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        contents = obj.get("contents", "")
        row["contents"] = objects.Shipwreck_Survivor_Reward(contents).name

        if contents == 0:
            art = artifacts.ID(obj.get("artifact", "")).name.replace("_", " ")
            row["artifact"] = format.ARTIFACT_SPECIAL_CASES.get(art, art)
        else:
            row["artifact"] = ""

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
