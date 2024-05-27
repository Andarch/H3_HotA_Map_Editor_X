from ..common import *

def count_objects(object_data: dict) -> None:
    print_action("Counting objects...")
    print()

    object_list = {}

    for obj in object_data:
        key = (obj["type"], obj["subtype"])
        if key in object_list:
            object_list[key] += 1
        else: object_list[key] = 1

    for k,v in sorted(object_list.items()):
        print(f"    {v} {'.'*(9-len(str(v)))}", k)

    print()
    print_done()
