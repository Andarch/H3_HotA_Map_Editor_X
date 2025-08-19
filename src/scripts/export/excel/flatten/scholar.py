import data.objects as objects
import data.skills as skills
import data.spells as spells

from .. import sort


def flatten(scholars):
    rows = []

    for obj in scholars:
        row = {}

        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        reward_type = obj.get("reward_type", "")

        match reward_type:
            case objects.Scholar_Reward.Random:
                row["reward_type"] = "Random"
                row["reward_value"] = ""
            case objects.Scholar_Reward.Primary_Skill:
                row["reward_type"] = "Primary Skill"
                row["reward_value"] = skills.Primary(obj.get("reward_value", "")).name
            case objects.Scholar_Reward.Secondary_Skill:
                row["reward_type"] = "Secondary Skill"
                row["reward_value"] = skills.Secondary(obj.get("reward_value", "")).name
            case objects.Scholar_Reward.Spell:
                row["reward_type"] = "Spell"
                row["reward_value"] = spells.ID(obj.get("reward_value", "")).name

        rows.append(row)

    rows = sort.sort_by_zone(rows)

    return rows
