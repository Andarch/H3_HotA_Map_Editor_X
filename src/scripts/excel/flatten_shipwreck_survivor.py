from . import format
import data.objects as objects
import data.artifacts as artifacts

def flatten_shipwreck_survivor(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        contents = obj.get("contents", "")
        row["Contents"] = objects.Shipwreck_Survivor_Reward(contents).name
        if contents == 0:
            art = artifacts.ID(obj.get("artifact", "")).name.replace('_', ' ')
            row["Artifact"] = format.ARTIFACT_SPECIAL_CASES.get(art, art)
        else:
            row["Artifact"] = ""
        rows.append(row)
    return rows
