def flatten_garrisons(garrison_objects):
    flattened = []

    for obj in garrison_objects:
        flat = {}

        # Copy all fields except those we want to transform
        for k, v in obj.items():
            if k == "guards":
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
            elif k == "troops_removable":
                flat[k] = bool(v)
            else:
                flat[k] = v

        flattened.append(flat)

    return flattened
