import os
import re

import pandas as pd
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from src.common import DONE, MsgType, draw_header, is_file_writable, map_data, xprint
from src.defs import objects

from . import worksheets

# Define columns to remove per category
_COLUMNS_TO_REMOVE = {
    "Heroes": [
        "zone_type",
        "zone_color",
        "def_id",
        "id",
        "sub_id",
        "type",
        "subtype",
        "owner",
        "hero_id",
        "default_name",
        "has_custom_name",
        "custom_name",
        "formation",
        "has_portrait",
        "portrait_id",
        "patrol",
        "has_biography",
        "coords_offset",
        # Remove individual artifact slot columns since we're creating combined "artifacts" and "backpack" columns
        "head",
        "shoulders",
        "neck",
        "right_hand",
        "left_hand",
        "torso",
        "right_ring",
        "left_ring",
        "feet",
        "misc1",
        "misc2",
        "misc3",
        "misc4",
        "misc5",
        "ballista",
        "ammo_cart",
        "first_aid_tent",
        "catapult",
        "spell_book",
        # Remove any existing backpack-related columns that might conflict
        "artifacts_backpack",
        "artifact_backpack",
    ],
    "Towns": [
        "zone_type",
        "zone_color",
        "def_id",
        "id",
        "sub_id",
        "type",
        "owner",
        "garrison_formation",
        "has_custom_buildings",
        "buildings_built",
        "buildings_disabled",
        "spells_must_appear",
        "spells_cant_appear",
        "buildings_special",
        "events",
        "coords_offset",
    ],
    "Monsters": ["type", "start_bytes", "middle_bytes"],
    "Spells": ["def_id", "id", "sub_id", "type", "contents"],
    "Artifacts": ["def_id", "id", "sub_id", "type", "has_common", "coords_offset"],
    "Resources": ["def_id", "id", "sub_id", "type", "has_common", "coords_offset"],
    "Campfire": ["def_id", "id", "sub_id", "type"],
    "Scholar": ["def_id", "id", "sub_id", "type"],
    "Treasure Chest": ["def_id", "id", "sub_id", "type"],
    "Sea Chest": ["def_id", "id", "sub_id", "type"],
    "Shipwreck Survivor": ["def_id", "id", "sub_id", "type"],
    "Flotsam & Jetsam": ["def_id", "id", "sub_id", "type"],
    "Sea Barrel": ["def_id", "id", "sub_id", "type"],
    "Vial of Mana": ["def_id", "id", "sub_id", "type"],
    "Ancient Lamp": ["def_id", "id", "sub_id", "type"],
    "Grave": ["def_id", "id", "sub_id", "type", "resource"],
    "Creature Banks": ["def_id", "id", "sub_id", "type", "rewards"],
    "Garrisons": ["zone_type", "zone_color", "def_id", "id", "sub_id", "type", "owner", "coords_offset"],
}


def export() -> bool:
    filepath = "....maps/exports/Excel/"
    filename = os.path.join(filepath, map_data["filename"][:-4] + ".xlsx")

    # Check if Excel file is already open
    if not is_file_writable(filename):
        return False

    # Show initial export message
    draw_header()
    xprint(type=MsgType.ACTION, text="Exporting Excel file…")

    # Open Excel writer with openpyxl engine
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Process objects (categorize and clean data)
        processed_data = _process_data()

        # Compile regex for Excel illegal characters
        illegal_chars = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

        # Write each category to Excel
        for category, items in processed_data.items():
            # Skip Decor category from Excel export
            if category == "Decor":
                continue

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
                df[col] = (
                    df[col]
                    .apply(
                        lambda value: (
                            illegal_chars.sub("", value)
                            if isinstance(value, str)
                            else (
                                illegal_chars.sub("", value.decode("latin-1", errors="ignore"))
                                if isinstance(value, bytes)
                                else value
                            )
                        )
                    )
                    .apply(lambda value: "'" + value if isinstance(value, str) and value and value[0] == "=" else value)
                )

            # Format column headers
            df.columns = [
                str(col).replace("_", " ").title().replace("Id", "ID").replace("Xp", "XP").replace("Ai", "AI")
                for col in df.columns
            ]

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
    xprint(type=MsgType.SPECIAL, text=DONE)

    return True


