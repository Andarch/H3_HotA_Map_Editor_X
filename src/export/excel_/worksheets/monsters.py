import src.core.artifacts as artifacts

from .. import format, sort


def process(monsters):
    flattened = []

    for monster in monsters:
        flat = {}

        # Basic monster information
        flat["coords"] = monster.get("coords", [])
        flat["zone_type"] = monster.get("zone_type", "")
        flat["zone_color"] = monster.get("zone_color", "")

        # Monster type and subtype
        flat["def_id"] = monster.get("def_id", "")
        flat["id"] = monster.get("id", "")
        flat["sub_id"] = monster.get("sub_id", "")
        flat["type"] = monster.get("type", "")
        flat["subtype"] = monster.get("subtype", "")

        # Monster details
        flat["quantity"] = monster.get("quantity", 0)

        # AI value
        flat["is_value"] = monster.get("is_value", False)
        flat["ai_value"] = monster.get("ai_value", 0)

        # Format disposition
        disposition = monster.get("disposition", "")

        if hasattr(disposition, "name"):
            flat["disposition"] = disposition.name.replace("_", " ").title()
        else:
            flat["disposition"] = str(disposition)

        # Precise disposition
        precise_disposition = monster.get("precise_disposition", 0)
        flat["precise_disposition"] = "" if precise_disposition == 4294967295 else precise_disposition

        # Monster behavior flags
        flat["no_flee"] = monster.get("monster_never_flees", False)
        flat["no_grow"] = monster.get("quantity_does_not_grow", False)
        flat["join_for_money"] = monster.get("join_only_for_money", False)
        flat["join_percent"] = monster.get("joining_monster_percent", 0)

        # Stack information
        upgraded_stack = monster.get("upgraded_stack", 0)
        stack_count = monster.get("stack_count", 0)
        flat["upgraded"] = "Default" if upgraded_stack == 4294967295 else upgraded_stack
        flat["stack_count"] = "Default" if stack_count == 4294967295 else stack_count

        # Message and rewards (if monster has them)
        if "message" in monster:
            flat["message"] = monster["message"]

            # Format resources
            resources = monster.get("resources", [])

            if resources and len(resources) >= 7:
                resource_names = ["Wood", "Mercury", "Ore", "Sulfur", "Crystal", "Gems", "Gold"]
                resource_lines = []

                for i, amount in enumerate(resources):
                    if amount != 0 and i < len(resource_names):
                        sign = "+" if amount > 0 else ""
                        resource_lines.append(f"{sign}{amount:,} {resource_names[i]}")

                flat["resources"] = "\n".join(resource_lines) if resource_lines else ""
            else:
                flat["resources"] = ""

            # Format artifact reward
            artifact_id = monster.get("artifact", "")

            if artifact_id and artifact_id != artifacts.ID.Empty_2_Bytes:
                try:
                    # Try to get artifact name from ID
                    artifact_name = artifacts.ID(artifact_id).name
                    # Format the name first, then apply special cases
                    formatted_name = artifact_name.replace("_", " ").title()
                    flat["artifact"] = format.ARTIFACT_SPECIAL_CASES.get(formatted_name, formatted_name)
                except (ValueError, AttributeError):
                    flat["artifact"] = str(artifact_id)
            else:
                flat["artifact"] = ""
        else:
            flat["message"] = ""
            flat["resources"] = ""
            flat["artifact"] = ""

        flattened.append(flat)

    flattened = sort.sort_by_zone(flattened)

    return flattened
