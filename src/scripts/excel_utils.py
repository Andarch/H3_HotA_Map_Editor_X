"""
Excel export utility functions for Heroes 3 map editor.
Contains common functionality for DataFrame processing and worksheet formatting.
"""

import re
import pandas as pd


def format_column_name(col):
    """Format column name: replace underscores, apply title case, fix 'Id' -> 'ID'"""
    formatted = str(col).replace('_', ' ').title()
    formatted = formatted.replace('Id', 'ID')
    return formatted


def sanitize_dataframe(df):
    """Clean DataFrame values to prevent Excel issues with illegal characters and formulas"""
    illegal_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

    def clean_value(value):
        if isinstance(value, str):
            cleaned = illegal_chars.sub("", value)
            if cleaned and cleaned[0] in ("=", "+", "@"):
                cleaned = "'" + cleaned
            return cleaned
        elif isinstance(value, bytes):
            try:
                decoded = value.decode("latin-1", errors="ignore")
                cleaned = illegal_chars.sub("", decoded)
                if cleaned and cleaned[0] in ("=", "+", "@"):
                    cleaned = "'" + cleaned
                return cleaned
            except:
                return str(value)
        else:
            return value

    for col in df.columns:
        df[col] = df[col].apply(clean_value)
    return df


def auto_fit_columns(worksheet):
    """Auto-fit column widths based on content length"""
    for column in worksheet.columns:
        max_length = 0
        header_length = 0
        column_letter = column[0].column_letter
        for i, cell in enumerate(column):
            try:
                cell_length = len(str(cell.value))
                if i == 0:
                    header_length = cell_length
                if cell_length > max_length:
                    max_length = cell_length
            except:
                pass
        if header_length == max_length:
            adjusted_width = header_length + 6
        else:
            adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width


def prepare_dataframe(data, remove_bytes_columns=True, format_columns=True):
    """Create, sanitize, and format a DataFrame with common processing steps"""
    df = pd.DataFrame(data)
    df = sanitize_dataframe(df)

    if remove_bytes_columns:
        df = df.loc[:, ~df.columns.str.endswith('_bytes')]

    if format_columns:
        df.columns = [format_column_name(col) for col in df.columns]

    return df


def create_worksheet(writer, df, sheet_name, add_row_numbers=True):
    """Create worksheet with formatted data, row numbers, and auto-fit columns"""
    if add_row_numbers and len(df) > 0:
        # Only add row numbers if it's not a "No data" case
        if not (len(df) == 1 and any(col.lower() in str(df.iloc[0]).lower() for col in ["no data"])):
            df.insert(0, "#", range(1, len(df) + 1))
        else:
            df.insert(0, "#", "")

    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    auto_fit_columns(worksheet)
    return worksheet


def create_empty_worksheet(writer, sheet_name, message="No data"):
    """Create an empty worksheet with a message"""
    df = pd.DataFrame([{sheet_name: message}])
    df.insert(0, "#", "")
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    auto_fit_columns(worksheet)
    return worksheet


def flatten_hero_data(objects_list):
    """
    Flatten nested hero data for Excel export.

    This function processes objects with hero_data and flattens the nested dictionaries
    into a flat structure suitable for Excel export, with special handling for:
    - Primary skills and artifacts (nested dicts)
    - Secondary skills (list of dicts formatted as text)
    - Hero ID renaming to avoid conflicts

    Args:
        objects_list: List of object dictionaries that may contain hero_data

    Returns:
        List of flattened object dictionaries
    """
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


def get_object_categories():
    """
    Get the predefined object categories for export organization.

    Returns:
        Dictionary mapping category names to sets of object IDs
    """
    import data.objects as objects

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


def categorize_objects(object_data, progress_callback=None):
    """
    Categorize objects into predefined categories for export.

    Args:
        object_data: List of object dictionaries to categorize
        progress_callback: Optional function to call for progress updates

    Returns:
        Dictionary mapping category names to lists of objects
    """
    import data.objects as objects

    categories = get_object_categories()
    categorized_objects = {category: [] for category in categories.keys()}
    total_items = len(object_data)

    for i, obj in enumerate(object_data, 1):
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

        # Call progress callback if provided
        if progress_callback and (i % 10000 == 0 or i == total_items):
            progress_callback(i, total_items)

    return categorized_objects


