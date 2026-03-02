from src.common import TextAlign, TextType, map_data
from src.defs import creatures, groups, objects, players
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress

HUMAN_EVENT_NAME = "[Human Bonus]"
AI_EVENT_NAME = "[AI Bonus]"
BOSS_EVENT_NAME = "[Boss Bonus]"
FOURTH_TOWN_EVENT_NAME = "[Bonus]"
MEGA_TOWN_EVENT_NAME = "[Bonus]"

##################################################
# Set lvl7 creature bonus amounts (max 666 each)
HUMAN_LVL7_CREATURES = 5
AI_LVL7_CREATURES = 15
BOSS_LVL7_CREATURES = 50
FOURTH_TOWN_LVL7_CREATURES = 15
MEGA_TOWN_LVL7_CREATURES = 20

# Set which players receive each bonus type
HUMAN_PLAYERS = [1, 1, 1, 1, 1, 1, 1, 0]
AI_PLAYERS = [1, 1, 1, 1, 1, 1, 1, 0]
BOSS_PLAYERS = [0, 0, 0, 0, 0, 0, 0, 1]
FOURTH_TOWN_PLAYERS = [0, 1, 1, 1, 1, 1, 1, 1]
MEGA_TOWN_PLAYERS = [0, 1, 1, 1, 1, 1, 1, 1]
##################################################

HUMAN_LVL1_CREATURES = round(HUMAN_LVL7_CREATURES * 25)
HUMAN_LVL2_CREATURES = round(HUMAN_LVL7_CREATURES * 20)
HUMAN_LVL3_CREATURES = round(HUMAN_LVL7_CREATURES * 15)
HUMAN_LVL4_CREATURES = round(HUMAN_LVL7_CREATURES * 10)
HUMAN_LVL5_CREATURES = round(HUMAN_LVL7_CREATURES * 6)
HUMAN_LVL6_CREATURES = round(HUMAN_LVL7_CREATURES * 3)

AI_LVL1_CREATURES = round(AI_LVL7_CREATURES * 25)
AI_LVL2_CREATURES = round(AI_LVL7_CREATURES * 20)
AI_LVL3_CREATURES = round(AI_LVL7_CREATURES * 15)
AI_LVL4_CREATURES = round(AI_LVL7_CREATURES * 10)
AI_LVL5_CREATURES = round(AI_LVL7_CREATURES * 6)
AI_LVL6_CREATURES = round(AI_LVL7_CREATURES * 3)

BOSS_LVL1_CREATURES = round(BOSS_LVL7_CREATURES * 25)
BOSS_LVL2_CREATURES = round(BOSS_LVL7_CREATURES * 20)
BOSS_LVL3_CREATURES = round(BOSS_LVL7_CREATURES * 15)
BOSS_LVL4_CREATURES = round(BOSS_LVL7_CREATURES * 10)
BOSS_LVL5_CREATURES = round(BOSS_LVL7_CREATURES * 6)
BOSS_LVL6_CREATURES = round(BOSS_LVL7_CREATURES * 3)

FOURTH_TOWN_LVL1_CREATURES = round(FOURTH_TOWN_LVL7_CREATURES * 25)
FOURTH_TOWN_LVL2_CREATURES = round(FOURTH_TOWN_LVL7_CREATURES * 20)
FOURTH_TOWN_LVL3_CREATURES = round(FOURTH_TOWN_LVL7_CREATURES * 15)
FOURTH_TOWN_LVL4_CREATURES = round(FOURTH_TOWN_LVL7_CREATURES * 10)
FOURTH_TOWN_LVL5_CREATURES = round(FOURTH_TOWN_LVL7_CREATURES * 6)
FOURTH_TOWN_LVL6_CREATURES = round(FOURTH_TOWN_LVL7_CREATURES * 3)

MEGA_TOWN_LVL1_CREATURES = round(MEGA_TOWN_LVL7_CREATURES * 25)
MEGA_TOWN_LVL2_CREATURES = round(MEGA_TOWN_LVL7_CREATURES * 20)
MEGA_TOWN_LVL3_CREATURES = round(MEGA_TOWN_LVL7_CREATURES * 15)
MEGA_TOWN_LVL4_CREATURES = round(MEGA_TOWN_LVL7_CREATURES * 10)
MEGA_TOWN_LVL5_CREATURES = round(MEGA_TOWN_LVL7_CREATURES * 6)
MEGA_TOWN_LVL6_CREATURES = round(MEGA_TOWN_LVL7_CREATURES * 3)


