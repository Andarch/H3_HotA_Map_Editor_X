import data.objects as objects
from .flatten_hero_data import flatten_hero_data
from .flatten_town_data import flatten_town_data
from .flatten_town_event_data import flatten_town_event_data


# Define columns to remove per category
COLUMNS_TO_REMOVE = {
    "Heroes": ["def_id", "id", "sub_id", "type", "subtype", "owner", "hero_id", "default_name", "has_custom_name", "custom_name", "formation",
               "has_portrait", "portrait_id", "patrol", "has_biography",
               # Remove individual artifact slot columns since we're creating combined "artifacts" and "backpack" columns
               "head", "shoulders", "neck", "right_hand", "left_hand", "torso", "right_ring", "left_ring", "feet",
               "misc1", "misc2", "misc3", "misc4", "misc5", "ballista", "ammo_cart", "first_aid_tent", "catapult", "spell_book",
               # Remove any existing backpack-related columns that might conflict
               "artifacts_backpack", "artifact_backpack"],
    "Towns": ["def_id", "id", "sub_id", "type", "owner", "garrison_formation", "has_custom_buildings", "buildings_built", "buildings_disabled",
              "spells_must_appear", "spells_cant_appear", "buildings_special", "events"],
    "Town Events": ["hota_town_event_1", "hota_town_event_2"],
}


def process_objects(object_data) -> dict:
    # Categorize objects and apply all necessary data transformations.
    processed_objects = {category: [] for category in objects.CATEGORIES.keys()}

    # Add Town Events category - will be populated separately
    processed_objects["Town Events"] = []

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
        if category == "Town Events":
            continue  # Handle this separately after processing towns

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
                cleaned_obj_raw = {k: v for k, v in obj.items()
                                   if not k.endswith('_bytes') and k not in columns_to_remove}

                # Clean empty list representations
                cleaned_obj = {}
                for key, value in cleaned_obj_raw.items():
                    if isinstance(value, str) and value == "[]":
                        cleaned_obj[key] = ""
                    else:
                        cleaned_obj[key] = value
                cleaned_objects.append(cleaned_obj)

            processed_objects[category] = cleaned_objects

    # Step 3: Extract and process town events
    town_events = []
    for obj in object_data:
        if obj["id"] in [objects.ID.Town, objects.ID.Random_Town] and "events" in obj and obj["events"]:
            for event in obj["events"]:
                # Create a flattened event object with town context
                flattened_event = flatten_town_event_data(event, obj)
                town_events.append(flattened_event)

    processed_objects["Town Events"] = town_events

    # Reorder to place Town Events right after Towns
    ordered_objects = {}
    for key in processed_objects.keys():
        if key == "Towns":
            ordered_objects[key] = processed_objects[key]
            ordered_objects["Town Events"] = processed_objects["Town Events"]
        elif key != "Town Events":
            ordered_objects[key] = processed_objects[key]

    return ordered_objects
