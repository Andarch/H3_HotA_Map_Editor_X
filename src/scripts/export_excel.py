import os
import re
import pandas as pd
from ..common import *
from ..menus import *
from .data_utils import *


def export_excel(map_key: dict) -> bool:
    # Create Excel filename by replacing .h3m with _objects.xlsx
    filename = map_key["filename"][:-4] + "_objects.xlsx"

    # Check if Excel file is already open
    if not is_file_writable(filename):
        xprint(type=Text.ERROR, text="Excel file currently open.")
        return False

    xprint()

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Handle categorized objects export
        data = map_key["object_data"]
        xprint(text=f"Exporting object data to Excel...", overwrite=1)

        # Categorize objects using utility function
        categorized_objects = categorize_objects(data)
        sections_data = {}

        for category, objects in categorized_objects.items():
            if objects:
                # Sort objects by ID first, then by sub_id
                objects.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

                # Special handling for Heroes sheet - flatten nested hero data
                if category == "Heroes":
                    objects = flatten_obj_hero_data(objects)

                # Remove byte columns from objects before creating DataFrame
                cleaned_objects = []
                for obj in objects:
                    cleaned_obj = {k: v for k, v in obj.items() if not k.endswith('_bytes')}
                    cleaned_objects.append(cleaned_obj)

                df = pd.DataFrame(cleaned_objects)

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


def is_file_writable(filepath: str) -> bool:
    try:
        # Try to open the file in write mode
        if os.path.exists(filepath):
            with open(filepath, 'r+b') as f:
                pass
        return True
    except (IOError, OSError, PermissionError):
        return False


def export_dataframes(writer, sections_data, is_final_export=True) -> None:
    for section_name, section_info in sections_data.items():
        # Handle both simple data and complex section info
        if isinstance(section_info, dict) and 'data' in section_info:
            # Complex section info with additional parameters
            data = section_info['data']
            add_row_numbers = section_info.get('add_row_numbers', True)
            section_key = section_info.get('section_key', 'data')
        else:
            # Simple data
            data = section_info
            add_row_numbers = True
            section_key = section_name.lower().replace(' ', '_')

        if data is not None and (
            (isinstance(data, pd.DataFrame) and not data.empty) or
            (isinstance(data, list) and len(data) > 0) or
            (not isinstance(data, (pd.DataFrame, list)) and data)
        ):
            # Show formatting message for each section
            from ..common import xprint, Color
            xprint(text=f"Formatting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)

            # Process non-empty data
            if isinstance(data, pd.DataFrame):
                df = data
            else:
                df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])

            # Format DataFrame for Excel: sanitize, headers, row numbers
            # Step 1: Sanitize data for Excel compatibility
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

            # Step 2: Format column headers
            # Inline column formatting: replace underscores, title case, fix "Id" -> "ID"
            df.columns = [str(col).replace('_', ' ').title().replace('Id', 'ID') for col in df.columns]

            # Step 3: Add row numbers
            if add_row_numbers:
                if len(df) > 0 and not (len(df) == 1 and section_key in df.columns):
                    # Add row numbers for actual data
                    df.insert(0, "#", range(1, len(df) + 1))
                else:
                    # Add empty numbering column for "No data" cases
                    df.insert(0, "#", "")

            # Export to Excel
            df.to_excel(writer, sheet_name=section_name, index=False)
            worksheet = writer.sheets[section_name]

            # Auto-fit columns
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
        else:
            # Create empty sheet for no data
            df = pd.DataFrame([{section_name: "No data"}])
            df.insert(0, "#", "")
            df.to_excel(writer, sheet_name=section_name, index=False)

    # Show final completion message
    if is_final_export:
        from ..common import xprint, Text
        xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)