def _process_data() -> dict:
    object_data = map_data["object_data"]

    # Categorize objects
    categorized_objects = {category: [] for category in objects.Categories.CATEGORIES.keys()}

    # Step 1: Categorize objects
    for obj in object_data:
        categorized = False

        # Special handling for Border_Gate based on sub_id
        if obj["id"] == objects.ID.Border_Gate:
            if obj["sub_id"] == 1000:  # Quest Gate
                categorized_objects["Quest Objects"].append(obj)
            elif obj["sub_id"] == 1001:  # Grave - reward giving object
                categorized_objects["Grave"].append(obj)
            else:  # Regular Border Gate
                categorized_objects["Border Objects"].append(obj)
            categorized = True
        # Special handling for HotA_Collectible based on subtype
        elif obj["id"] == objects.ID.HotA_Collectible:
            subtype = obj.get("subtype", "")
            if hasattr(subtype, "name"):
                subtype_name = subtype.name
            elif hasattr(subtype, "value"):
                # Map subtype value to name using HotA_Collectible enum
                try:
                    subtype_name = objects.HotA_Collectible(subtype.value).name
                except (ValueError, AttributeError):
                    subtype_name = str(subtype)
            else:
                subtype_name = str(subtype)
            if subtype_name == "Jetsam":
                categorized_objects["Flotsam & Jetsam"].append(obj)
            elif subtype_name == "Sea Barrel":
                categorized_objects["Sea Barrel"].append(obj)
            elif subtype_name == "Vial of Mana":
                categorized_objects["Vial of Mana"].append(obj)
            elif subtype_name == "Ancient Lamp":
                categorized_objects["Ancient Lamp"].append(obj)
            else:
                # Fallback to Simple Objects if unknown subtype
                categorized_objects["Simple Objects"].append(obj)
            categorized = True
        else:
            # Check each category
            for category, object_ids in objects.Categories.CATEGORIES.items():
                if obj["id"] in object_ids:
                    # Skip HotA_Collectible here since we handled it specially above
                    if obj["id"] == objects.ID.HotA_Collectible:
                        continue
                    categorized_objects[category].append(obj)
                    categorized = True
                    break

        # If object doesn't fit any category, add to Simple Objects
        if not categorized:
            categorized_objects["Simple Objects"].append(obj)

    # Step 2: Process each category
    processed_data = {}

    for category, items in categorized_objects.items():
        if items:
            # Sort objects by ID first, then by sub_id
            items.sort(key=lambda obj: (obj["id"], obj.get("sub_id", 0)))

            # Category-specific transformations
            if category == "Heroes":
                items = worksheets.heroes.process(items)
            elif category == "Towns":
                items = worksheets.towns.process(items)
            elif category == "Monsters":
                items = worksheets.monsters.process(items)
            elif category == "Spells":
                items = worksheets.spells.process(items)
            elif category == "Artifacts":
                items = worksheets.artifacts.process(items)
            elif category == "Resources":
                items = worksheets.resources.process(items)
            elif category == "Campfire":
                items = worksheets.campfire.process(items)
            elif category == "Scholar":
                items = worksheets.scholar.process(items)
            elif category == "Treasure Chest":
                items = worksheets.treasure_chest.process(items)
            elif category == "Sea Chest":
                items = worksheets.sea_chest.process(items)
            elif category == "Shipwreck Survivor":
                items = worksheets.shipwreck_survivor.process(items)
            elif category == "Flotsam & Jetsam":
                items = worksheets.flotsam_jetsam.process(items)
            elif category == "Sea Barrel":
                items = worksheets.sea_barrel.process(items)
            elif category == "Vial of Mana":
                items = worksheets.vial_of_mana.process(items)
            elif category == "Ancient Lamp":
                items = worksheets.ancient_lamp.process(items)
            elif category == "Grave":
                items = worksheets.grave.process(items)
            elif category == "Creature Banks":
                items = worksheets.creature_banks.process(items)
            elif category == "Garrisons":
                items = worksheets.garrisons.process(items)

            # Remove unwanted columns (universal + category-specific)
            cleaned_items = []
            columns_to_remove = _COLUMNS_TO_REMOVE.get(category, [])
            for item in items:
                # Remove _bytes columns (universal) and category-specific columns
                cleaned_item_raw = {
                    k: v for k, v in item.items() if not k.endswith("_bytes") and k not in columns_to_remove
                }

                # Clean empty list representations
                cleaned_item = {}
                for key, value in cleaned_item_raw.items():
                    if isinstance(value, str) and value == "[]":
                        cleaned_item[key] = ""
                    elif isinstance(value, list) and len(value) == 0:
                        cleaned_item[key] = ""
                    else:
                        cleaned_item[key] = value
                cleaned_items.append(cleaned_item)

            processed_data[category] = cleaned_items

    return processed_data
