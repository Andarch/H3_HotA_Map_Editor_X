import data.objects as objects
import math
from ...common import *

def set_compliant_monster_values(obj_data: list) -> bool:
    xprint(type=Text.ACTION, text="Setting compliant monster values...")

    count = 0
    for obj in obj_data:
        # Check if this is a monster (id 54) with zone_type "Player" and disposition "Compliant"
        if (obj.get("id") == objects.ID.Monster and
            obj.get("zone_type") == "Player" and
            obj.get("disposition") == 0):  # Disposition.Compliant = 0

            match obj["ai_value"]:
                case 1000:
                    obj["ai_value"] = 3000
                case 1500:
                    obj["ai_value"] = 10000
                case 2000:
                    obj["ai_value"] = 15000
                case 2500:
                    obj["ai_value"] = 25000
                case 10000:
                    obj["ai_value"] = 100000

            count += 1

    xprint(type=Text.SPECIAL, text=DONE)
    xprint()
    xprint(type=Text.INFO, text=f"Updated {count} objects.")
    press_any_key()
    return True
