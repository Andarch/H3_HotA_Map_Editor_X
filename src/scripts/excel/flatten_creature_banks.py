from . import format
from ...common import *
import data.objects as objects
import data.artifacts as artifacts

def flatten_creature_banks(creature_banks):
    rows = []
    for obj in creature_banks:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        row["Difficulty"] = objects.Creature_Bank_Difficulty(obj.get("difficulty", "")).name.replace('_', ' ')

        if obj.get("id") != objects.ID.Dragon_Utopia and row["Difficulty"] == "Random" or obj.get("id") == objects.ID.Dragon_Utopia:
            row["Upgraded Stack"] = ""
        else:
            row["Upgraded Stack"] = objects.Creature_Bank_Stack(obj.get("upgraded_stack", "")).name.replace('_', ' ')

        if obj.get("id") == objects.ID.Dragon_Utopia and row["Difficulty"] == "Random":
            row["Artifacts"] = ""
        else:
            arts = obj.get("artifacts", [])
            art_names = []
            for art_num in arts:
                art_name = artifacts.ID(art_num).name.replace('_', ' ')
                if art_name == "Empty 4 Bytes":
                    art_name = "Random"
                art_names.append(art_name)
            row["Artifacts"] = "\n".join(art_names)
        rows.append(row)
    return rows
