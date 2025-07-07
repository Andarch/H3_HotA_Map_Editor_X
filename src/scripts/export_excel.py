import re
import os
import pandas as pd
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from ..common import *
from ..file_io import is_file_writable
from .excel.process_objects import *


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
            # Create DataFrame with preserved column order
            if objects:
                # Get column order from first object
                column_order = list(objects[0].keys())
                # Create DataFrame and reorder columns to match original key order
                df = pd.DataFrame(objects)
                df = df.reindex(columns=column_order)
            else:
                df = pd.DataFrame([{"": "No data"}])

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
            df.columns = [str(col).replace('_', ' ').title().replace('Id', 'ID').replace('Xp', 'XP').replace('Ai', 'AI') for col in df.columns]

            # Add row numbers (skip for "No data" sheets)
            if not (len(df) == 1 and df.iloc[0, 0] == "No data"):
                df.insert(0, "#", range(1, len(df) + 1))

            # Export to Excel and auto-fit columns
            df.to_excel(writer, sheet_name=category, index=False)
            worksheet = writer.sheets[category]

            # Handle image embedding for portrait columns
            if category == "Heroes" and "Portrait" in df.columns:
                portrait_col_idx = df.columns.get_loc("Portrait")
                portrait_col_letter = get_column_letter(portrait_col_idx + 1)

                # Set row height for images and embed portraits
                for row_idx, portrait_path in enumerate(df["Portrait"], start=2):  # Start at row 2 (after header)
                    if portrait_path and os.path.exists(portrait_path):
                        try:
                            # Create image object
                            img = Image(portrait_path)

                            # Resize image to fit in cell (max 64x64 pixels)
                            max_size = 64
                            if img.width > max_size or img.height > max_size:
                                scale = min(max_size / img.width, max_size / img.height)
                                img.width = int(img.width * scale)
                                img.height = int(img.height * scale)

                            # Set cell position
                            cell_ref = f"{portrait_col_letter}{row_idx}"
                            img.anchor = cell_ref

                            # Add image to worksheet
                            worksheet.add_image(img)

                            # Set row height to accommodate image
                            worksheet.row_dimensions[row_idx].height = max(img.height + 5, 20)

                            # Clear the cell text since we're showing the image
                            worksheet[cell_ref].value = ""

                        except Exception as e:
                            # If image embedding fails, keep the path as text
                            print(f"Warning: Could not embed image {portrait_path}: {e}")

                # Set portrait column width
                worksheet.column_dimensions[portrait_col_letter].width = 12

            # Auto-fit other column widths
            for column in worksheet.columns:
                column_letter = column[0].column_letter
                if category == "Heroes" and column_letter == portrait_col_letter:
                    continue  # Skip portrait column, already set

                max_length = max(len(str(cell.value or "")) for cell in column)
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = max(adjusted_width, 8)

    # Show completion message and return success
    xprint(type=Text.SPECIAL, text=DONE)

    return True
