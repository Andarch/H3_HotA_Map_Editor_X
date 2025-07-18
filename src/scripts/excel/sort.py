# No imports


def sort_by_zone(flattened: list) -> list:
    ZONE_TYPE_ORDER = {"Player": 1, "Normal": 2, "Treasure": 3, "Red": 4}
    ZONE_COLOR_ORDER = {"Blue": 1, "Tan": 2, "Green": 3, "Orange": 4, "Purple": 5, "Teal": 6, "Pink": 7}

    # Sort by zone type first, then by zone color within each type
    flattened.sort(key=lambda x: (
        ZONE_TYPE_ORDER.get(x.get("zone_type", ""), 5),
        ZONE_COLOR_ORDER.get(x.get("zone_color", ""), 8)
    ))

    return flattened
