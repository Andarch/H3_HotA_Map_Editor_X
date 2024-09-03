from ..common import *
from enum import IntEnum
from pprint import pprint
from tabulate import tabulate
import data.objects as objects

class TOWN_TABLE(IntEnum):
    RESOURCES = 1
    CREATURES = 2

#################
# MAIN FUNCTION #
#################

def update_events(global_events: list, obj_data: list) -> None:
    # Filter global events with non-zero resources
    global_events = [event for event in global_events if not all_slots_zero(event["resources"])]
    for event in global_events:
        event["resources"] = convert_resources(event["resources"])

    town_events_resources = []
    town_events_creatures = []
    for obj in obj_data:
        if obj["type"] is not objects.ID.Town and obj["type"] is not objects.ID.Random_Town:
            continue
        if "events" not in obj or obj["events"] is None:
            continue
        # Filter events with non-zero resources and creatures
        non_zero_resource_events = []
        non_zero_creature_events = []
        for event in obj["events"]:
            if not all_slots_zero(event["resources"]):
                event["resources"] = convert_resources(event["resources"])
                non_zero_resource_events.append(event)
            if not all_slots_zero(event["creatures"]):
                event["creatures"] = convert_resources(event["creatures"])
                non_zero_creature_events.append(event)
        if non_zero_resource_events:
            town_events_resources.append({
                "name": obj.get("name", "Random"),
                "events": non_zero_resource_events
            })
        if non_zero_creature_events:
            town_events_creatures.append({
                "name": obj.get("name", "Random"),
                "events": non_zero_creature_events
            })

    while True:
        print("Select an option:")
        print_cyan("   1. Global Events (Resources)")
        print_cyan("   2. Town Events (Resources)")
        print_cyan("   3. Town Events (Creatures)")
        print_cyan("   4. Back")
        print()
        option = detect_key_press("1234")

        if option == "1":
            update_global_events(global_events)
            continue
        elif option == "2":
            update_town_events(town_events_resources, TOWN_TABLE.RESOURCES)
            continue
        elif option == "3":
            update_town_events(town_events_creatures, TOWN_TABLE.CREATURES)
            continue
        elif option == "4":
            break
        else:
            print_error("Error: Invalid option. Please try again.")

####################
# HELPER FUNCTIONS #
####################

def all_slots_zero(slots: list) -> bool:
    return all(slot == 0 for slot in slots)

def convert_resources(resources: list) -> list:
    return [convert_resource_value(value) for value in resources]

def convert_resource_value(value) -> str:
    if isinstance(value, str):
        value = int(value)
    if value > 2147483647:  # 2^31 - 1, the maximum positive value for a 32-bit signed integer
        value = value - 4294967296  # 2^32, the range of a 32-bit unsigned integer
    if value > 0:
        return f"+{value}"
    return str(value)

def color_number(value: str) -> str:
    if value.startswith('+'):
        return f"{CLR.GREEN}{value}{CLR.RESET}"  # Green for positive numbers
    elif value.startswith('-'):
        return f"{CLR.RED}{value}{CLR.RESET}"  # Red for negative numbers
    return value

#################
# GLOBAL EVENTS #
#################

def update_global_events(global_events: list) -> None:
    if not global_events:
        print_error("No global events found.")
        return

    table = []
    headers = [
        "#",
        "EVENT NAME",
        "WOOD",
        "MERCURY",
        "ORE",
        "SULFUR",
        "CRYSTAL",
        "GEMS",
        "GOLD"
    ]

    for i, event in enumerate(global_events):
        resources = event["resources"]
        table.append([
            i + 1,
            event["name"],
            color_number(str(resources[0])),
            color_number(str(resources[1])),
            color_number(str(resources[2])),
            color_number(str(resources[3])),
            color_number(str(resources[4])),
            color_number(str(resources[5])),
            color_number(str(resources[6]))
        ])

    print(tabulate(table, headers, tablefmt = "fancy_grid"))
    print()

###############
# TOWN EVENTS #
###############

def update_town_events(town_events: list, table_type: int) -> None:
    table = []
    headers = []
    if table_type == TOWN_TABLE.RESOURCES:
        headers = [
            "#",
            "TOWN NAME",
            "#",
            "EVENT NAME",
            "WOOD",
            "MERCURY",
            "ORE",
            "SULFUR",
            "CRYSTAL",
            "GEMS",
            "GOLD"
        ]
    elif table_type == TOWN_TABLE.CREATURES:
        headers = [
            "#",
            "TOWN NAME",
            "#",
            "EVENT NAME",
            "LEVEL 1",
            "LEVEL 2",
            "LEVEL 3",
            "LEVEL 4",
            "LEVEL 5",
            "LEVEL 6",
            "LEVEL 7"
        ]
    blank_row = [""] * len(headers)

    n1 = 0
    for i, town in enumerate(town_events):
        n1 += 1
        # print(f"Processing town: {town}")
        if "name" not in town:
            town["name"] = "Random"
        n2 = 0
        if "events" not in town or town["events"] is None:
            continue
        for event in town["events"]:
            n2 += 1
            if table_type == TOWN_TABLE.RESOURCES:
                if all_slots_zero(event["resources"]):
                    continue
                resources = event["resources"]
                table.append([
                    n1,
                    town["name"],
                    n2,
                    event["name"],
                    color_number(str(resources[0])),
                    color_number(str(resources[1])),
                    color_number(str(resources[2])),
                    color_number(str(resources[3])),
                    color_number(str(resources[4])),
                    color_number(str(resources[5])),
                    color_number(str(resources[6]))
                ])
            elif table_type == TOWN_TABLE.CREATURES:
                if all_slots_zero(event["creatures"]):
                    continue
                creatures = event["creatures"]
                table.append([
                    n1,
                    town["name"],
                    n2,
                    event["name"],
                    color_number(str(creatures[0])),
                    color_number(str(creatures[1])),
                    color_number(str(creatures[2])),
                    color_number(str(creatures[3])),
                    color_number(str(creatures[4])),
                    color_number(str(creatures[5])),
                    color_number(str(creatures[6]))
                ])
        if i < len(town_events) - 1:
            table.append(blank_row)

    if table:
        print(tabulate(table, headers, tablefmt = "fancy_grid"))
        print()
    else:
        print_error("No events found for the selected table type.")
