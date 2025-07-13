import re
import os
import pandas as pd
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from ..common import *
from ..file_io import is_file_writable
from . import excel
import data.objects as objects
import data.spells as spells


# Define columns to remove per category
_COLUMNS_TO_REMOVE = {
    "Heroes": ["def_id", "id", "sub_id", "type", "subtype", "owner", "hero_id", "default_name", "has_custom_name", "custom_name", "formation",
               "has_portrait", "portrait_id", "patrol", "has_biography",
               # Remove individual artifact slot columns since we're creating combined "artifacts" and "backpack" columns
               "head", "shoulders", "neck", "right_hand", "left_hand", "torso", "right_ring", "left_ring", "feet",
               "misc1", "misc2", "misc3", "misc4", "misc5", "ballista", "ammo_cart", "first_aid_tent", "catapult", "spell_book",
               # Remove any existing backpack-related columns that might conflict
               "artifacts_backpack", "artifact_backpack"],
    "Towns": ["def_id", "id", "sub_id", "type", "owner", "garrison_formation", "has_custom_buildings", "buildings_built", "buildings_disabled",
              "spells_must_appear", "spells_cant_appear", "buildings_special", "events"],
    "Monsters": ["def_id", "id", "sub_id", "type", "start_bytes", "middle_bytes", "is_value"],
    "Spells": ["def_id", "id", "sub_id", "type", "contents"],
    "Town Events": ["hota_town_event_1", "hota_town_event_2"],
    "Global Events": [],  # No columns to remove for global events
    "Artifacts": ["def_id", "id", "sub_id", "type", "has_common"],
    "Resources": ["def_id", "id", "sub_id", "type", "has_common"],
    "Campfire": ["def_id", "id", "sub_id", "type"],
    "Scholar": ["def_id", "id", "sub_id", "type"],
    "Treasure Chest": ["def_id", "id", "sub_id", "type"],
    "Sea Chest": ["def_id", "id", "sub_id", "type"],
    "Shipwreck Survivor": ["def_id", "id", "sub_id", "type"],
    "Flotsam & Jetsam": ["def_id", "id", "sub_id", "type"],
    "Sea Barrel": ["def_id", "id", "sub_id", "type"],
    "Vial of Mana": ["def_id", "id", "sub_id", "type"],
    "Ancient Lamp": ["def_id", "id", "sub_id", "type"],
}


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
        processed_data = _process_data(map_key["object_data"], map_key["events"])

        # Compile regex for Excel illegal characters
        illegal_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

        # Write each category to Excel
        for category, items in processed_data.items():
            # Create DataFrame with preserved column order
            if items:
                # Get column order from first object
                column_order = list(items[0].keys())
                # Create DataFrame and reorder columns to match original key order
                df = pd.DataFrame(items)
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


