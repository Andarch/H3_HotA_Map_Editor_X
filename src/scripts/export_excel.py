import pandas as pd
from ..common import *
from ..menus import *
from .excel_utils import *
from .data_utils import *


def export_excel(map_key: dict) -> bool:
    all_sections = ["general", "player_specs", "rumors", "hero_data", "terrain", "object_defs", "object_data", "events"]
    hero_sections = ["player_specs", "custom_heroes", "hero_data", "object_data"]
    terrain_sections = ["terrain"]

    filename = map_key["filename"]
    if filename.endswith(".h3m"): filename = filename[:-4]

    export_type = xprint(menu=Menu.EXCEL.value)
    if export_type == KB.ESC.value: return False

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
        # Determine export parameters based on type
        if export_type == 1:
            sections = all_sections
            use_hero_data = False
            categorize_objects = False
        elif export_type == 2:
            sections = hero_sections
            use_hero_data = True
            categorize_objects = False
        elif export_type == 3:
            sections = terrain_sections
            use_hero_data = False
            categorize_objects = False
        elif export_type == 4:
            sections = None
            use_hero_data = False
            categorize_objects = True

        # Handle data processing and export
        if categorize_objects:
            # Handle categorized objects export
            object_data = map_key["object_data"]
            xprint(text=f"Exporting... {Color.CYAN.value}Object Data{Color.RESET.value}", overwrite=1)

            # Categorize objects using utility function
            categorized_objects = categorize_objects(object_data)
            sections_data = {}

            for category, objects_list in categorized_objects.items():
                if objects_list:
                    # Sort objects by ID first, then by sub_id
                    objects_list.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

                    # Special handling for Heroes sheet - flatten nested hero data
                    if category == "Heroes":
                        objects_list = flatten_obj_hero_data(objects_list)

                    # Create DataFrame with specialized processing for object data
                    df = pd.DataFrame(objects_list)
                    # Remove byte columns
                    df = df.loc[:, ~df.columns.str.endswith('_bytes')]

                    sections_data[category] = {
                        'data': df,
                        'section_key': "object_category",
                        'add_row_numbers': True
                    }
                else:
                    sections_data[category] = {'data': None}
        else:
            # Handle regular sections export
            data_source = get_all_hero_data(map_key) if use_hero_data else map_key
            sections_data = {}

            for section in sections:
                section_name = section.replace("_", " ").title()
                section_data = data_source[section]

                # Handle all sections uniformly
                xprint(text=f"Exporting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
                time.sleep(Sleep.SHORT.value)

                # Create DataFrame based on section data
                df = create_dataframe(section_data, section, section_name)

                sections_data[section_name] = {
                    'data': df,
                    'section_key': section
                }

        # Export all sections using unified function
        export_dataframes(writer, sections_data, is_final_export=True)

    xprint(type=Text.SPECIAL, text=DONE)
    return True
