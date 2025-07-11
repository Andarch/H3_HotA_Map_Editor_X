"""
Flattens and formats artifact object data for Excel export.
"""
import data.artifacts as artifacts

def flatten_artifacts(artifact_objects):
    """
    Flatten artifact object data for Excel export.

    Args:
        artifact_objects: List of artifact object dictionaries

    Returns:
        List of flattened artifact dictionaries ready for Excel export
    """
    flattened = []
    for obj in artifact_objects:
        flat = {}
        # Copy all fields except those we want to transform
        for k, v in obj.items():
            if k == "has_common":
                flat[k] = bool(v)
            elif k == "guards":
                # guards is a list of dicts with 'id' and 'amount'
                guards_list = []
                for guard in v:
                    guard_id = getattr(guard['id'], 'value', guard['id'])
                    # skip NONE (65535)
                    if guard_id == 65535:
                        continue
                    guards_list.append(f"{guard['id'].name.replace('_', ' ').title()}: {guard['amount']}")
                flat[k] = "\n".join(guards_list)
            elif k == "pickup_mode":
                # pickup_mode is a single value, use artifacts.Pickup_Mode
                if hasattr(artifacts, "Pickup_Mode"):
                    try:
                        mode = artifacts.Pickup_Mode(v)
                        flat[k] = mode.name.replace('_', ' ').title()
                    except Exception:
                        flat[k] = v
                else:
                    flat[k] = v
            elif k == "pickup_conditions":
                # Only display pickup_conditions if pickup_mode is 2 (Customized)
                mode_val = obj.get("pickup_mode")
                mode_enum = None
                if hasattr(artifacts, "Pickup_Mode"):
                    try:
                        mode_enum = artifacts.Pickup_Mode(mode_val)
                    except Exception:
                        mode_enum = None
                if (mode_enum is not None and mode_enum.value == 2) or (mode_val == 2):
                    # pickup_conditions is a list of ints, use artifacts.Pickup_Conditions
                    if hasattr(artifacts, "Pickup_Conditions") and isinstance(v, list):
                        names = []
                        for i, val in enumerate(v):
                            if val:
                                try:
                                    cond = list(artifacts.Pickup_Conditions)[i]
                                    names.append(cond.name.replace('_', ' ').title())
                                except IndexError:
                                    pass
                        flat[k] = "\n".join(names)
                    else:
                        flat[k] = v
                else:
                    flat[k] = ""
            else:
                flat[k] = v
        # Ensure 'message' column is always present
        if "message" not in flat:
            flat["message"] = obj.get("message", "")
        flattened.append(flat)
    return flattened
