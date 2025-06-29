from copy import deepcopy
import os
import pandas as pd
import data.objects as objects
from ..common import *
from ..menus import *
from .excel_utils import *

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
                df.columns = [format_column_name(col) for col in df.columns]

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

        # Progress callback for categorization
        def progress_callback(current, total):
            xprint(text=f"Exporting... {Color.CYAN.value}Object Data {current}/{total}{Color.RESET.value}", overwrite=1)

        xprint(text=f"Exporting... {Color.CYAN.value}Object Data 0/{total_items}{Color.RESET.value}", overwrite=1)

        # Categorize objects using utility function
        categorized_objects = categorize_objects(object_data, progress_callback)

        xprint(text="Formatting...")

        # Export each category to its own sheet
        for category, objects_list in categorized_objects.items():
            if objects_list:
                # Sort objects by ID first, then by sub_id
                objects_list.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

                # Special handling for Heroes sheet - flatten nested hero data
                if category == "Heroes":
                    objects_list = flatten_hero_data(objects_list)

                df = prepare_dataframe(objects_list, remove_bytes_columns=True, format_columns=True)
                create_worksheet(writer, df, category, add_row_numbers=True)
            else:
                # Create empty sheet if no objects in this category
                create_empty_worksheet(writer, category, "No data")

        # Clean up progress display
        xprint(text="", overwrite=2)
        xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)

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