def enable_spells() -> None:
    xprint(type=TextType.ACTION, text="Enabling spell research and all spells in all towns…")
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS:
            obj["spell_research"] = True
            for i in range(len(obj["spells_must_appear"])):
                obj["spells_must_appear"][i] = 0
            for i in range(len(obj["spells_cant_appear"])):
                obj["spells_cant_appear"][i] = 0
    xprint(type=TextType.DONE)


def enable_buildings() -> None:
    xprint(type=TextType.ACTION, text="Enabling all buildings in all towns…")
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS:
            if "buildings_disabled" in obj:
                for i in range(len(obj["buildings_disabled"])):
                    obj["buildings_disabled"][i] = 0
            else:
                obj["has_fort"] = True
    xprint(type=TextType.DONE)


def create_events() -> None:
    def _get_event_dict(
        name: str,
        players: list,
        human: bool,
        ai: bool,
        first: int,
        subsequent: int,
        hota_level7b: int,
        hota_special: list,
        buildings: list,
        creatures: list,
    ) -> dict:
        return {
            "name": name,
            "message": "",
            "resources": [0] * 7,
            "apply_to": players,
            "apply_human": human,
            "apply_ai": ai,
            "first_occurence": first,
            "subsequent_occurences": subsequent,
            "trash_bytes": b"\x00" * 16,
            "allowed_difficulties": 31,
            "eventType": 0,
            "hotaLevel7b": hota_level7b,
            "hotaAmount": 48,
            "hotaSpecial": hota_special,
            "apply_neutral_towns": False,
            "buildings": buildings,
            "creatures": creatures,
            "end_trash": b"\x00" * 4,
        }

    xprint(type=TextType.ACTION, text="Configuring town events…")
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["owner"] != players.ID.Neutral:
            # Remove any existing events with the same name
            obj["town_events"] = [e for e in obj["town_events"] if e["name"] != HUMAN_EVENT_NAME]
            obj["town_events"] = [e for e in obj["town_events"] if e["name"] != AI_EVENT_NAME]
            obj["town_events"] = [e for e in obj["town_events"] if e["name"] != BOSS_EVENT_NAME]
            # Create human event
            if HUMAN_PLAYERS[obj["owner"]]:
                human_event = _get_event_dict(
                    name=HUMAN_EVENT_NAME,
                    players=HUMAN_PLAYERS,
                    human=True,
                    ai=False,
                    first=7,
                    subsequent=7,
                    hota_level7b=HUMAN_LVL7_CREATURES if obj["sub_id"] == objects.SubID.Town.Factory else 0,
                    hota_special=[0] * 6,
                    buildings=[0] * 48,
                    creatures=[
                        HUMAN_LVL1_CREATURES,
                        HUMAN_LVL2_CREATURES,
                        HUMAN_LVL3_CREATURES,
                        HUMAN_LVL4_CREATURES,
                        HUMAN_LVL5_CREATURES,
                        HUMAN_LVL6_CREATURES,
                        HUMAN_LVL7_CREATURES,
                    ],
                )
                obj["town_events"].extend([human_event])
            # Create AI event
            if AI_PLAYERS[obj["owner"]] and not BOSS_PLAYERS[obj["owner"]]:
                ai_event = _get_event_dict(
                    name=AI_EVENT_NAME,
                    players=AI_PLAYERS,
                    human=False,
                    ai=True,
                    first=0,
                    subsequent=7,
                    hota_level7b=AI_LVL7_CREATURES if obj["sub_id"] == objects.SubID.Town.Factory else 0,
                    hota_special=[255, 255, 255, 255, 255, 15],
                    buildings=[0 if i in (2, 17) or 41 <= i <= 47 else 1 for i in range(48)],
                    creatures=[
                        AI_LVL1_CREATURES,
                        AI_LVL2_CREATURES,
                        AI_LVL3_CREATURES,
                        AI_LVL4_CREATURES,
                        AI_LVL5_CREATURES,
                        AI_LVL6_CREATURES,
                        AI_LVL7_CREATURES,
                    ],
                )
                obj["town_events"].extend([ai_event])
            # Create boss event
            # if BOSS_PLAYERS[obj["owner"]]:
            #     boss_event = _get_event_dict(
            #         name=BOSS_EVENT_NAME,
            #         players=BOSS_PLAYERS,
            #         human=False,
            #         ai=True,
            #         first=0,
            #         subsequent=7,
            #         hota_level7b=BOSS_LVL7_CREATURES if obj["sub_id"] == Town.Factory else 0,
            #         hota_special=[255, 255, 255, 255, 255, 15],
            #         buildings=[0 if i in (2, 17) or 41 <= i <= 47 else 1 for i in range(48)],
            #         creatures=[
            #             BOSS_LVL1_CREATURES,
            #             BOSS_LVL2_CREATURES,
            #             BOSS_LVL3_CREATURES,
            #             BOSS_LVL4_CREATURES,
            #             BOSS_LVL5_CREATURES,
            #             BOSS_LVL6_CREATURES,
            #             BOSS_LVL7_CREATURES,
            #         ],
            #     )
            #     obj["town_events"].extend([boss_event])
    xprint(type=TextType.DONE)


