"""
Flattens and formats treasure object data for Excel export.
"""

def flatten_treasure(treasure_objects):
    """
    Flatten treasure object data for Excel export.

    Args:
        treasure_objects: List of treasure object dictionaries

    Returns:
        List of flattened treasure dictionaries ready for Excel export
    """
    # Collect all possible keys
    all_keys = set()
    for obj in treasure_objects:
        all_keys.update(obj.keys())
    flattened = []
    for obj in treasure_objects:
        flat = {}
        for k in all_keys:
            v = obj.get(k, "")
            if k == "has_common":
                flat[k] = bool(v) if v != "" else ""
            else:
                flat[k] = v
        flattened.append(flat)
    return flattened
