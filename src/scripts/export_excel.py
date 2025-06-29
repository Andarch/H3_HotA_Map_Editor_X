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
                # Determine update interval based on section type
                update_interval = 1 if section == "events" else 10000

                # Process with progress tracking
                processed_items = process_section_with_progress(section_data, section_name, update_interval)
                df = pd.DataFrame(processed_items)

                if section in ["terrain", "object_data"]:
                    xprint(text="Formatting...")
            else:
                # Handle regular sections
                xprint(text=f"Exporting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
                time.sleep(Sleep.SHORT.value)

                # Create DataFrame based on section data
                df = create_section_dataframe(section_data, section, section_name)

            # Export section to worksheet using utility function
            export_section_to_worksheet(writer, df, section, section_name)

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

                # Create DataFrame with specialized processing for object data
                df = prepare_dataframe(objects_list, remove_bytes_columns=True, format_columns=True)

                # Export using utility function (pre-processed since prepare_dataframe already formatted columns)
                export_section_to_worksheet(writer, df, "object_category", category, add_row_numbers=True, pre_processed=True)
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

    return main(map_key)
