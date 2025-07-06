import data.objects as objects
import data.heroes as heroes
import data.spells as spells
import os


# Define columns to remove per category
COLUMNS_TO_REMOVE = {
    "Heroes": ["def_id", "id", "sub_id", "type", "subtype", "owner", "hero_id", "default_name", "has_custom_name", "custom_name", "formation",
               "has_portrait", "portrait_id", "patrol", "has_biography",
               # Remove individual artifact slot columns since we're creating combined "artifacts" and "backpack" columns
               "head", "shoulders", "neck", "right_hand", "left_hand", "torso", "right_ring", "left_ring", "feet",
               "misc1", "misc2", "misc3", "misc4", "misc5", "ballista", "ammo_cart", "first_aid_tent", "catapult", "spell_book",
               # Remove any existing backpack-related columns that might conflict
               "artifacts_backpack", "artifact_backpack"],
    "Towns": ["def_id", "id", "sub_id", "type", "owner", "garrison_formation", "has_custom_buildings"],
}


def process_objects(object_data) -> dict:
    def main():
        # Categorize objects and apply all necessary data transformations.
        processed_objects = {category: [] for category in objects.CATEGORIES.keys()}

        # Step 1: Categorize objects
        for obj in object_data:
            categorized = False

            # Special handling for Border_Gate based on sub_id
            if obj["id"] == objects.ID.Border_Gate:
                if obj["sub_id"] == 1000:  # Quest Gate
                    processed_objects["Quest Objects"].append(obj)
                elif obj["sub_id"] == 1001:  # Grave - reward giving object
                    processed_objects["Treasure"].append(obj)
                else:  # Regular Border Gate
                    processed_objects["Border Objects"].append(obj)
                categorized = True
            else:
                # Check each category
                for category, object_ids in objects.CATEGORIES.items():
                    if obj["id"] in object_ids:
                        processed_objects[category].append(obj)
                        categorized = True
                        break

            # If object doesn't fit any category, add to Simple Objects
            if not categorized:
                processed_objects["Simple Objects"].append(obj)

        # Step 2: Process each category
        for category, objects_list in processed_objects.items():
            if objects_list:
                # Sort objects by ID first, then by sub_id
                objects_list.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

                # Category-specific transformations
                if category == "Heroes":
                    objects_list = flatten_hero_data(objects_list)
                elif category == "Towns":
                    objects_list = flatten_town_data(objects_list)

                # Remove unwanted columns (universal + category-specific)
                cleaned_objects = []
                columns_to_remove = COLUMNS_TO_REMOVE.get(category, [])
                for obj in objects_list:
                    # Remove _bytes columns (universal) and category-specific columns
                    cleaned_obj = {k: v for k, v in obj.items()
                                   if not k.endswith('_bytes') and k not in columns_to_remove}

                    # Clean empty list representations
                    cleaned_obj = clean_empty_lists(cleaned_obj)
                    cleaned_objects.append(cleaned_obj)

                processed_objects[category] = cleaned_objects

        return processed_objects


    def clean_empty_lists(obj_dict):
        cleaned_obj = {}
        for key, value in obj_dict.items():
            if isinstance(value, str) and value == "[]":
                cleaned_obj[key] = ""
            elif isinstance(value, list) and len(value) == 0:
                cleaned_obj[key] = ""
            else:
                cleaned_obj[key] = value
        return cleaned_obj


    def flatten_hero_data(objects_list) -> list:
        flattened_objects = []

        for obj in objects_list:
            flattened_obj = {}

            for key, value in obj.items():
                if key == "hero_data" and isinstance(value, dict):
                    # Flatten hero data dictionaries using just the sub-key names
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, dict):
                            # Handle artifacts_equipped specially
                            if sub_key == "artifacts_equipped":
                                # Extract artifact names, ignoring empty slots
                                artifact_names = []
                                for slot_name, artifact_data in sub_value.items():
                                    if isinstance(artifact_data, list) and len(artifact_data) >= 2:
                                        artifact_id = artifact_data[0]
                                        # Skip empty artifacts (ID 65535)
                                        if artifact_id != 65535 and str(artifact_id) != "<ID.Empty_2_Bytes: 65535>":
                                            # Extract artifact name from enum
                                            artifact_name = ''
                                            if hasattr(artifact_id, 'name'):
                                                artifact_name = artifact_id.name.replace('_', ' ')
                                            elif ':' in str(artifact_id) and '.' in str(artifact_id):
                                                # Handle format like "<ID.Pendant_of_Reflection: 123>"
                                                artifact_name = str(artifact_id).split('.')[1].split(':')[0].replace('_', ' ')
                                            else:
                                                artifact_name = str(artifact_id).replace('_', ' ')

                                            if artifact_name:
                                                artifact_names.append(artifact_name)

                                flattened_obj["artifacts"] = "\n".join(artifact_names) if artifact_names else ""
                            else:
                                # Flatten other nested dictionaries (like primary_skills)
                                for nested_key, nested_value in sub_value.items():
                                    flattened_obj[nested_key] = nested_value
                        elif isinstance(sub_value, list):
                            # Special formatting for secondary_skills
                            if sub_key == "secondary_skills" and sub_value:
                                skill_lines = []
                                for skill in sub_value:
                                    if isinstance(skill, dict):
                                        level_name = skill.get('level_name', '')
                                        skill_name = skill.get('name', '').replace('_', ' ')
                                        if level_name and skill_name:
                                            skill_lines.append(f"{level_name} {skill_name}")
                                flattened_obj[sub_key] = "\n".join(skill_lines) if skill_lines else ""
                            # Special formatting for creatures
                            elif sub_key == "creatures" and sub_value:
                                creature_lines = []
                                for creature in sub_value:
                                    if isinstance(creature, dict):
                                        creature_id = creature.get('id', '')
                                        amount = creature.get('amount', '')

                                        # Skip creatures with 0 amount
                                        if not amount or amount == 0:
                                            continue

                                        # Extract creature name from ID enum string representation
                                        creature_name = ''
                                        if creature_id:
                                            id_str = str(creature_id)
                                            # Handle different possible enum formats
                                            if ':' in id_str and '.' in id_str:
                                                # Format: "<ID.Arch_Devil: 55>" -> "Arch Devil"
                                                creature_name = id_str.split('.')[1].split(':')[0].replace('_', ' ')
                                            elif hasattr(creature_id, 'name'):
                                                # Direct access to enum name
                                                creature_name = creature_id.name.replace('_', ' ')
                                            else:
                                                # Fallback: use string representation
                                                creature_name = str(creature_id).replace('_', ' ')

                                        if creature_name and amount:
                                            creature_lines.append(f"{creature_name}: {amount}")

                                flattened_obj[sub_key] = "\n".join(creature_lines) if creature_lines else ""
                            # Special formatting for backpack artifacts
                            elif sub_key == "backpack" and sub_value:
                                backpack_names = []
                                for artifact_data in sub_value:
                                    if isinstance(artifact_data, list) and len(artifact_data) >= 2:
                                        artifact_id = artifact_data[0]
                                        # Skip empty artifacts (ID 65535)
                                        if artifact_id != 65535 and str(artifact_id) != "<ID.Empty_2_Bytes: 65535>":
                                            # Extract artifact name from enum
                                            artifact_name = ''
                                            if hasattr(artifact_id, 'name'):
                                                artifact_name = artifact_id.name.replace('_', ' ')
                                            elif ':' in str(artifact_id) and '.' in str(artifact_id):
                                                # Handle format like "<ID.Pendant_of_Reflection: 123>"
                                                artifact_name = str(artifact_id).split('.')[1].split(':')[0].replace('_', ' ')
                                            else:
                                                artifact_name = str(artifact_id).replace('_', ' ')

                                            if artifact_name:
                                                backpack_names.append(artifact_name)

                                flattened_obj["backpack"] = "\n".join(backpack_names) if backpack_names else ""
                            # Special formatting for spells
                            elif sub_key == "spells" and sub_value:
                                flattened_obj["spells"] = format_spell_list(sub_value)
                            else:
                                # Convert other lists to strings
                                flattened_obj[sub_key] = str(sub_value) if sub_value else ""
                        else:
                            # Rename "id" to "hero_id" to avoid conflicts with object id
                            if sub_key == "id":
                                flattened_obj["hero_id"] = sub_value
                            else:
                                flattened_obj[sub_key] = sub_value

                                # Add Portrait column after portrait_id
                                if sub_key == "portrait_id":
                                    # Pass the entire object to get_portrait_path so it can access default_name
                                    flattened_obj["portrait"] = get_portrait_path(sub_value, flattened_obj)

                                # Convert gender numeric values to readable text
                                if sub_key == "gender":
                                    if sub_value == 0:
                                        flattened_obj["gender"] = "Male"
                                    elif sub_value == 1:
                                        flattened_obj["gender"] = "Female"
                                    elif sub_value == 255:
                                        flattened_obj["gender"] = "Default"
                                    else:
                                        flattened_obj["gender"] = str(sub_value)  # Fallback for unknown values
                else:
                    # Keep non-hero_data fields as-is
                    flattened_obj[key] = value

            flattened_objects.append(flattened_obj)

        return flattened_objects


    def flatten_town_data(objects_list) -> list:
        flattened_objects = []

        for obj in objects_list:
            flattened_obj = {}

            for key, value in obj.items():
                # Handle spells_must_appear and spells_cant_appear fields
                if key == "spells_must_appear" and isinstance(value, list):
                    flattened_obj["Spells - Always"] = format_spell_list(value)
                elif key == "spells_cant_appear" and isinstance(value, list):
                    flattened_obj["Spells - Disabled"] = format_spell_list(value)
                # Handle alignment field
                elif key == "alignment" and value is not None:
                    alignment_enum = objects.Town_Alignment(value)
                    flattened_obj[key] = alignment_enum.name.replace('_', ' ')
                else:
                    # Keep other fields as-is
                    flattened_obj[key] = value

            flattened_objects.append(flattened_obj)

        return flattened_objects


    def get_portrait_path(portrait_id, hero_data=None):
        # Handle default portrait case
        if portrait_id is None or portrait_id == 255:  # Default portrait
            if hero_data and "default_name" in hero_data:
                default_name = hero_data["default_name"]
                if default_name:
                    # Use the default name to find the portrait
                    filename = f"{default_name}.bmp"

                    # Get the full path to the portrait file
                    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    portrait_path = os.path.join(script_dir, "portraits", filename)

                    # Only return path if file exists
                    if os.path.exists(portrait_path):
                        return portrait_path
            return ""

        try:
            # Get the portrait enum name
            portrait_enum = heroes.Portrait(portrait_id)
            portrait_name = portrait_enum.name

            # Handle special cases
            if portrait_name.endswith('_campaign'):
                # Remove '_campaign' and add ' (campaign)'
                base_name = portrait_name[:-9]  # Remove '_campaign'
                filename = f"{base_name} (campaign).bmp"
            elif portrait_name.startswith('Tarnum_'):
                # Convert Tarnum_Barbarian to Tarnum (Barbarian)
                class_name = portrait_name[7:]  # Remove 'Tarnum_'
                filename = f"Tarnum ({class_name}).bmp"
            else:
                # Standard conversion: replace underscores with spaces
                filename = portrait_name.replace('_', ' ') + '.bmp'

            # Get the full path to the portrait file
            script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            portrait_path = os.path.join(script_dir, "portraits", filename)

            # Only return path if file exists
            if os.path.exists(portrait_path):
                return portrait_path
            else:
                return ""
        except (ValueError, AttributeError):
            # Invalid portrait ID or other error
            return ""


    def format_spell_list(spell_list):
        """Convert a list of 1s and 0s to readable spell names separated by commas"""
        if not spell_list:
            return ""

        spell_names = []
        # spells is a list of 1s and 0s where index corresponds to spell ID
        for spell_index, has_spell in enumerate(spell_list):
            if has_spell == 1:  # Spell is in the list
                try:
                    spell_enum = spells.ID(spell_index)
                    spell_name = spell_enum.name.replace('_', ' ')

                    # Special case for Titan's Lightning Bolt
                    if spell_name == "Titans Lightning Bolt":
                        spell_name = "Titan's Lightning Bolt"

                    spell_names.append(spell_name)
                except ValueError:
                    # Invalid spell index, skip
                    pass

        return ", ".join(spell_names)


    return main()
