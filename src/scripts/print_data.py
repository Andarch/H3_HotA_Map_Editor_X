
import pprint

from ..common import *

PRINT_WIDTH = 120

def print_data(map_key: dict, data_key: str) -> None:
    print_action("Retrieving map data...")

    print_done()

    if data_key in map_key:
        data = pprint.pformat(map_key[data_key], width=PRINT_WIDTH)
        print_cyan(data)
        print()
    else:
        print_error("Error: Unrecognized data key.")

    print()
