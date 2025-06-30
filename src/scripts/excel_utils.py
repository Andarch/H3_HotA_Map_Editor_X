"""
Excel export utility functions for Heroes 3 map editor.
Contains common functionality for DataFrame processing and worksheet formatting.
"""

import re
import pandas as pd
from .data_utils import *


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


def export_sections_to_excel(writer, sections_data, use_progress=True, is_final_export=True):
    """
    Generic function to export multiple sections/categories to Excel worksheets.

    This function can handle both sequential section exports and categorized object exports
    by accepting a dictionary of section/category names mapped to their data.

    Args:
        writer: Excel writer object
        sections_data: Dictionary mapping section/category names to their data
        use_progress: Whether to show progress updates during export
        is_final_export: Whether to show "Writing Excel file to disk..." message at the end

    Returns:
        None
    """
    total_sections = len(sections_data)

    for section_idx, (section_name, section_info) in enumerate(sections_data.items()):
        # Handle both simple data and complex section info
        if isinstance(section_info, dict) and 'data' in section_info:
            # Complex section info with additional parameters
            data = section_info['data']
            pre_processed = section_info.get('pre_processed', False)
            add_row_numbers = section_info.get('add_row_numbers', True)
            section_key = section_info.get('section_key', 'data')
        else:
            # Simple data
            data = section_info
            pre_processed = False
            add_row_numbers = True
            section_key = section_name.lower().replace(' ', '_')

        if data is not None and len(data) > 0:
            # Show formatting message for each section
            if use_progress:
                from ..common import xprint, Color
                xprint(text=f"Formatting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)

            # Process non-empty data
            if isinstance(data, pd.DataFrame):
                df = data
            else:
                df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])

            # Export to worksheet
            export_section_to_worksheet(
                writer, df, section_key, section_name,
                add_row_numbers=add_row_numbers,
                pre_processed=pre_processed
            )
        else:
            # Create empty sheet for no data
            create_empty_worksheet(writer, section_name, "No data")

    # Show final completion message
    if is_final_export:
        from ..common import xprint, Text
        xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)
