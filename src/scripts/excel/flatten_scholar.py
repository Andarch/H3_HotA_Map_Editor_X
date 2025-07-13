import data.objects as objects
import data.skills as skills
import data.spells as spells

def flatten_scholar(scholars):
    rows = []
    for obj in scholars:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Subtype"] = obj.get("subtype", "")
        reward_type = obj.get("reward_type", "")
        match reward_type:
            case objects.Scholar_Reward.Random:
                row["Reward Type"] = "Random"
                row["Reward Value"] = ""
            case objects.Scholar_Reward.Primary_Skill:
                row["Reward Type"]  = "Primary Skill"
                row["Reward Value"] = skills.Primary(obj.get("reward_value", "")).name
            case objects.Scholar_Reward.Secondary_Skill:
                row["Reward Type"] = "Secondary Skill"
                row["Reward Value"] = skills.Secondary(obj.get("reward_value", "")).name
            case objects.Scholar_Reward.Spell:
                row["Reward Type"] = "Spell"
                row["Reward Value"] = spells.ID(obj.get("reward_value", "")).name
        rows.append(row)
    return rows
