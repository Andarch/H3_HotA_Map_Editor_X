import data.objects as objects
from src.scripts import excel


def flatten_town_events(event, town_obj):
    """Flatten town event data into a readable format"""
    flattened_event = {}

    # Match the first 4 columns from Towns sheet
    flattened_event["Coords"] = town_obj.get("coords", [0, 0, 0])
    flattened_event["Subtype"] = town_obj.get("subtype", "")
    flattened_event["Color"] = town_obj.get("color", "")
    flattened_event["Town Name"] = town_obj.get("name", "")

    # Event-specific information
    flattened_event["Event Name"] = event.get("name", "")
    flattened_event["Message"] = event.get("message", "")

    # Resources
    resources = event.get("resources", [])
    if len(resources) >= 7:
        resource_names = ["Wood", "Mercury", "Ore", "Sulfur", "Crystal", "Gems", "Gold"]
        resource_lines = []
        for i, amount in enumerate(resources):
            if amount != 0 and i < len(resource_names):
                sign = "+" if amount > 0 else ""
                resource_lines.append(f"{sign}{amount:,} {resource_names[i]}")
        flattened_event["Resources"] = "\n".join(resource_lines) if resource_lines else ""

    # Player application
    apply_to = event.get("apply_to", [])
    if isinstance(apply_to, list) and len(apply_to) >= 8:
        applied_players = []
        for i, applies in enumerate(apply_to):
            if applies == 1:
                applied_players.append(f"Player {i+1}")
        flattened_event["Players"] = "\n".join(applied_players) if applied_players else "None"

    # Event settings
    flattened_event["Human"] = True if event.get("apply_human", False) else False
    flattened_event["AI"] = True if event.get("apply_ai", False) else False

    # Format First occurrence as "Day X" (add 1 since 0-based)
    first_occurrence = event.get("first_occurence", "")
    if first_occurrence != "" and first_occurrence is not None:
        flattened_event["First"] = f"Day {first_occurrence + 1}"
    else:
        flattened_event["First"] = ""

    # Format Repeat based on subsequent_occurences value
    next_occurrence = event.get("subsequent_occurences", 0)
    if next_occurrence == 0:
        flattened_event["Repeat"] = ""
    elif next_occurrence == 1:
        flattened_event["Repeat"] = "Every day"
    else:
        flattened_event["Repeat"] = f"Every {next_occurrence} days"

    # Town-specific event data (if available)
    if event.get("isTown", False):
        # Creatures for town events
        creatures = event.get("creatures", [])
        if creatures and len(creatures) >= 7:
            creature_lines = []
            creature_names = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7"]
            for i, amount in enumerate(creatures):
                if amount != 0 and i < len(creature_names):
                    sign = "+" if amount > 0 else ""
                    creature_lines.append(f"{sign}{amount:,} {creature_names[i]}")
            flattened_event["Creatures"] = "\n".join(creature_lines) if creature_lines else ""

        # HotA-specific fields
        flattened_event["Neutral Towns"] = True if event.get("apply_neutral_towns", False) else False

        # Buildings
        buildings = event.get("buildings", [])
        if buildings and isinstance(buildings, list):
            # Get regular buildings from the event
            regular_built = excel.format.format_enum_list(buildings, objects.Town_Buildings)
            # Get special buildings from the event's hota_special field
            special_built = ""
            if "hota_special" in event:
                special_built = excel.format.format_special_buildings(event["hota_special"], state_filter=1)

            # Combine regular and special buildings
            all_built = []
            if regular_built:
                all_built.append(regular_built)
            if special_built:
                all_built.append(special_built)

            flattened_event["Buildings"] = ", ".join(all_built) if all_built else ""

    return flattened_event
