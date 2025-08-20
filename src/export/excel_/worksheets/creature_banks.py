import src.core.artifacts as artifacts
import src.core.objects as objects

from .. import sort


def process(creature_banks):
    rows = []

    for obj in creature_banks:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        row["difficulty"] = objects.Creature_Bank_Difficulty(obj.get("difficulty", "")).name.replace("_", " ")

        if (
            obj.get("id") != objects.ID.Dragon_Utopia
            and row["difficulty"] == "Random"
            or obj.get("id") == objects.ID.Dragon_Utopia
        ):
            row["upgraded_stack"] = ""
        else:
            row["upgraded_stack"] = objects.Creature_Bank_Stack(obj.get("upgraded_stack", "")).name.replace("_", " ")

        if obj.get("id") == objects.ID.Dragon_Utopia and row["difficulty"] == "Random":
            row["artifacts"] = ""
        else:
            arts = obj.get("artifacts", [])
            art_names = []

            for art_num in arts:
                art_name = artifacts.ID(art_num).name.replace("_", " ")

                if art_name == "Empty 4 Bytes":
                    art_name = "Random"

                art_names.append(art_name)

            row["artifacts"] = "\n".join(art_names)

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
