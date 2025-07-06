import data.objects as objects


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
                # elif category == "Towns":
                #     objects_list = flatten_town_data(objects_list)  # future

                # Remove unwanted columns (universal + category-specific)
                cleaned_objects = []
                for obj in objects_list:
                    # For now, just remove _bytes columns (universal)
                    # Future: add category-specific column removal here
                    cleaned_obj = {k: v for k, v in obj.items() if not k.endswith('_bytes')}
                    cleaned_objects.append(cleaned_obj)

                processed_objects[category] = cleaned_objects

        return processed_objects


    def flatten_hero_data(objects_list) -> list:
        flattened_objects = []

        for obj in objects_list:
            flattened_obj = {}

            for key, value in obj.items():
                if key == "hero_data" and isinstance(value, dict):
                    # Flatten hero data dictionaries using just the sub-key names
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, dict):
                            # Flatten nested dictionaries (like primary_skills, artifacts_equipped)
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
                            else:
                                # Convert other lists to strings
                                flattened_obj[sub_key] = str(sub_value) if sub_value else ""
                        else:
                            # Rename "id" to "hero_id" to avoid conflicts with object id
                            if sub_key == "id":
                                flattened_obj["hero_id"] = sub_value
                            else:
                                flattened_obj[sub_key] = sub_value
                else:
                    # Keep non-hero_data fields as-is
                    flattened_obj[key] = value

            flattened_objects.append(flattened_obj)

        return flattened_objects

    return main()
