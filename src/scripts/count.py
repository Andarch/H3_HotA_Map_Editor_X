#!/usr/bin/env python3

###################
## COUNT OBJECTS ##
###################

def count_objects(obj_data: dict) -> None:
    print("\n---[ Counting objects (v.101) ]---")
    print("\n[ Amount ] (Type, Subtype)\n")

    obj_list = {}

    for obj in obj_data:
        key = (obj["type"], obj["subtype"])
        if key in obj_list:
            obj_list[key] += 1
        else: obj_list[key] = 1

    for k,v in sorted(obj_list.items()):
        print(f"{v} {'.'*(9-len(str(v)))}", k)

    print("\n---[ Finished counting objects ]---")