def _process_data(object_data, events) -> dict:
    """Categorize and process data for Excel export"""
    # Categorize objects
    processed_data = {category: [] for category in objects.CATEGORIES.keys()}

    # Add Town Events and Global Events categories - will be populated separately
    processed_data["Town Events"] = []
    processed_data["Global Events"] = []

    # Step 1: Categorize objects
    for obj in object_data:
        categorized = False

        # Special handling for Border_Gate based on sub_id
        if obj["id"] == objects.ID.Border_Gate:
            if obj["sub_id"] == 1000:  # Quest Gate
                processed_data["Quest Objects"].append(obj)
            elif obj["sub_id"] == 1001:  # Grave - reward giving object
                processed_data["Grave"].append(obj)
            else:  # Regular Border Gate
                processed_data["Border Objects"].append(obj)
            categorized = True
        # Special handling for HotA_Collectible based on subtype
        elif obj["id"] == objects.ID.HotA_Collectible:
            subtype = obj.get("subtype", "")
            if hasattr(subtype, 'name'):
                subtype_name = subtype.name
            elif hasattr(subtype, 'value'):
                # Map subtype value to name using HotA_Collectible enum
                try:
                    subtype_name = objects.HotA_Collectible(subtype.value).name
                except (ValueError, AttributeError):
                    subtype_name = str(subtype)
            else:
                subtype_name = str(subtype)

            if subtype_name == "Jetsam":
                processed_data["Flotsam & Jetsam"].append(obj)
            elif subtype_name == "Sea Barrel":
                processed_data["Sea Barrel"].append(obj)
            elif subtype_name == "Vial of Mana":
                processed_data["Vial of Mana"].append(obj)
            elif subtype_name == "Ancient Lamp":
                processed_data["Ancient Lamp"].append(obj)
            else:
                # Fallback to Simple Objects if unknown subtype
                processed_data["Simple Objects"].append(obj)
            categorized = True
        else:
            # Check each category
            for category, object_ids in objects.CATEGORIES.items():
                if obj["id"] in object_ids:
                    # Skip HotA_Collectible here since we handled it specially above
                    if obj["id"] == objects.ID.HotA_Collectible:
                        continue
                    processed_data[category].append(obj)
                    categorized = True
                    break

        # If object doesn't fit any category, add to Simple Objects
        if not categorized:
            processed_data["Simple Objects"].append(obj)

    # Step 2: Process each category
    for category, items in processed_data.items():
        if category in ["Town Events", "Global Events"]:
            continue  # Handle these separately after processing towns and global events

        if items:
            # Sort objects by ID first, then by sub_id
            items.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

            # Category-specific transformations
            if category == "Heroes":
                items = excel.flatten_heroes(items)
            elif category == "Towns":
                items = excel.flatten_towns(items)
            elif category == "Monsters":
                items = excel.flatten_monsters(items)
            elif category == "Spells":
                items = excel.flatten_spells(items)
            elif category == "Artifacts":
                items = excel.flatten_artifacts(items)
            elif category == "Resources":
                items = excel.flatten_resources(items)
            elif category == "Campfire":
                items = excel.flatten_campfire(items)
            elif category == "Scholar":
                items = excel.flatten_scholar(items)
            elif category == "Treasure Chest":
                items = excel.flatten_treasure_chest(items)
            elif category == "Sea Chest":
                items = excel.flatten_sea_chest(items)
            elif category == "Shipwreck Survivor":
                items = excel.flatten_shipwreck_survivor(items)
            elif category == "Flotsam & Jetsam":
                items = excel.flatten_flotsam_jetsam(items)
            elif category == "Sea Barrel":
                items = excel.flatten_sea_barrel(items)
            elif category == "Vial of Mana":
                items = excel.flatten_vial_of_mana(items)
            elif category == "Ancient Lamp":
                items = excel.flatten_ancient_lamp(items)

            # Remove unwanted columns (universal + category-specific)
            cleaned_data = []
            columns_to_remove = _COLUMNS_TO_REMOVE.get(category, [])
            for item in items:
                # Remove _bytes columns (universal) and category-specific columns
                cleaned_item_raw = {k: v for k, v in item.items()
                                   if not k.endswith('_bytes') and k not in columns_to_remove}

                # Clean empty list representations
                cleaned_item = {}
                for key, value in cleaned_item_raw.items():
                    if isinstance(value, str) and value == "[]":
                        cleaned_item[key] = ""
                    elif isinstance(value, list) and len(value) == 0:
                        cleaned_item[key] = ""
                    else:
                        cleaned_item[key] = value
                cleaned_data.append(cleaned_item)

            processed_data[category] = cleaned_data

    # Step 3: Extract and process town events
    town_events = []
    for obj in object_data:
        if obj["id"] in [objects.ID.Town, objects.ID.Random_Town] and "events" in obj and obj["events"]:
            for event in obj["events"]:
                # Create a flattened event object with town context
                flattened_event = excel.flatten_town_events(event, obj)
                town_events.append(flattened_event)

    processed_data["Town Events"] = town_events

    # Step 4: Process global events
    global_events = excel.flatten_events(events or [])
    processed_data["Global Events"] = global_events

    # Reorder to place Campfires after Resources and before Treasure
    final_data = {}
    for key in processed_data.keys():
        if key == "Resources":
            final_data[key] = processed_data[key]
            if "Campfires" in processed_data:
                final_data["Campfires"] = processed_data["Campfires"]
        elif key == "Campfires":
            continue  # Already inserted after Resources
        elif key == "Towns":
            final_data[key] = processed_data[key]
            final_data["Town Events"] = processed_data["Town Events"]
            final_data["Global Events"] = processed_data["Global Events"]
        elif key not in ["Town Events", "Global Events"]:
            final_data[key] = processed_data[key]

    return final_data
