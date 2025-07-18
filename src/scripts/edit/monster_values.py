import data.objects as objects
from ...common import *

def set_compliant_monster_values(obj_data: list) -> bool:
    xprint(type=Text.ACTION, text="Setting compliant monster values...")

    count = 0
    for obj in obj_data:
        # Check if this is a monster (id 54) with zone_type "Player" and disposition "Compliant"
        if (obj.get("id") == objects.ID.Monster and
            obj.get("zone_type") == "Player" and
            obj.get("disposition") == 0):  # Disposition.Compliant = 0

            # Multiply ai_value by 3
            old_value = obj["ai_value"]
            obj["ai_value"] = old_value * 3
            count += 1

    xprint(type=Text.SPECIAL, text=DONE)
    xprint()
    xprint(type=Text.INFO, text=f"Updated {count} objects.")
    press_any_key()
    return True
