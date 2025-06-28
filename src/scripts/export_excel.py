from copy import deepcopy
import pandas as pd
import data.objects as objects
from ..common import *
from ..menus import *

def export_excel(map_key: dict) -> bool:
    def main(map_key: dict) -> bool:
        filename = map_key['filename']
        if filename.endswith('.h3m'): filename = filename[:-4]
        if not filename.endswith('.xlsx'): filename += '.xlsx'
        type = get_export_type()
        if not type: return False
        xprint()
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            match type:
                case 1: export_full_data(map_key, writer)
                case 2: export_hero_data(map_key, writer)
                case 3: export_terrain_data(map_key, writer)
                case 4: export_object_data(map_key, writer)
        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def export_full_data(map_key: dict, writer):
        sections = ["general", "player_specs", "rumors", "hero_data", "terrain", "object_defs", "object_data", "events"]
        for section in sections:
            section_name = section.replace("_", " ").title()
            section_data = map_key[section]
            if section in ["terrain", "object_data", "events"]:
                total_items = len(section_data)
                if section in ["terrain", "object_data"]: update_interval = 10000
                elif section == "events": update_interval = 1
                xprint(text=f"Exporting section... {Color.CYAN.value}{section_name} 0/{total_items}{Color.RESET.value}", overwrite=1)
                processed_items = []
                for i, item in enumerate(section_data, 1):
                    processed_items.append(item)
                    if i % update_interval == 0 or i == total_items:
                        xprint(text=f"Exporting section... {Color.CYAN.value}{section_name} {i}/{total_items}{Color.RESET.value}", overwrite=1)
                df = pd.DataFrame(processed_items)
                if section in ["terrain", "object_data"]: xprint(text=f"Formatting...")
            else:
                xprint(text=f"Exporting section... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
                time.sleep(Sleep.SHORT.value)
                if isinstance(section_data, list) and section_data:
                    df = pd.DataFrame(section_data)
                elif section == "general":
                    df = create_general_dataframe(section_data)
                else:
                    df = pd.DataFrame([{section: "No data"}])
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name=section_name, index=False)
            worksheet = writer.sheets[section_name]
            auto_fit_columns(worksheet)
            if section in ["terrain", "object_data"]: xprint(text="", overwrite=2)
            elif section == "events": xprint(type=Text.ACTION, text="Writing Excel file to disk...", overwrite=1)

    def export_hero_data(map_key: dict, writer):
        hero_data = get_hero_data(map_key)
        sections = ["player_specs", "custom_heroes", "hero_data", "object_data"]
        for section in sections:
            section_name = section.replace("_", " ").title()
            xprint(type=Text.ACTION, text=f"Exporting Excel file... {Color.CYAN.value}{section_name}{Color.RESET.value}", overwrite=1)
            df = pd.DataFrame(hero_data[section])
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name=section_name, index=False)
            worksheet = writer.sheets[section_name]
            auto_fit_columns(worksheet)

    def export_terrain_data(map_key: dict, writer):
        terrain = map_key["terrain"]
        if isinstance(terrain, list): df = pd.DataFrame(terrain)
        else: df = pd.DataFrame([terrain])
        df = sanitize_dataframe(df)
        df.to_excel(writer, sheet_name="Terrain", index=False)
        auto_fit_columns(writer.sheets["Terrain"])

    def export_object_data(map_key: dict, writer):
        xprint(type=Text.ACTION, text=f"Exporting object data...", overwrite=1)
        object_data = map_key["object_data"]
        if isinstance(object_data, list): df = pd.DataFrame(object_data)
        else: df = pd.DataFrame([object_data])
        df = sanitize_dataframe(df)
        df.to_excel(writer, sheet_name="Object Data", index=False)
        auto_fit_columns(writer.sheets["Object Data"])

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
