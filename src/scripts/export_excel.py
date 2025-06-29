from copy import deepcopy
import os
import pandas as pd
import data.objects as objects
from ..common import *
from ..menus import *

def export_excel(map_key: dict) -> bool:
    def main(map_key: dict) -> bool:
        all_sections = ["general", "player_specs", "rumors", "hero_data", "terrain", "object_defs", "object_data", "events"]
        hero_sections = ["player_specs", "custom_heroes", "hero_data", "object_data"]
        terrain_sections = ["terrain"]

        filename = map_key["filename"]
        if filename.endswith(".h3m"): filename = filename[:-4]

        export_type = get_export_type()
        if not export_type: return False

        # Append export type suffix to filename
        suffix_map = {1: "_all", 2: "_heros", 3: "_terrain", 4: "_objects"}
        filename += suffix_map[export_type]

        if not filename.endswith(".xlsx"): filename += ".xlsx"

        # Check if Excel file is already open
        if not is_file_writable(filename):
            xprint(type=Text.ERROR, text="Excel file currently open.")
            return False

        xprint()
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            match export_type:
                case 1: export_data(map_key, writer, all_sections)
                case 2: export_data(map_key, writer, hero_sections, use_hero_data=True)
                case 3: export_data(map_key, writer, terrain_sections)
                case 4: export_object_data(map_key, writer)

        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def export_data(map_key: dict, writer, sections, use_hero_data=False):
        # Get the appropriate data source
        data_source = get_hero_data(map_key) if use_hero_data else map_key

        for section_idx, section in enumerate(sections):
            section_name = section.replace("_", " ").title()
            section_data = data_source[section]

            # Handle progress tracking for large sections
            if section in ["terrain", "object_data", "events"] and not use_hero_data:
                total_items = len(section_data)
                if section in ["terrain", "object_data"]:
                    update_interval = 10000
                elif section == "events":
                    update_interval = 1

                xprint(text=f"Exporting... {Color.CYAN.value}{section_name} 0/{total_items}{Color.RESET.value}", overwrite=1)
                processed_items = []
                for i, item in enumerate(section_data, 1):
                    processed_items.append(item)
                    if i % update_interval == 0 or i == total_items:
                        xprint(text=f"Exporting... {Color.CYAN.value}{section_name} {i}/{total_items}{Color.RESET.value}", overwrite=1)

                # Create DataFrame based on processed items
                df = pd.DataFrame(processed_items)
                if section in ["terrain", "object_data"]:
                    xprint(text="Formatting...")
            else:
                # Handle regular sections
                xprint(text=f"Exporting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
                time.sleep(Sleep.SHORT.value)

                # Create DataFrame based on section data
                if isinstance(section_data, list) and section_data:
                    df = pd.DataFrame(section_data)
                elif section == "general":
                    df = create_general_dataframe(section_data)
                else:
                    df = pd.DataFrame([{section: "No data"}])

            # Common processing for all sections
            df = sanitize_dataframe(df)

            # Clean up column headers: replace underscores with spaces and apply title case
            # (except for the general section which has a custom structure)
            if section != "general":
                df.columns = [str(col).replace('_', ' ').title().replace(' Id', ' ID') for col in df.columns]

            # Insert row numbering column for all sections except general
            if section != "general":
                if len(df) > 0 and not (len(df) == 1 and section in df.columns):
                    # Add row numbers for actual data
                    df.insert(0, "#", range(1, len(df) + 1))
                else:
                    # Add empty numbering column for "No data" cases
                    df.insert(0, "#", "")

            df.to_excel(writer, sheet_name=section_name, index=False)
            worksheet = writer.sheets[section_name]
            auto_fit_columns(worksheet)

            # Progress cleanup for large sections
            if section in ["terrain", "object_data"] and not use_hero_data:
                xprint(text="", overwrite=2)

            # Show "Writing Excel file to disk..." message for the last section
            if section_idx == len(sections) - 1:
                xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)

    def export_object_data(map_key: dict, writer):
        """Special export function for object data that categorizes objects into multiple sheets"""
        object_data = map_key["object_data"]
        total_items = len(object_data)

        # Define object categories
        categories = {
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

        # Initialize category lists
        categorized_objects = {category: [] for category in categories.keys()}

        xprint(text=f"Exporting... {Color.CYAN.value}Object Data 0/{total_items}{Color.RESET.value}", overwrite=1)

        # Categorize objects
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

            if i % 10000 == 0 or i == total_items:
                xprint(text=f"Exporting... {Color.CYAN.value}Object Data {i}/{total_items}{Color.RESET.value}", overwrite=1)

        xprint(text="Formatting...")

        # Export each category to its own sheet
        for category, objects_list in categorized_objects.items():
            if objects_list:
                # Sort objects by ID first, then by sub_id
                objects_list.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

                # Special handling for Heroes sheet - flatten nested hero data
                if category == "Heroes":
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
                    objects_list = flattened_objects

                df = pd.DataFrame(objects_list)
                df = sanitize_dataframe(df)

                # Remove columns ending with "_bytes"
                df = df.loc[:, ~df.columns.str.endswith('_bytes')]

                # Clean up column headers: replace underscores with spaces and apply title case
                df.columns = [str(col).replace('_', ' ').title().replace(' Id', ' ID') for col in df.columns]

                df.insert(0, "#", range(1, len(df) + 1))
                df.to_excel(writer, sheet_name=category, index=False)
                worksheet = writer.sheets[category]
                auto_fit_columns(worksheet)
            else:
                # Create empty sheet if no objects in this category
                df = pd.DataFrame([{category: "No data"}])
                df.insert(0, "#", "")
                df.to_excel(writer, sheet_name=category, index=False)
                worksheet = writer.sheets[category]
                auto_fit_columns(worksheet)

        # Clean up progress display
        xprint(text="", overwrite=2)
        xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)

    def flatten_dict(d, parent_key="", sep="_"):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict): items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, bytes): items.append((new_key, v.decode("latin-1")))
            else: items.append((new_key, str(v) if isinstance(v, (list, tuple)) else v))
        return dict(items)

    def create_general_dataframe(general_data):
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

    def get_export_type() -> int:
        input = xprint(menu=Menu.EXCEL.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    def get_hero_data(map_key: dict) -> dict:
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

    def sanitize_dataframe(df):
        import re
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

    def is_file_writable(filepath: str) -> bool:
        """Check if a file can be written to (not currently open in another application)"""
        try:
            # Try to open the file in write mode
            if os.path.exists(filepath):
                with open(filepath, 'r+b') as f:
                    pass
            return True
        except (IOError, OSError, PermissionError):
            return False

    return main(map_key)
