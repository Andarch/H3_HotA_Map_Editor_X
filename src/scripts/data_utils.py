import data.objects as objects


def categorize_objects(object_data) -> dict:
    categories = get_obj_categories()
    categorized_objects = {category: [] for category in categories.keys()}

    for obj in object_data:
        categorized = False

        # Special handling for Border_Gate based on sub_id
        if obj["id"] == objects.ID.Border_Gate:
            if obj["sub_id"] == 1000:  # Quest Gate
                categorized_objects["Quest Objects"].append(obj)
            elif obj["sub_id"] == 1001:  # Grave - reward giving object
                categorized_objects["Treasure"].append(obj)
            else:  # Regular Border Gate
                categorized_objects["Border Objects"].append(obj)
            categorized = True
        else:
            # Check each category
            for category, object_ids in categories.items():
                if obj["id"] in object_ids:
                    categorized_objects[category].append(obj)
                    categorized = True
                    break

        # If object doesn't fit any category, add to Simple Objects
        if not categorized:
            categorized_objects["Simple Objects"].append(obj)

    return categorized_objects


def get_obj_categories() -> dict:
    return {
        "Heroes": {
            objects.ID.Hero, objects.ID.Prison, objects.ID.Random_Hero, objects.ID.Hero_Placeholder
        },
        "Towns": {
            objects.ID.Town, objects.ID.Random_Town
        },
        "Monsters": {
            objects.ID.Monster, objects.ID.Random_Monster, objects.ID.Random_Monster_1,
            objects.ID.Random_Monster_2, objects.ID.Random_Monster_3, objects.ID.Random_Monster_4,
            objects.ID.Random_Monster_5, objects.ID.Random_Monster_6, objects.ID.Random_Monster_7
        },
        "Spells": {
            objects.ID.Shrine_of_Magic_Incantation, objects.ID.Shrine_of_Magic_Gesture,
            objects.ID.Shrine_of_Magic_Thought, objects.ID.Pyramid, objects.ID.Spell_Scroll
        },
        "Artifacts": {
            objects.ID.Artifact, objects.ID.Random_Artifact, objects.ID.Random_Treasure_Artifact,
            objects.ID.Random_Minor_Artifact, objects.ID.Random_Major_Artifact, objects.ID.Random_Relic
        },
        "Resources": {
            objects.ID.Resource, objects.ID.Random_Resource
        },
        "Treasure": {
            objects.ID.Treasure_Chest, objects.ID.Sea_Chest, objects.ID.Flotsam, objects.ID.Campfire,
            objects.ID.Shipwreck_Survivor, objects.ID.HotA_Collectible
        },
        "Other Pickups": {
            objects.ID.Scholar, objects.ID.Ocean_Bottle, objects.ID.Grail
        },
        "Creature Banks": {
            objects.ID.Creature_Bank, objects.ID.Derelict_Ship, objects.ID.Dragon_Utopia,
            objects.ID.Crypt, objects.ID.Shipwreck
        },
        "Garrisons": {
            objects.ID.Garrison, objects.ID.Garrison_Vertical
        },
        "Seers Huts": {
            objects.ID.Seers_Hut
        },
        "Quest Objects": {
            objects.ID.Quest_Guard
        },
        "Event Pickups": {
            objects.ID.Event, objects.ID.Pandoras_Box
        },
        "Border Objects": {
            objects.ID.Border_Guard, objects.ID.Keymasters_Tent
        },
        "Dwellings": {
            objects.ID.Creature_Generator_1, objects.ID.Creature_Generator_4, objects.ID.Random_Dwelling,
            objects.ID.Random_Dwelling_Leveled, objects.ID.Random_Dwelling_Faction
        },
        "Mines & Warehouses": {
            objects.ID.Mine, objects.ID.HotA_Warehouse, objects.ID.Abandoned_Mine
        },
        "Interactive": {
            objects.ID.University, objects.ID.Witch_Hut, objects.ID.Black_Market,
            objects.ID.HotA_Visitable_1, objects.ID.HotA_Visitable_2
        },
        "Simple Objects": {
            objects.ID.Tree_of_Knowledge, objects.ID.Lean_To, objects.ID.Wagon, objects.ID.Warriors_Tomb,
            objects.ID.Lighthouse, objects.ID.Shipyard
        },
        "Decor": objects.DECOR_OBJECTS
    }


def flatten_obj_hero_data(objects_list) -> list:
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


def process_objects(object_data) -> dict:
    # Categorize objects and apply all necessary data transformations.
    categories = get_obj_categories()
    processed_objects = {category: [] for category in categories.keys()}

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
            for category, object_ids in categories.items():
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
                objects_list = flatten_obj_hero_data(objects_list)
            # elif category == "Towns":
            #     objects_list = flatten_obj_town_data(objects_list)  # future

            # Remove unwanted columns (universal + category-specific)
            cleaned_objects = []
            for obj in objects_list:
                # For now, just remove _bytes columns (universal)
                # Future: add category-specific column removal here
                cleaned_obj = {k: v for k, v in obj.items() if not k.endswith('_bytes')}
                cleaned_objects.append(cleaned_obj)

            processed_objects[category] = cleaned_objects

    return processed_objects
