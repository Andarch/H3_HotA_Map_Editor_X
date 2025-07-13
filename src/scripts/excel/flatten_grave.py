from . import format
import data.objects as objects
import data.artifacts as artifacts

def flatten_grave(graves):
    rows = []
    for obj in graves:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        row["Contents"] = objects.Grave_Reward(obj.get("contents", "")).name.replace('_', ' ')
        if row["Contents"] == "Custom":
            amount = obj.get("amount", "")
            amount_str = f"{int(amount):,}"
            row["Amount"] = f"+{amount_str} Gold"
            art = artifacts.ID(obj.get("artifact", "")).name.replace('_', ' ')
            row["Artifact"] = format.ARTIFACT_SPECIAL_CASES.get(art, art)
        else:
            row["Amount"] = ""
            row["Artifact"] = ""
        rows.append(row)
    return rows