def create_fourth_town_events() -> None:
    xprint(type=TextType.ACTION, text="Configuring 4th-town events…")
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["name"] in {
            "Knight's Niche",
            "Grim Galley",
            "Feather Lodge",
            "Hacksaw Hole",
            "Skull Temple",
            "Pirate Piazza",
            "Mage's Retreat",
        }:
            # Remove any existing events with the same name
            obj["town_events"] = [e for e in obj["town_events"] if e["name"] != FOURTH_TOWN_EVENT_NAME]
            # Create event
            fourth_town_event = {
                "name": FOURTH_TOWN_EVENT_NAME,
                "message": "",
                "resources": [10, 5, 10, 5, 5, 5, 25000],
                "apply_to": FOURTH_TOWN_PLAYERS,
                "apply_human": True,
                "apply_ai": True,
                "first_occurence": 0,
                "subsequent_occurences": 7,
                "trash_bytes": b"\x00" * 16,
                "allowed_difficulties": 31,
                "eventType": 0,
                "hotaLevel7b": FOURTH_TOWN_LVL7_CREATURES if obj["sub_id"] == objects.SubID.Town.Factory else 0,
                "hotaAmount": 48,
                "hotaSpecial": [0] * 6,
                "apply_neutral_towns": True,
                "buildings": [0] * 48,
                "creatures": [
                    FOURTH_TOWN_LVL1_CREATURES,
                    FOURTH_TOWN_LVL2_CREATURES,
                    FOURTH_TOWN_LVL3_CREATURES,
                    FOURTH_TOWN_LVL4_CREATURES,
                    FOURTH_TOWN_LVL5_CREATURES,
                    FOURTH_TOWN_LVL6_CREATURES,
                    FOURTH_TOWN_LVL7_CREATURES,
                ],
                "end_trash": b"\x00" * 4,
            }
            obj["town_events"].extend([fourth_town_event])
    xprint(type=TextType.DONE)


def create_mega_town_events() -> None:
    xprint(type=TextType.ACTION, text="Configuring mega-town events…")
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["name"] in {
            "The Vault",
            "Hag's Hollow",
            "Cragspire",
            "Grandview",
        }:
            # Remove any existing events with the same name
            obj["town_events"] = [e for e in obj["town_events"] if e["name"] != MEGA_TOWN_EVENT_NAME]
            # Create event
            mega_town_event = {
                "name": MEGA_TOWN_EVENT_NAME,
                "message": "",
                "resources": [20, 10, 20, 10, 10, 10, 50000],
                "apply_to": MEGA_TOWN_PLAYERS,
                "apply_human": True,
                "apply_ai": True,
                "first_occurence": 0,
                "subsequent_occurences": 7,
                "trash_bytes": b"\x00" * 16,
                "allowed_difficulties": 31,
                "eventType": 0,
                "hotaLevel7b": MEGA_TOWN_LVL7_CREATURES if obj["sub_id"] == objects.SubID.Town.Factory else 0,
                "hotaAmount": 48,
                "hotaSpecial": [0] * 6,
                "apply_neutral_towns": True,
                "buildings": [0] * 48,
                "creatures": [
                    MEGA_TOWN_LVL1_CREATURES,
                    MEGA_TOWN_LVL2_CREATURES,
                    MEGA_TOWN_LVL3_CREATURES,
                    MEGA_TOWN_LVL4_CREATURES,
                    MEGA_TOWN_LVL5_CREATURES,
                    MEGA_TOWN_LVL6_CREATURES,
                    MEGA_TOWN_LVL7_CREATURES,
                ],
                "end_trash": b"\x00" * 4,
            }
            obj["town_events"].extend([mega_town_event])
    xprint(type=TextType.DONE)


