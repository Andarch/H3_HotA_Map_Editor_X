from copy import deepcopy
import data.objects as objects


def categorize_objects(object_data) -> dict:

    categories = get_obj_categories()
    categorized_objects = {category: [] for category in categories.keys()}

    for obj in object_data:
        categorized = False

        # Special handling for Border_Gate based on sub_id
        if obj["id"] == objects.ID.Border_Gate:
            if obj["sub_id"] == 1000:  # Quest Gate
                categorized_objects["Quest Objects"].append(obj)
            elif obj["sub_id"] == 1001:  # Grave - reward giving object
                categorized_objects["Treasure"].append(obj)
            else:  # Regular Border Gate
                categorized_objects["Border Objects"].append(obj)
            categorized = True
        else:
            # Check each category
            for category, object_ids in categories.items():
                if obj["id"] in object_ids:
                    categorized_objects[category].append(obj)
                    categorized = True
                    break

        # If object doesn't fit any category, add to Simple Objects
        if not categorized:
            categorized_objects["Simple Objects"].append(obj)

    return categorized_objects


def get_obj_categories() -> dict:
    return {
        "Heroes": {
            objects.ID.Hero, objects.ID.Prison, objects.ID.Random_Hero, objects.ID.Hero_Placeholder
        },
        "Towns": {
            objects.ID.Town, objects.ID.Random_Town
        },
        "Monsters": {
            objects.ID.Monster, objects.ID.Random_Monster, objects.ID.Random_Monster_1,
            objects.ID.Random_Monster_2, objects.ID.Random_Monster_3, objects.ID.Random_Monster_4,
            objects.ID.Random_Monster_5, objects.ID.Random_Monster_6, objects.ID.Random_Monster_7
        },
        "Spells": {
            objects.ID.Shrine_of_Magic_Incantation, objects.ID.Shrine_of_Magic_Gesture,
            objects.ID.Shrine_of_Magic_Thought, objects.ID.Pyramid, objects.ID.Spell_Scroll
        },
        "Artifacts": {
            objects.ID.Artifact, objects.ID.Random_Artifact, objects.ID.Random_Treasure_Artifact,
            objects.ID.Random_Minor_Artifact, objects.ID.Random_Major_Artifact, objects.ID.Random_Relic
        },
        "Resources": {
            objects.ID.Resource, objects.ID.Random_Resource
        },
        "Treasure": {
            objects.ID.Treasure_Chest, objects.ID.Sea_Chest, objects.ID.Flotsam, objects.ID.Campfire,
            objects.ID.Shipwreck_Survivor, objects.ID.HotA_Collectible
        },
        "Other Pickups": {
            objects.ID.Scholar, objects.ID.Ocean_Bottle, objects.ID.Grail
        },
        "Creature Banks": {
            objects.ID.Creature_Bank, objects.ID.Derelict_Ship, objects.ID.Dragon_Utopia,
            objects.ID.Crypt, objects.ID.Shipwreck
        },
        "Garrisons": {
            objects.ID.Garrison, objects.ID.Garrison_Vertical
        },
        "Seers Huts": {
            objects.ID.Seers_Hut
        },
        "Quest Objects": {
            objects.ID.Quest_Guard
        },
        "Event Pickups": {
            objects.ID.Event, objects.ID.Pandoras_Box
        },
        "Border Objects": {
            objects.ID.Border_Guard, objects.ID.Keymasters_Tent
        },
        "Dwellings": {
            objects.ID.Creature_Generator_1, objects.ID.Creature_Generator_4, objects.ID.Random_Dwelling,
            objects.ID.Random_Dwelling_Leveled, objects.ID.Random_Dwelling_Faction
        },
        "Mines & Warehouses": {
            objects.ID.Mine, objects.ID.HotA_Warehouse, objects.ID.Abandoned_Mine
        },
        "Interactive": {
            objects.ID.University, objects.ID.Witch_Hut, objects.ID.Black_Market,
            objects.ID.HotA_Visitable_1, objects.ID.HotA_Visitable_2
        },
        "Simple Objects": {
            objects.ID.Tree_of_Knowledge, objects.ID.Lean_To, objects.ID.Wagon, objects.ID.Warriors_Tomb,
            objects.ID.Lighthouse, objects.ID.Shipyard
        },
        "Decor": objects.DECOR_OBJECTS
    }


def flatten_obj_hero_data(objects_list) -> list:
    flattened_objects = []

    for obj in objects_list:
        flattened_obj = {}

        for key, value in obj.items():
            if key == "hero_data" and isinstance(value, dict):
                # Flatten hero data dictionaries using just the sub-key names
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        # Flatten nested dictionaries (like primary_skills, artifacts_equipped)
                        for nested_key, nested_value in sub_value.items():
                            flattened_obj[nested_key] = nested_value
                    elif isinstance(sub_value, list):
                        # Special formatting for secondary_skills
                        if sub_key == "secondary_skills" and sub_value:
                            skill_lines = []
                            for skill in sub_value:
                                if isinstance(skill, dict):
                                    level_name = skill.get('level_name', '')
                                    skill_name = skill.get('name', '').replace('_', ' ')
                                    if level_name and skill_name:
                                        skill_lines.append(f"{level_name} {skill_name}")
                            flattened_obj[sub_key] = "\n".join(skill_lines) if skill_lines else ""
                        else:
                            # Convert other lists to strings
                            flattened_obj[sub_key] = str(sub_value) if sub_value else ""
                    else:
                        # Rename "id" to "hero_id" to avoid conflicts with object id
                        if sub_key == "id":
                            flattened_obj["hero_id"] = sub_value
                        else:
                            flattened_obj[sub_key] = sub_value
            else:
                # Keep non-hero_data fields as-is
                flattened_obj[key] = value

        flattened_objects.append(flattened_obj)

    return flattened_objects


def get_all_hero_data(map_key: dict) -> dict:
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
    object_data[:] = [obj for obj in object_data if obj["id"] in (objects.ID.Hero, objects.ID.Prison)]

    final_hero_data = {
        "player_specs": player_specs,
        "custom_heroes": custom_heroes,
        "hero_data": hero_data,
        "object_data": object_data
    }
    return final_hero_data


def flatten_dict(d) -> dict:
    items = []
    for k, v in d.items():
        if isinstance(v, dict):
            items.extend(flatten_dict(v).items())
        elif isinstance(v, bytes):
            items.append((k, v.decode("latin-1")))
        else:
            items.append((k, str(v) if isinstance(v, (list, tuple)) else v))
    return dict(items)
