import src.core.creatures as creatures
import src.core.objects as objects

from ...common import DONE, Text, map_data, wait_for_keypress, xprint


def set_compliant_monster_values() -> None:
    xprint(type=Text.ACTION, text="Setting compliant monster values...")

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj.get("id") == objects.ID.Monster
            and obj.get("zone_type") == "Player"
            and obj.get("disposition") == creatures.Disposition.Compliant
        ):

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
    xprint(type=Text.INFO, text=f"\nUpdated {count} objects.")

    wait_for_keypress()
