from . import format
import data.creatures as creatures
import data.artifacts as artifacts


def flatten_monsters(monsters):
    flattened_monsters = []

    for monster in monsters:
        flattened_monster = {}

        # Basic monster information
        flattened_monster["coords"] = monster.get("coords", [])
        flattened_monster["zone"] = monster.get("zone", "")

        # Monster type and subtype
        flattened_monster["id"] = monster.get("id", "")
        flattened_monster["sub_id"] = monster.get("sub_id", "")
        flattened_monster["type"] = monster.get("type", "")
        flattened_monster["subtype"] = monster.get("subtype", "")

        # Monster details
        flattened_monster["quantity"] = monster.get("quantity", 0)

        # AI value
        flattened_monster["is_value"] = monster.get("is_value", False)
        flattened_monster["ai_value"] = monster.get("ai_value", 0)

        # Format disposition
        disposition = monster.get("disposition", "")
        if hasattr(disposition, 'name'):
            flattened_monster["disposition"] = disposition.name.replace('_', ' ').title()
        else:
            flattened_monster["disposition"] = str(disposition)

        # Precise disposition
        precise_disposition = monster.get("precise_disposition", 0)
        flattened_monster["precise_disposition"] = "" if precise_disposition == 4294967295 else precise_disposition

        # Monster behavior flags
        flattened_monster["monster_never_flees"] = monster.get("monster_never_flees", False)
        flattened_monster["quantity_does_not_grow"] = monster.get("quantity_does_not_grow", False)
        flattened_monster["join_only_for_money"] = monster.get("join_only_for_money", False)
        flattened_monster["joining_monster_percent"] = monster.get("joining_monster_percent", 0)

        # Stack information
        upgraded_stack = monster.get("upgraded_stack", 0)
        stack_count = monster.get("stack_count", 0)
        flattened_monster["upgraded_stack"] = "Default" if upgraded_stack == 4294967295 else upgraded_stack
        flattened_monster["stack_count"] = "Default" if stack_count == 4294967295 else stack_count

        # Message and rewards (if monster has them)
        if "message" in monster:
            flattened_monster["message"] = monster["message"]

            # Format resources
            resources = monster.get("resources", [])
            if resources and len(resources) >= 7:
                resource_names = ["Wood", "Mercury", "Ore", "Sulfur", "Crystal", "Gems", "Gold"]
                resource_lines = []
                for i, amount in enumerate(resources):
                    if amount != 0 and i < len(resource_names):
                        sign = "+" if amount > 0 else ""
                        resource_lines.append(f"{sign}{amount:,} {resource_names[i]}")
                flattened_monster["resources"] = "\n".join(resource_lines) if resource_lines else ""
            else:
                flattened_monster["resources"] = ""

            # Format artifact reward
            artifact_id = monster.get("artifact", "")
            if artifact_id and artifact_id != artifacts.ID.Empty_2_Bytes:
                try:
                    # Try to get artifact name from ID
                    artifact_name = artifacts.ID(artifact_id).name
                    # Format the name first, then apply special cases
                    formatted_name = artifact_name.replace('_', ' ').title()
                    flattened_monster["artifact"] = format.ARTIFACT_SPECIAL_CASES.get(formatted_name, formatted_name)
                except (ValueError, AttributeError):
                    flattened_monster["artifact"] = str(artifact_id)
            else:
                flattened_monster["artifact"] = ""
        else:
            flattened_monster["message"] = ""
            flattened_monster["resources"] = ""
            flattened_monster["artifact"] = ""

        flattened_monsters.append(flattened_monster)

    return flattened_monsters