def change_ai_events() -> None:
    xprint(type=TextType.ACTION, text="Adding Humans to AI-only town events…")
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS:
            for event in obj["town_events"]:
                if event["apply_ai"] and event["apply_to"] == [1] * 8:
                    event["apply_human"] = True
    xprint(type=TextType.DONE)


def copy_events() -> None:
    xprint(type=TextType.ACTION, text="Copying events from source town to target towns…")
    events = []
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["town_events"] and obj["town_events"][0]["message"] == "source":
            for event in obj["town_events"]:
                event["message"] = ""
                events.append(event)
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["town_events"] and obj["town_events"][0]["message"] == "target":
            obj["town_events"] = events.copy()
            obj["town_events"][0]["message"] == ""
    xprint(type=TextType.DONE)


def copy_buildings() -> None:
    xprint(type=TextType.ACTION, text="Copying buildings from source town to target towns…")
    buildings = {}
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["name"] == "Watchfield":
            buildings["has_fort"] = obj["has_fort"]
            buildings["built"] = obj["buildings_built"]
            buildings["disabled"] = obj["buildings_disabled"]
            buildings["special"] = obj["buildings_special"]
    for obj in map_data["object_data"]:
        if obj["id"] in groups.TOWNS and obj["name"] in {"Wayside", "Brenwick Hill"}:
            obj["has_custom_buildings"] = True
            obj["has_fort"] = buildings["has_fort"]
            obj["buildings_built"] = buildings["built"]
            obj["buildings_disabled"] = buildings["disabled"]
            obj["buildings_special"] = buildings["special"]
    xprint(type=TextType.DONE)


