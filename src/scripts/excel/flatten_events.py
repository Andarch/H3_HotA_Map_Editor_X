"""
Flattens global event data for Excel export.
"""


def flatten_events(events):
    """
    Flatten global events data for Excel export.

    Args:
        events: List of global event dictionaries

    Returns:
        List of flattened global event dictionaries
    """
    flattened_events = []

    if not events:
        return flattened_events

    for event in events:
        # Process global events (similar structure to town events but without town context)
        global_event = {}

        # Basic event information
        global_event["Event Name"] = event.get("name", "")
        global_event["Message"] = event.get("message", "")

        # Resources
        resources = event.get("resources", [])
        if len(resources) >= 7:
            resource_names = ["Wood", "Mercury", "Ore", "Sulfur", "Crystal", "Gems", "Gold"]
            resource_lines = []
            for i, amount in enumerate(resources):
                if amount != 0 and i < len(resource_names):
                    sign = "+" if amount > 0 else ""
                    resource_lines.append(f"{sign}{amount:,} {resource_names[i]}")
            global_event["Resources"] = "\n".join(resource_lines) if resource_lines else ""

        # Player application
        apply_to = event.get("apply_to", [])
        if isinstance(apply_to, list) and len(apply_to) >= 8:
            applied_players = []
            for i, applies in enumerate(apply_to):
                if applies == 1:
                    applied_players.append(f"Player {i+1}")
            global_event["Players"] = "\n".join(applied_players) if applied_players else "None"

        # Event settings
        global_event["Human"] = True if event.get("apply_human", False) else False
        global_event["AI"] = True if event.get("apply_ai", False) else False

        # Format First occurrence as "Day X" (add 1 since 0-based)
        first_occurrence = event.get("first_occurence", "")
        if first_occurrence != "" and first_occurrence is not None:
            global_event["First"] = f"Day {first_occurrence + 1}"
        else:
            global_event["First"] = ""

        # Format Repeat based on subsequent_occurences value
        next_occurrence = event.get("subsequent_occurences", 0)
        if next_occurrence == 0:
            global_event["Repeat"] = ""
        elif next_occurrence == 1:
            global_event["Repeat"] = "Every day"
        else:
            global_event["Repeat"] = f"Every {next_occurrence} days"

        flattened_events.append(global_event)

    return flattened_events
