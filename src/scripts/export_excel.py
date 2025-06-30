import pandas as pd
from ..common import *
from ..menus import *
from .excel_utils import *
from .data_utils import *


def export_excel(map_key: dict) -> bool:
    filename = map_key["filename"]
    if filename.endswith(".h3m"): filename = filename[:-4]

    export_type = xprint(menu=Menu.EXCEL.value)
    if export_type == KB.ESC.value: return False

    # Currently only object data export is supported (option 4)
    # Keep menu structure for future extensibility
    if export_type != 4:
        xprint(type=Text.ERROR, text="Only object data export is currently supported.")
        return False

    # Append export type suffix to filename
    filename += "_objects"
    if not filename.endswith(".xlsx"): filename += ".xlsx"

    # Check if Excel file is already open
    if not is_file_writable(filename):
        xprint(type=Text.ERROR, text="Excel file currently open.")
        return False

    xprint()
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
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

        # Export all sections using unified function
        export_dataframes(writer, sections_data, is_final_export=True)

    xprint(type=Text.SPECIAL, text=DONE)
    return True