def set_guards() -> None:
    xprint(type=TextType.ACTION, text="Setting garrison troops in target towns…")

    PLAYERS = {
        players.ID.Blue,
        players.ID.Tan,
        players.ID.Green,
        players.ID.Orange,
        players.ID.Purple,
        players.ID.Teal,
        players.ID.Pink,
    }

    GUARD_IDS = {
        objects.SubID.Town.Castle: [
            creatures.ID.Zealot,
            creatures.ID.Royal_Griffin,
            creatures.ID.Champion,
            creatures.ID.Archangel,
            creatures.ID.Crusader,
            creatures.ID.Halberdier,
            creatures.ID.Marksman,
        ],
        objects.SubID.Town.Rampart: [
            creatures.ID.Grand_Elf,
            creatures.ID.Dendroid_Soldier,
            creatures.ID.War_Unicorn,
            creatures.ID.Gold_Dragon,
            creatures.ID.Silver_Pegasus,
            creatures.ID.Battle_Dwarf,
            creatures.ID.Centaur_Captain,
        ],
        objects.SubID.Town.Tower: [
            creatures.ID.Titan,
            creatures.ID.Iron_Golem,
            creatures.ID.Naga_Queen,
            creatures.ID.Master_Gremlin,
            creatures.ID.Master_Genie,
            creatures.ID.Obsidian_Gargoyle,
            creatures.ID.Arch_Mage,
        ],
        objects.SubID.Town.Necropolis: [
            creatures.ID.Power_Lich,
            creatures.ID.Wraith,
            creatures.ID.Dread_Knight,
            creatures.ID.Ghost_Dragon,
            creatures.ID.Vampire_Lord,
            creatures.ID.Zombie,
            creatures.ID.Skeleton_Warrior,
        ],
        objects.SubID.Town.Dungeon: [
            creatures.ID.Medusa_Queen,
            creatures.ID.Harpy_Hag,
            creatures.ID.Scorpicore,
            creatures.ID.Black_Dragon,
            creatures.ID.Minotaur_King,
            creatures.ID.Infernal_Troglodyte,
            creatures.ID.Evil_Eye,
        ],
        objects.SubID.Town.Stronghold: [
            creatures.ID.Cyclops_King,
            creatures.ID.Wolf_Raider,
            creatures.ID.Thunderbird,
            creatures.ID.Ancient_Behemoth,
            creatures.ID.Ogre_Mage,
            creatures.ID.Hobgoblin,
            creatures.ID.Orc_Chieftain,
        ],
        objects.SubID.Town.Fortress: [
            creatures.ID.Lizard_Warrior,
            creatures.ID.Greater_Basilisk,
            creatures.ID.Wyvern_Monarch,
            creatures.ID.Chaos_Hydra,
            creatures.ID.Mighty_Gorgon,
            creatures.ID.Dragon_Fly,
            creatures.ID.Gnoll_Marauder,
        ],
        objects.SubID.Town.Conflux: [
            creatures.ID.Ice_Elemental,
            creatures.ID.Energy_Elemental,
            creatures.ID.Magic_Elemental,
            creatures.ID.Phoenix,
            creatures.ID.Magma_Elemental,
            creatures.ID.Sprite,
            creatures.ID.Storm_Elemental,
        ],
        objects.SubID.Town.Cove: [
            creatures.ID.Zealot,
            creatures.ID.Seaman,
            creatures.ID.Nix_Warrior,
            creatures.ID.Haspid,
            creatures.ID.Ayssid,
            creatures.ID.Oceanid,
            creatures.ID.Marksman,
        ],
        objects.SubID.Town.Factory: [
            creatures.ID.Bounty_Hunter,
            creatures.ID.Sentinel_Automaton,
            creatures.ID.Crimson_Couatl,
            creatures.ID.Olgoi_Khorkhoi,
            creatures.ID.Juggernaut,
            creatures.ID.Bellwether_Armadillo,
            creatures.ID.Halfling_Grenadier,
        ],
        objects.SubID.Town.Bulwark: [
            creatures.ID.Great_Shaman,
            creatures.ID.Argali,
            creatures.ID.War_Mammoth,
            creatures.ID.Jotunn_Warlord,
            creatures.ID.Yeti_Runemaster,
            creatures.ID.Kobold_Foreman,
            creatures.ID.Steel_Elf,
        ],
    }

    GUARD_AMOUNTS = {
        "I": None,
        "II": {
            "player": [300, 250, 200, 150, 100, 40, 15],
            "neutral": [2000, 1500, 1000, 500, 300, 200, 100],
        },
        "III": {
            "player": [750, 625, 500, 375, 250, 150, 50],
            "neutral": None,
        },
        "IV": {
            "player": [3000, 2500, 2000, 1500, 1000, 500, 250],
            "neutral": None,
        },
    }

    def _build_guard_list(town_type, amounts: list[int]) -> list[dict]:
        creature_ids = GUARD_IDS[town_type]
        level_classes = [
            creatures.Level1,
            creatures.Level2,
            creatures.Level3,
            creatures.Level4,
            creatures.Level5,
            creatures.Level6,
            creatures.Level7,
        ]
        garrison = []
        for cid in creature_ids:
            amount = 0
            for level_idx, level_class in enumerate(level_classes):
                if cid in [m.value for m in level_class]:
                    amount = amounts[level_idx]
                    break
            garrison.append({"id": cid, "amount": amount})
        return garrison

    modified_count = 0

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Town and obj["owner"] == players.ID.Neutral:
            guards_config = GUARD_AMOUNTS[obj["zone_type"]]
            zone_owner_type = "player" if obj["zone_owner"] in PLAYERS else "neutral"
            amounts = guards_config[zone_owner_type]
            if amounts is not None:
                obj["garrison_guards"] = _build_guard_list(obj["sub_id"], amounts)
                modified_count += 1
                xprint(type=TextType.INFO, text=obj["garrison_guards"])
                xprint()

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, align=TextAlign.CENTER, text=f"Updated {modified_count} towns.")

    wait_for_keypress()
