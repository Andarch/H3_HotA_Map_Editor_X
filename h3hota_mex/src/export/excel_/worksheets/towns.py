from .....core.data import objects, spells
from .. import format


def process(objects_list) -> list:
    flattened_objects = []

    for obj in objects_list:
        flattened_obj = {}

        for key, value in obj.items():
            # Handle spells_must_appear and spells_cant_appear fields
            if key == "spells_must_appear":
                flattened_obj["Spells – Always"] = format.format_enum_list(value, spells.ID, format.SPELL_SPECIAL_CASES)
            elif key == "spells_cant_appear":
                flattened_obj["Spells – Disabled"] = format.format_enum_list(
                    value, spells.ID, format.SPELL_SPECIAL_CASES
                )
            # Handle buildings_built field
            elif key == "buildings_built":
                # Get regular buildings first
                regular_built = format.format_enum_list(value, objects.Town_Buildings)
                # Get special buildings that are built (state = 1)
                special_built = ""

                if "buildings_special" in obj:
                    special_built = format.format_special_buildings(obj["buildings_special"], state_filter=1)

                # Combine regular and special buildings
                all_built = []

                if regular_built:
                    all_built.append(regular_built)
                if special_built:
                    all_built.append(special_built)

                flattened_obj["Buildings – Built"] = ", ".join(all_built)
            # Handle buildings_disabled field
            elif key == "buildings_disabled":
                # Get regular buildings first
                regular_disabled = format.format_enum_list(value, objects.Town_Buildings)
                # Get special buildings that are disabled (state = 2)
                special_disabled = ""

                if "buildings_special" in obj:
                    special_disabled = format.format_special_buildings(obj["buildings_special"], state_filter=2)

                # Combine regular and special buildings
                all_disabled = []

                if regular_disabled:
                    all_disabled.append(regular_disabled)
                if special_disabled:
                    all_disabled.append(special_disabled)

                flattened_obj["Buildings – Disabled"] = ", ".join(all_disabled)
            # Handle special buildings fields - skip the old ones since we process buildings_special separately
            elif key.startswith("buildings_special_"):
                # Skip these old fields as they're replaced by buildings_special
                pass
            # Handle alignment field
            elif key == "alignment" and value is not None:
                alignment_enum = objects.Town_Alignment(value)
                flattened_obj[key] = alignment_enum.name.replace("_", " ")
            else:
                # Keep other fields as-is
                flattened_obj[key] = value

        flattened_objects.append(flattened_obj)

    return flattened_objects
