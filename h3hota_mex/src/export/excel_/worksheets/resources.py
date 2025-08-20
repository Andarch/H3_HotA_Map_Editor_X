from .....core.data import objects
from .. import sort


def process(resource_objects):
    flattened = []

    for obj in resource_objects:
        flat = {}

        for k, v in obj.items():
            if k == "has_common":
                flat[k] = bool(v)
            elif k == "amount":
                subtype = obj.get("subtype", "")
                is_gold = False

                if hasattr(objects, "Resource") and hasattr(objects.Resource, "Gold"):
                    gold_val = getattr(objects.Resource, "Gold")
                    is_gold = (
                        subtype == gold_val
                        or (hasattr(subtype, "name") and subtype.name == "Gold")
                        or subtype == "Gold"
                    )
                else:
                    is_gold = subtype == "Gold"

                try:
                    amount_int = int(v)
                except Exception:
                    amount_int = None

                if amount_int == 0:
                    flat[k] = "Default"
                elif is_gold and amount_int is not None:
                    flat[k] = f"{amount_int:,} ({amount_int * 100:,})"
                elif amount_int is not None:
                    flat[k] = f"{amount_int:,}"
                else:
                    flat[k] = v
            else:
                flat[k] = v
        # Ensure "amount" is always present
        if "amount" not in flat:
            flat["amount"] = obj.get("amount", "")

        flattened.append(flat)

    flattened = sort.sort_by_zone(flattened)

    return flattened
