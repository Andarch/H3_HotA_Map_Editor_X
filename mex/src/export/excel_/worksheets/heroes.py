import os

from core.h3 import heroes, spells

from .. import format


def process(objects) -> list:
    processed_objects = []

    for obj in objects:
        processed_obj = {}

        for key, value in obj.items():
            if key == "hero_data" and isinstance(value, dict):
                # Flatten hero data dictionaries using just the sub-key names
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        # Handle artifacts_equipped specially
                        if sub_key == "artifacts_equipped":
                            # Extract artifact names, ignoring empty slots
                            artifact_names = []

                            for _, artifact_data in sub_value.items():
                                if isinstance(artifact_data, list) and len(artifact_data) >= 2:
                                    artifact_id = artifact_data[0]

                                    # Skip empty artifacts (ID 65535)
                                    if artifact_id != 65535 and str(artifact_id) != "<ID.Empty_2_Bytes: 65535>":
                                        # Extract artifact name from enum
                                        artifact_name = ""

                                        if hasattr(artifact_id, "name"):
                                            artifact_name = artifact_id.name.replace("_", " ")
                                        elif ":" in str(artifact_id) and "." in str(artifact_id):
                                            # Handle format like "<ID.Pendant_of_Reflection: 123>"
                                            artifact_name = (
                                                str(artifact_id).split(".")[1].split(":")[0].replace("_", " ")
                                            )
                                        else:
                                            artifact_name = str(artifact_id).replace("_", " ")

                                        if artifact_name:
                                            artifact_names.append(artifact_name)

                            processed_obj["artifacts"] = "\n".join(artifact_names) if artifact_names else ""
                        else:
                            # Flatten other nested dictionaries (like primary_skills)
                            for nested_key, nested_value in sub_value.items():
                                processed_obj[nested_key] = nested_value
                    elif isinstance(sub_value, list):
                        # Special formatting for secondary_skills
                        if sub_key == "secondary_skills" and sub_value:
                            skill_lines = []

                            for skill in sub_value:
                                if isinstance(skill, dict):
                                    level_name = skill.get("level_name", "")
                                    skill_name = skill.get("name", "").replace("_", " ")

                                    if level_name and skill_name:
                                        skill_lines.append(f"{level_name} {skill_name}")

                            processed_obj[sub_key] = "\n".join(skill_lines) if skill_lines else ""
                        # Special formatting for creatures
                        elif sub_key == "creatures" and sub_value:
                            creature_lines = []

                            for creature in sub_value:
                                if isinstance(creature, dict):
                                    creature_id = creature.get("id", "")
                                    amount = creature.get("amount", "")

                                    # Skip creatures with 0 amount
                                    if not amount or amount == 0:
                                        continue

                                    # Extract creature name from ID enum string representation
                                    creature_name = ""

                                    if creature_id:
                                        id_str = str(creature_id)

                                        # Handle different possible enum formats
                                        if ":" in id_str and "." in id_str:
                                            # Format: "<ID.Arch_Devil: 55>" -> "Arch Devil"
                                            creature_name = id_str.split(".")[1].split(":")[0].replace("_", " ")
                                        elif hasattr(creature_id, "name"):
                                            # Direct access to enum name
                                            creature_name = creature_id.name.replace("_", " ")
                                        else:
                                            # Fallback: use string representation
                                            creature_name = str(creature_id).replace("_", " ")

                                    if creature_name and amount:
                                        creature_lines.append(f"{creature_name}: {amount}")

                            processed_obj[sub_key] = "\n".join(creature_lines) if creature_lines else ""
                        # Special formatting for backpack artifacts
                        elif sub_key == "backpack" and sub_value:
                            backpack_names = []

                            for artifact_data in sub_value:
                                if isinstance(artifact_data, list) and len(artifact_data) >= 2:
                                    artifact_id = artifact_data[0]

                                    # Skip empty artifacts (ID 65535)
                                    if artifact_id != 65535 and str(artifact_id) != "<ID.Empty_2_Bytes: 65535>":
                                        artifact_name = ""

                                        # Extract artifact name from enum
                                        if hasattr(artifact_id, "name"):
                                            artifact_name = artifact_id.name.replace("_", " ")
                                        elif ":" in str(artifact_id) and "." in str(artifact_id):
                                            # Handle format like "<ID.Pendant_of_Reflection: 123>"
                                            artifact_name = (
                                                str(artifact_id).split(".")[1].split(":")[0].replace("_", " ")
                                            )
                                        else:
                                            artifact_name = str(artifact_id).replace("_", " ")

                                        if artifact_name:
                                            backpack_names.append(artifact_name)

                            processed_obj["backpack"] = "\n".join(backpack_names) if backpack_names else ""
                        # Special formatting for spells
                        elif sub_key == "spells" and sub_value:
                            processed_obj["spells"] = format.format_enum_list(
                                sub_value, spells.ID, format.SPELL_SPECIAL_CASES
                            )
                        else:
                            # Convert other lists to strings
                            processed_obj[sub_key] = str(sub_value) if sub_value else ""
                    else:
                        # Rename "id" to "hero_id" to avoid conflicts with object id
                        if sub_key == "id":
                            processed_obj["hero_id"] = sub_value
                        else:
                            processed_obj[sub_key] = sub_value

                            # Add Portrait column after portrait_id
                            if sub_key == "portrait_id":
                                # Pass the entire object to get_portrait_path so it can access default_name
                                processed_obj["portrait"] = _get_portrait_path(sub_value, processed_obj)

                            # Convert gender numeric values to readable text
                            if sub_key == "gender":
                                if sub_value == 0:
                                    processed_obj["gender"] = "Male"
                                elif sub_value == 1:
                                    processed_obj["gender"] = "Female"
                                elif sub_value == 255:
                                    processed_obj["gender"] = "Default"
                                else:
                                    processed_obj["gender"] = str(sub_value)  # Fallback for unknown values
            else:
                # Keep non-hero_data fields as-is
                processed_obj[key] = value

        processed_objects.append(processed_obj)

    return processed_objects


def _get_portrait_path(portrait_id, hero_data=None):
    # Handle default portrait case
    if portrait_id is None or portrait_id == 255:  # Default portrait
        if hero_data and "default_name" in hero_data:
            default_name = hero_data["default_name"]

            if default_name:
                # Use the default name to find the portrait
                filename = f"{default_name}.bmp"

                # Get the path to the portrait file
                portrait = os.path.join("core/portraits", filename)

                # Only return path if portrait exists
                if os.path.exists(portrait):
                    return portrait

        return ""

    try:
        # Get the portrait enum name
        portrait_enum = heroes.Portrait(portrait_id)
        portrait_name = portrait_enum.name

        # Handle special cases
        if portrait_name.endswith("_campaign"):
            # Remove "_campaign" and add " (campaign)"
            base_name = portrait_name[:-9]  # Remove "_campaign"
            filename = f"{base_name} (campaign).bmp"
        elif portrait_name.startswith("Tarnum_"):
            # Convert Tarnum_Barbarian to Tarnum (Barbarian)
            class_name = portrait_name[7:]  # Remove "Tarnum_"
            filename = f"Tarnum ({class_name}).bmp"
        else:
            # Standard conversion: replace underscores with spaces
            filename = portrait_name.replace("_", " ") + ".bmp"

        # Get the full path to the portrait file
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        portrait = os.path.join(script_dir, "portraits", filename)

        # Only return path if file exists
        if os.path.exists(portrait):
            return portrait
        else:
            return ""
    except (ValueError, AttributeError):
        # Invalid portrait ID or other error
        return ""