def flatten_dict(d, parent_key="", sep="_"):
    """
    Recursively flatten a nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nested structure
        sep: Separator to use between keys

    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, bytes):
            items.append((new_key, v.decode("latin-1")))
        else:
            items.append((new_key, str(v) if isinstance(v, (list, tuple)) else v))
    return dict(items)


def create_general_dataframe(general_data):
    """
    Create a structured DataFrame for general map data.

    Args:
        general_data: Dictionary containing general map information

    Returns:
        pandas.DataFrame with Category, Key, Value columns
    """
    rows = []
    categories = ["map_specs", "teams", "conditions", "start_heroes", "ban_flags"]

    for category in categories:
        if category in general_data:
            if category == "map_specs" and "filename" in general_data:
                rows.append({
                    "Category": "map_specs",
                    "Key": "filename",
                    "Value": general_data["filename"]
                })

            category_data = general_data[category]
            if isinstance(category_data, dict):
                flattened = flatten_dict(category_data)
                for key, value in flattened.items():
                    rows.append({
                        "Category": category,
                        "Key": key,
                        "Value": value
                    })
            else:
                rows.append({
                    "Category": category,
                    "Key": category,
                    "Value": category_data
                })

    return pd.DataFrame(rows)


def is_file_writable(filepath: str) -> bool:
    """
    Check if a file can be written to (not currently open in another application).

    Args:
        filepath: Path to the file to check

    Returns:
        True if file can be written to, False otherwise
    """
    import os

    try:
        # Try to open the file in write mode
        if os.path.exists(filepath):
            with open(filepath, 'r+b') as f:
                pass
        return True
    except (IOError, OSError, PermissionError):
        return False


def get_hero_data(map_key: dict) -> dict:
    """
    Extract and filter hero-related data from map data.

    This function processes the map data to extract only hero-relevant information,
    filtering out empty sections and removing unnecessary fields for cleaner exports.

    Args:
        map_key: Dictionary containing the full map data

    Returns:
        Dictionary with filtered hero data containing player_specs, custom_heroes,
        hero_data, and object_data (heroes only)
    """
    from copy import deepcopy
    import data.objects as objects

    player_specs = deepcopy(map_key['player_specs'])
    player_specs[:] = [player for player in player_specs if len(player["available_heroes"]) > 0]
    for player in player_specs:
        del player["ai_behavior"]
        del player["alignments_customized"]
        del player["alignments_allowed"]
        del player["alignment_is_random"]
        del player["has_main_town"]
        if "generate_hero" in player: del player["generate_hero"]
        if "town_type" in player: del player["town_type"]
        if "town_coords" in player: del player["town_coords"]
        if "garbage_byte" in player: del player["garbage_byte"]
        if "placeholder_heroes" in player: del player["placeholder_heroes"]

    custom_heroes = deepcopy(map_key["start_heroes"]["custom_heroes"])
    hero_data = deepcopy(map_key["hero_data"])
    hero_data[:] = [hero for hero in hero_data if len(hero) > 3]
    object_data = deepcopy(map_key["object_data"])
    object_data[:] = [obj for obj in object_data if obj["id"] in (objects.ID.Hero, objects.ID.Prison)]

    final_hero_data = {
        "player_specs": player_specs,
        "custom_heroes": custom_heroes,
        "hero_data": hero_data,
        "object_data": object_data
    }
    return final_hero_data


def process_section_with_progress(section_data, section_name, update_interval=10000):
    """
    Process large sections with progress tracking.

    Args:
        section_data: List of items to process
        section_name: Name of the section for progress display
        update_interval: How often to update progress display

    Returns:
        List of processed items
    """
    from ..common import Color, xprint

    total_items = len(section_data)
    xprint(text=f"Exporting... {Color.CYAN.value}{section_name} 0/{total_items}{Color.RESET.value}", overwrite=1)

    processed_items = []
    for i, item in enumerate(section_data, 1):
        processed_items.append(item)
        if i % update_interval == 0 or i == total_items:
            xprint(text=f"Exporting... {Color.CYAN.value}{section_name} {i}/{total_items}{Color.RESET.value}", overwrite=1)

    return processed_items


def create_section_dataframe(section_data, section, section_name):
    """
    Create a DataFrame for a section with appropriate handling for different data types.

    Args:
        section_data: The data for this section
        section: The section identifier
        section_name: The formatted section name

    Returns:
        pandas.DataFrame
    """
    if isinstance(section_data, list) and section_data:
        return pd.DataFrame(section_data)
    elif section == "general":
        return create_general_dataframe(section_data)
    else:
        return pd.DataFrame([{section: "No data"}])


def export_section_to_worksheet(writer, df, section, section_name, add_row_numbers=True, pre_processed=False):
    """
    Complete processing and export of a section to Excel worksheet.

    Args:
        writer: Excel writer object
        df: DataFrame to export
        section: Section identifier
        section_name: Formatted section name
        add_row_numbers: Whether to add row numbers
        pre_processed: If True, skip sanitization and column formatting (for pre-processed DataFrames)

    Returns:
        The created worksheet
    """
    if not pre_processed:
        # Sanitize the dataframe
        df = sanitize_dataframe(df)

        # Format column headers (except for general section)
        if section != "general":
            df.columns = [format_column_name(col) for col in df.columns]

    # Add row numbers for non-general sections
    if section != "general" and add_row_numbers:
        if len(df) > 0 and not (len(df) == 1 and section in df.columns):
            # Add row numbers for actual data
            df.insert(0, "#", range(1, len(df) + 1))
        else:
            # Add empty numbering column for "No data" cases
            df.insert(0, "#", "")

    # Export to Excel and auto-fit columns
    df.to_excel(writer, sheet_name=section_name, index=False)
    worksheet = writer.sheets[section_name]
    auto_fit_columns(worksheet)

    return worksheet
