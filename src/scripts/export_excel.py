import re
import pandas as pd
from ..common import *
from ..file_io import is_file_writable
from .process_objects import *


def export_excel(map_key: dict) -> bool:
    # Create Excel filename by replacing .h3m with _objects.xlsx
    filename = map_key["filename"][:-4] + "_objects.xlsx"

    # Check if Excel file is already open
    if not is_file_writable(filename):
        return False

    # Show initial export message
    draw_header()
    xprint(type=Text.ACTION, text=f"Exporting object data...")

    # Open Excel writer with openpyxl engine
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Process objects (categorize and clean data)
        processed_objects = process_objects(map_key["object_data"])

        # Compile regex for Excel illegal characters
        illegal_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

        # Write each category to Excel
        for category, objects in processed_objects.items():
            # Create DataFrame
            df = pd.DataFrame(objects) if objects else pd.DataFrame([{"": "No data"}])

            # Sanitize data for Excel compatibility
            for col in df.columns:
                df[col] = df[col].apply(lambda value:
                    illegal_chars.sub("", value) if isinstance(value, str) else
                    illegal_chars.sub("", value.decode("latin-1", errors="ignore")) if isinstance(value, bytes) else
                    value
                ).apply(lambda value:
                    "'" + value if isinstance(value, str) and value and value[0] == "=" else value
                )

            # Format column headers
            df.columns = [str(col).replace('_', ' ').title().replace('Id', 'ID') for col in df.columns]

            # Add row numbers (skip for "No data" sheets)
            if not (len(df) == 1 and df.iloc[0, 0] == "No data"):
                df.insert(0, "#", range(1, len(df) + 1))

            # Export to Excel and auto-fit columns
            df.to_excel(writer, sheet_name=category, index=False)
            worksheet = writer.sheets[category]

            # Auto-fit column widths
            for column in worksheet.columns:
                column_letter = column[0].column_letter
                max_length = max(len(str(cell.value or "")) for cell in column)
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = max(adjusted_width, 8)

    # Show completion message and return success
    xprint(type=Text.SPECIAL, text=DONE)

    return True
