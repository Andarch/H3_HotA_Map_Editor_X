from core.h3m import artifacts, objects

from .. import format, sort


def process(graves):
    rows = []

    for obj in graves:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        row["contents"] = objects.Grave_Reward(obj.get("contents", "")).name.replace("_", " ")

        if row["contents"] == "Custom":
            amount = obj.get("amount", "")
            amount_str = f"{int(amount):,}"
            row["amount"] = f"+{amount_str} Gold"
            art = artifacts.ID(obj.get("artifact", "")).name.replace("_", " ")
            row["artifact"] = format.ARTIFACT_SPECIAL_CASES.get(art, art)
        else:
            row["amount"] = ""
            row["artifact"] = ""

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
