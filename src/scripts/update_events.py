from ..common import *

#################
# MAIN FUNCTION #
#################

def update_events() -> None:

    # Allow user to select between global and town events
    while True:
        print("Select an option:")
        print("1. Global Events")
        print("2. Town Events")
        print("3. Back")
        option = input("Enter a number: ")

        if option == "1":
            update_global_events()
        elif option == "2":
            update_town_events()
        elif option == "3":
            break
        else:
            print_error("Error: Invalid option. Please try again.")



#################
# GLOBAL EVENTS #
#################

def update_global_events() -> None:
    print("Global Events")

###############
# TOWN EVENTS #
###############

def update_town_events() -> None:
    print("Town Events")
