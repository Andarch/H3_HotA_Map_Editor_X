from ..common import *
from pprint import pprint

#################
# MAIN FUNCTION #
#################

def update_events(all_events: dict) -> None:
    events = sort_events(all_events)
    while True:
        print("Select an option:")
        print("   1. Global Events")
        print("   2. Town Events")
        print("   3. Back")
        print()
        option = print_prompt("Enter a number")

        if option == "1":
            update_global_events(events["global"])
            break
        elif option == "2":
            update_town_events(events["towns"])
            break
        elif option == "3":
            break
        else:
            print_error("Error: Invalid option. Please try again.")

####################
# HELPER FUNCTIONS #
####################

def sort_events(all_events: dict) -> dict:
    events = {
        "global": [],
        "towns" : []
    }
    for event in all_events:
        if event["isTown"]:
            events["towns"].append(event)
        else:
            events["global"].append(event)
    return events

#################
# GLOBAL EVENTS #
#################

def update_global_events(global_events: dict) -> None:
    if not global_events:
        print_error("No global events found.")
        return

    pprint(global_events)
    print()

###############
# TOWN EVENTS #
###############

def update_town_events(town_events: dict) -> None:
    if not town_events:
        print_error("No town events found.")
        return

    pprint(town_events)
    print()
