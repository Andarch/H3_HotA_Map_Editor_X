from . import format
import data.objects as objects
import data.artifacts as artifacts

def flatten_treasure_chest(treasure_objects):
    rows = []
    for obj in treasure_objects:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Zone"] = obj.get("zone", "")
        row["Subtype"] = obj.get("subtype", "")
        contents = obj.get("contents", "")
        row["Contents"] = objects.Treasure_Chest_Reward(contents).name
        if contents == 3:
            art = artifacts.ID(obj.get("artifact", "")).name.replace('_', ' ')
            if art == "Empty 4 Bytes":
                art = "Random"
            row["Artifact"] = format.ARTIFACT_SPECIAL_CASES.get(art, art)
        else:
            row["Artifact"] = ""
        rows.append(row)
    return rows
