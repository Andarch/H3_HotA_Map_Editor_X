from src.defs import artifacts

from .. import format, sort


def process(artifact_objects):
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
                    guard_id = getattr(guard["id"], "value", guard["id"])
                    # skip NONE (65535)
                    if guard_id == 65535:
                        continue
                    amount_str = f"{guard['amount']:,}"
                    guards_list.append(f"{guard['id'].name.replace('_', ' ').title()}: {amount_str}")
                flat[k] = "\n".join(guards_list)
            elif k == "pickup_mode":
                # pickup_mode is a single value, use artifacts.Pickup_Mode
                if hasattr(artifacts, "Pickup_Mode"):
                    try:
                        mode = artifacts.PickupMode(v)
                        flat[k] = mode.name.replace("_", " ").title()
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
                        mode_enum = artifacts.PickupMode(mode_val)
                    except Exception:
                        mode_enum = None
                if (mode_enum is not None and mode_enum.value == 2) or (mode_val == 2):
                    # pickup_conditions is a list of ints, use artifacts.Pickup_Conditions
                    if hasattr(artifacts, "Pickup_Conditions") and isinstance(v, list):
                        names = []
                        for i, val in enumerate(v):
                            if val:
                                try:
                                    cond = list(artifacts.PickupConditions)[i]
                                    names.append(cond.name.replace("_", " "))
                                except IndexError:
                                    pass
                        flat[k] = "\n".join(names)
                    else:
                        flat[k] = v
                else:
                    flat[k] = ""
            elif k == "subtype":
                # Ensure Subtype (artifact name) is processed through ARTIFACT_SPECIAL_CASES
                name = str(v).replace("_", " ")
                name = format.ARTIFACT_SPECIAL_CASES.get(name, name)
                flat[k] = name
            else:
                flat[k] = v
        # Ensure 'message' column is always present
        if "message" not in flat:
            flat["message"] = obj.get("message", "")
        flattened.append(flat)

    flattened = sort.sort_by_zone(flattened)

    return flattened
