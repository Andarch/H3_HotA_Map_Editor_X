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
                case 1: export_sections(map_key, writer, all_sections)
                case 2: export_sections(map_key, writer, hero_sections, use_hero_data=True)
                case 3: export_sections(map_key, writer, terrain_sections)
                case 4: export_categorized_objects(map_key, writer)

        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def export_sections(map_key: dict, writer, sections, use_hero_data=False):
        """Unified function for exporting sequential sections to Excel"""
        # Get the appropriate data source
        data_source = get_hero_data(map_key) if use_hero_data else map_key

        # Prepare sections data for export
        sections_data = {}

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

                sections_data[section_name] = {
                    'data': df,
                    'section_key': section,
                    'pre_processed': False
                }
            else:
                # Handle regular sections
                xprint(text=f"Exporting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
                time.sleep(Sleep.SHORT.value)

                # Create DataFrame based on section data
                df = create_section_dataframe(section_data, section, section_name)

                sections_data[section_name] = {
                    'data': df,
                    'section_key': section,
                    'pre_processed': False
                }

        # Export all sections using unified function
        export_sections_to_excel(writer, sections_data, use_progress=True, is_final_export=True)

    def export_categorized_objects(map_key: dict, writer):
        """Export function for categorized object data to multiple sheets"""
        object_data = map_key["object_data"]
        total_items = len(object_data)

        # Progress callback for categorization
        def progress_callback(current, total):
            xprint(text=f"Exporting... {Color.CYAN.value}Object Data {current}/{total}{Color.RESET.value}", overwrite=1)

        xprint(text=f"Exporting... {Color.CYAN.value}Object Data 0/{total_items}{Color.RESET.value}", overwrite=1)

        # Categorize objects using utility function
        categorized_objects = categorize_objects(object_data, progress_callback)

        # Prepare categorized data for export
        sections_data = {}

        for category, objects_list in categorized_objects.items():
            if objects_list:
                # Sort objects by ID first, then by sub_id
                objects_list.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

                # Special handling for Heroes sheet - flatten nested hero data
                if category == "Heroes":
                    objects_list = flatten_hero_data(objects_list)

                # Create DataFrame with specialized processing for object data
                df = prepare_dataframe(objects_list, remove_bytes_columns=True, format_columns=True)

                sections_data[category] = {
                    'data': df,
                    'section_key': "object_category",
                    'pre_processed': True,
                    'add_row_numbers': True
                }
            else:
                sections_data[category] = {'data': None}

        # Export all categories using unified function
        export_sections_to_excel(writer, sections_data, use_progress=True, is_final_export=True)

    def get_export_type() -> int:
        input = xprint(menu=Menu.EXCEL.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    return main(map_key)
