from copy import deepcopy
import pandas as pd
import data.objects as objects
from ..common import *
from ..menus import *

def export_excel(map_key: dict) -> bool:
    def main(map_key: dict) -> bool:
        all_sections = ["general", "player_specs", "rumors", "hero_data", "terrain", "object_defs", "object_data", "events"]
        hero_sections = ["player_specs", "custom_heroes", "hero_data", "object_data"]
        terrain_sections = ["terrain"]
        object_sections = ["object_data"]

        filename = map_key["filename"]
        if filename.endswith(".h3m"): filename = filename[:-4]

        export_type = get_export_type()
        if not export_type: return False

        # Append export type suffix to filename
        suffix_map = {1: "_all", 2: "_heros", 3: "_terrain", 4: "_objects"}
        filename += suffix_map[export_type]

        if not filename.endswith(".xlsx"): filename += ".xlsx"

        xprint()
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            match export_type:
                case 1: export_data(map_key, writer, all_sections)
                case 2: export_data(map_key, writer, hero_sections, use_hero_data=True)
                case 3: export_data(map_key, writer, terrain_sections)
                case 4: export_data(map_key, writer, object_sections)

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
                total_items = len(section_data)
                if section in ["terrain", "object_data"]:
                    update_interval = 10000
                elif section == "events":
                    update_interval = 1

                xprint(text=f"Exporting... {Color.CYAN.value}{section_name} 0/{total_items}{Color.RESET.value}", overwrite=1)
                processed_items = []
                for i, item in enumerate(section_data, 1):
                    processed_items.append(item)
                    if i % update_interval == 0 or i == total_items:
                        xprint(text=f"Exporting... {Color.CYAN.value}{section_name} {i}/{total_items}{Color.RESET.value}", overwrite=1)

                # Create DataFrame based on processed items
                df = pd.DataFrame(processed_items)
                if section in ["terrain", "object_data"]:
                    xprint(text="Formatting...")
            else:
                # Handle regular sections
                xprint(text=f"Exporting... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
                time.sleep(Sleep.SHORT.value)

                # Create DataFrame based on section data
                if isinstance(section_data, list) and section_data:
                    df = pd.DataFrame(section_data)
                elif section == "general":
                    df = create_general_dataframe(section_data)
                else:
                    df = pd.DataFrame([{section: "No data"}])

            # Common processing for all sections
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name=section_name, index=False)
            worksheet = writer.sheets[section_name]
            auto_fit_columns(worksheet)

            # Progress cleanup for large sections
            if section in ["terrain", "object_data"] and not use_hero_data:
                xprint(text="", overwrite=2)

            # Show "Writing Excel file to disk..." message for the last section
            if section_idx == len(sections) - 1:
                xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)

    def flatten_dict(d, parent_key="", sep="_"):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict): items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, bytes): items.append((new_key, v.decode("latin-1")))
            else: items.append((new_key, str(v) if isinstance(v, (list, tuple)) else v))
        return dict(items)

    def create_general_dataframe(general_data):
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

    def get_export_type() -> int:
        input = xprint(menu=Menu.EXCEL.value)
        if input == KB.ESC.value: return False
        else: return int(input)

    def get_hero_data(map_key: dict) -> dict:
        player_specs = deepcopy(map_key['player_specs'])
        player_specs[:] = [player for player in player_specs if len(player["available_heroes"]) > 0]
        for player in player_specs:
            del player["ai_behavior"]
            del player["alignments_customized"]
            del player["alignments_allowed"]
            del player["alignment_is_random"]
            del player["has_main_town"]
            if "generate_hero" in player: del player["generate_hero"]
            if "town_type" in player: del player["town_type"]
            if "town_coords" in player: del player["town_coords"]
            if "garbage_byte" in player: del player["garbage_byte"]
            if "placeholder_heroes" in player: del player["placeholder_heroes"]
        custom_heroes = deepcopy(map_key["start_heroes"]["custom_heroes"])
        hero_data = deepcopy(map_key["hero_data"])
        hero_data[:] = [hero for hero in hero_data if len(hero) > 3]
        object_data = deepcopy(map_key["object_data"])
        object_data[:] = [obj for obj in object_data if obj["type"] in (objects.ID.Hero, objects.ID.Prison)]
        final_hero_data = {
            "player_specs": player_specs,
            "custom_heroes": custom_heroes,
            "hero_data": hero_data,
            "object_data": object_data
        }
        return final_hero_data

    def sanitize_dataframe(df):
        import re
        illegal_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')
        def clean_value(value):
            if isinstance(value, str):
                cleaned = illegal_chars.sub("", value)
                if cleaned and cleaned[0] in ("=", "+", "-", "@"):
                    cleaned = "'" + cleaned
                return cleaned
            elif isinstance(value, bytes):
                try:
                    decoded = value.decode("latin-1", errors="ignore")
                    cleaned = illegal_chars.sub("", decoded)
                    if cleaned and cleaned[0] in ("=", "+", "-", "@"):
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

    return main(map_key)
