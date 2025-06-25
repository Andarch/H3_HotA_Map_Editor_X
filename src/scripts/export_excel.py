from copy import deepcopy
import pandas as pd
import data.objects as objects
from ..common import *
from ..menus import *

def export_excel(map_key: dict) -> bool:
    def main(map_key: dict) -> bool:
        filename = map_key['filename']
        if filename.endswith('.h3m'):
            filename = filename[:-4]
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'

        type = get_export_type()
        if not type: return False

        xprint()
        xprint(text=f"Exporting Excel file...", overwrite=True)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            match type:
                case 1: export_full_data(map_key, writer)
                case 2: export_hero_data(map_key, writer)
                case 3: export_terrain_data(map_key, writer)

        xprint(type=Text.ACTION, text=f"Exporting Excel file...", overwrite=True)

        xprint(type=Text.SPECIAL, text=DONE)
        return True

    def export_full_data(map_key: dict, writer):
        # Export each main section to its own sheet
        sections = [
            "general", "player_specs", "conditions", "teams", 
            "start_heroes", "ban_flags", "rumors", "hero_data",
            "terrain", "object_defs", "object_data", "events"
        ]
        
        # Sections that should be transposed (single row data -> key-value pairs)
        transpose_sections = {"general", "conditions", "teams", "ban_flags"}
        
        for section in sections:
            if section in map_key:
                formatted_section = section.replace('_', ' ').title()
                xprint(text=f"Exporting Excel file... {Color.CYAN.value}{formatted_section}{Color.RESET.value}", overwrite=True)
                time.sleep(Sleep.SHORT.value)
                section_data = map_key[section]                
                # Handle different data types appropriately
                if isinstance(section_data, list) and section_data:
                    # For lists, create DataFrame directly
                    df = pd.DataFrame(section_data)
                elif isinstance(section_data, dict):
                    # For dictionaries, flatten and create single-row DataFrame
                    flattened_data = flatten_dict(section_data)
                    df = pd.DataFrame([flattened_data])
                    
                    # Transpose specific sections for better readability
                    if section in transpose_sections:
                        df = df.transpose()
                        df.columns = ['Value']
                        df.index.name = 'Key'
                        df = df.reset_index()
                else:
                    # For other types, create simple DataFrame
                    df = pd.DataFrame([{section: section_data}])
                
                # Sanitize DataFrame to remove illegal characters
                df = sanitize_dataframe(df)
                
                # Use section name as sheet name, capitalize first letter
                sheet_name = section.replace('_', ' ').title()
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def export_hero_data(map_key: dict, writer):
        hero_data = get_hero_data(map_key)
        if hero_data['player_specs']: 
            df = pd.DataFrame(hero_data['player_specs'])
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name='Player_Specs', index=False)        
        if hero_data['custom_heroes']: 
            df = pd.DataFrame(hero_data['custom_heroes'])
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name='Custom_Heroes', index=False)        
        if hero_data['hero_data']: 
            df = pd.DataFrame(hero_data['hero_data'])
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name='Hero_Data', index=False)        
        if hero_data['object_data']: 
            df = pd.DataFrame(hero_data['object_data'])
            df = sanitize_dataframe(df)
            df.to_excel(writer, sheet_name='Object_Data', index=False)

    def export_terrain_data(map_key: dict, writer):
        terrain = map_key['terrain']
        if isinstance(terrain, list):
            df = pd.DataFrame(terrain)
        else:
            df = pd.DataFrame([terrain])
        df = sanitize_dataframe(df)
        df.to_excel(writer, sheet_name='Terrain', index=False)

    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, bytes):
                items.append((new_key, v.decode('latin-1')))
            else:
                items.append((new_key, str(v) if isinstance(v, (list, tuple)) else v))
        return dict(items)

    def get_export_type() -> int:
        input = xprint(menu=Menu.JSON.value)
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
            if "generate_hero" in player:
                del player["generate_hero"]
            if "town_type" in player:
                del player["town_type"]
            if "town_coords" in player:
                del player["town_coords"]
            if "garbage_byte" in player:
                del player["garbage_byte"]
            if "placeholder_heroes" in player:
                del player["placeholder_heroes"]

        custom_heroes = deepcopy(map_key['start_heroes']['custom_heroes'])
        hero_data = deepcopy(map_key['hero_data'])
        hero_data[:] = [hero for hero in hero_data if len(hero) > 3]
        object_data = deepcopy(map_key['object_data'])
        object_data[:] = [obj for obj in object_data if obj["type"] in (objects.ID.Hero, objects.ID.Prison)]

        final_hero_data = {
            "player_specs": player_specs,
            "custom_heroes": custom_heroes,
            "hero_data": hero_data,
            "object_data": object_data
        }
        return final_hero_data

    def sanitize_dataframe(df):
        """Remove illegal characters and prevent formula interpretation in Excel worksheets."""
        import re
        
        # Define illegal characters pattern (control characters except tab, newline, carriage return)
        illegal_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')
        
        def clean_value(value):
            if isinstance(value, str):
                # Remove illegal characters
                cleaned = illegal_chars.sub('', value)
                # Prevent formula interpretation by prefixing with single quote if starts with formula characters
                if cleaned and cleaned[0] in ('=', '+', '-', '@'):
                    cleaned = "'" + cleaned
                return cleaned
            elif isinstance(value, bytes):
                # Decode bytes and remove illegal characters
                try:
                    decoded = value.decode('latin-1', errors='ignore')
                    cleaned = illegal_chars.sub('', decoded)
                    # Prevent formula interpretation
                    if cleaned and cleaned[0] in ('=', '+', '-', '@'):
                        cleaned = "'" + cleaned
                    return cleaned
                except:
                    return str(value)
            else:
                return value
        
        # Apply cleaning to all columns
        for col in df.columns:
            df[col] = df[col].apply(clean_value)
        
        return df

    return main(map_key)
