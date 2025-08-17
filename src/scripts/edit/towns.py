import data.objects as objects
from data.players import Players

from ...common import DONE, Text, map_data, xprint

TOWN_IDS = [objects.ID.Town, objects.ID.Random_Town]

HUMAN_EVENT_NAME = "[Human Bonus]"
AI_EVENT_NAME = "[AI Bonus]"
BOSS_EVENT_NAME = "[Boss Bonus]"

##################################################
# Set lvl7 creature bonus amounts (max 666 each)
HUMAN_LVL7_CREATURES = 10
AI_LVL7_CREATURES = 20
BOSS_LVL7_CREATURES = 50

# Set player colors (customize AI if necessary)
HUMAN_PLAYERS = [1, 1, 1, 1, 1, 1, 1, 0]
AI_PLAYERS = [1, 1, 1, 1, 1, 1, 1, 1]
BOSS_PLAYERS = [0, 0, 0, 0, 0, 0, 0, 1]
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


def modify(events: bool = False) -> None:
    if not events:
        msg = "Enabling spell research, spells, and buildings for all towns..."
    else:
        msg = "Enabling spell research, spells, buildings, and events for all towns..."
    xprint(type=Text.ACTION, text=msg)

    for obj in map_data["object_data"]:
        if obj["id"] in TOWN_IDS:
            # Enable spell research
            obj["spell_research"] = True

            # Enable all spells
            for i in range(len(obj["spells_must_appear"])):
                obj["spells_must_appear"][i] = 0
            for i in range(len(obj["spells_cant_appear"])):
                obj["spells_cant_appear"][i] = 0

            # Enable all buildings
            if "buildings_disabled" in obj:
                for i in range(len(obj["buildings_disabled"])):
                    obj["buildings_disabled"][i] = 0
            else:
                obj["has_fort"] = True

            # Add events
            if events and obj["owner"] != Players.Neutral:
                # Remove existing events
                obj["events"] = [e for e in obj["events"] if e["name"] != HUMAN_EVENT_NAME]
                obj["events"] = [e for e in obj["events"] if e["name"] != AI_EVENT_NAME]
                obj["events"] = [e for e in obj["events"] if e["name"] != BOSS_EVENT_NAME]
                # Add lines for map-specific events to remove permanently like this:
                # obj["events"] = [e for e in obj["events"] if e["name"] != "AI support"]

                # Create human event
                if HUMAN_PLAYERS[obj["owner"]]:
                    human_event = _get_event(
                        name=HUMAN_EVENT_NAME,
                        players=HUMAN_PLAYERS,
                        human=True,
                        ai=False,
                        lvl7b_creatures=HUMAN_LVL7_CREATURES if obj["owner"] == objects.Town.Factory else 0,
                        random_buildings=[0] * 48,
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
                    obj["events"].extend([human_event])

                # Create AI event
                if AI_PLAYERS[obj["owner"]] and not BOSS_PLAYERS[obj["owner"]]:
                    ai_event = _get_event(
                        name=AI_EVENT_NAME,
                        players=AI_PLAYERS,
                        human=False,
                        ai=True,
                        lvl7b_creatures=AI_LVL7_CREATURES if obj["owner"] == objects.Town.Factory else 0,
                        random_buildings=[1] * 48,
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
                    obj["events"].extend([ai_event])

                # Create boss event
                if BOSS_PLAYERS[obj["owner"]]:
                    boss_event = _get_event(
                        name=BOSS_EVENT_NAME,
                        players=BOSS_PLAYERS,
                        human=False,
                        ai=True,
                        lvl7b_creatures=BOSS_LVL7_CREATURES if obj["owner"] == objects.Town.Factory else 0,
                        random_buildings=[1] * 48,
                        buildings=[0 if i in (2, 17) or 41 <= i <= 47 else 1 for i in range(48)],
                        creatures=[
                            BOSS_LVL1_CREATURES,
                            BOSS_LVL2_CREATURES,
                            BOSS_LVL3_CREATURES,
                            BOSS_LVL4_CREATURES,
                            BOSS_LVL5_CREATURES,
                            BOSS_LVL6_CREATURES,
                            BOSS_LVL7_CREATURES,
                        ],
                    )
                    obj["events"].extend([boss_event])

    xprint(type=Text.SPECIAL, text=DONE)


def _modify_towns(events: bool = False) -> None:
    if not events:
        msg = "Enabling spell research, spells, and buildings for all towns..."
    else:
        msg = "Enabling spell research, spells, buildings, and events for all towns..."
    xprint(type=Text.ACTION, text=msg)

    for obj in map_data["object_data"]:
        if obj["id"] in TOWN_IDS:
            # Enable spell research
            obj["spell_research"] = True

            # Enable all spells
            for i in range(len(obj["spells_must_appear"])):
                obj["spells_must_appear"][i] = 0
            for i in range(len(obj["spells_cant_appear"])):
                obj["spells_cant_appear"][i] = 0

            # Enable all buildings
            if "buildings_disabled" in obj:
                for i in range(len(obj["buildings_disabled"])):
                    obj["buildings_disabled"][i] = 0
            else:
                obj["has_fort"] = True

            # Add events
            if events and obj["owner"] != Players.Neutral:
                # Remove existing events
                obj["events"] = [e for e in obj["events"] if e["name"] != HUMAN_EVENT_NAME]
                obj["events"] = [e for e in obj["events"] if e["name"] != AI_EVENT_NAME]
                obj["events"] = [e for e in obj["events"] if e["name"] != BOSS_EVENT_NAME]
                # Add lines for map-specific events to remove permanently like this:
                # obj["events"] = [e for e in obj["events"] if e["name"] != "AI support"]

                # Create human event
                if HUMAN_PLAYERS[obj["owner"]]:
                    human_event = _get_event(
                        name=HUMAN_EVENT_NAME,
                        players=HUMAN_PLAYERS,
                        human=True,
                        ai=False,
                        lvl7b_creatures=HUMAN_LVL7_CREATURES if obj["owner"] == objects.Town.Factory else 0,
                        random_buildings=[0] * 48,
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
                    obj["events"].extend([human_event])

                # Create AI event
                if AI_PLAYERS[obj["owner"]] and not BOSS_PLAYERS[obj["owner"]]:
                    ai_event = _get_event(
                        name=AI_EVENT_NAME,
                        players=AI_PLAYERS,
                        human=False,
                        ai=True,
                        lvl7b_creatures=AI_LVL7_CREATURES if obj["owner"] == objects.Town.Factory else 0,
                        random_buildings=[1] * 48,
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
                    obj["events"].extend([ai_event])

                # Create boss event
                if BOSS_PLAYERS[obj["owner"]]:
                    boss_event = _get_event(
                        name=BOSS_EVENT_NAME,
                        players=BOSS_PLAYERS,
                        human=False,
                        ai=True,
                        lvl7b_creatures=BOSS_LVL7_CREATURES if obj["owner"] == objects.Town.Factory else 0,
                        random_buildings=[1] * 48,
                        buildings=[0 if i in (2, 17) or 41 <= i <= 47 else 1 for i in range(48)],
                        creatures=[
                            BOSS_LVL1_CREATURES,
                            BOSS_LVL2_CREATURES,
                            BOSS_LVL3_CREATURES,
                            BOSS_LVL4_CREATURES,
                            BOSS_LVL5_CREATURES,
                            BOSS_LVL6_CREATURES,
                            BOSS_LVL7_CREATURES,
                        ],
                    )
                    obj["events"].extend([boss_event])

    xprint(type=Text.SPECIAL, text=DONE)


def _get_event(
    name: str,
    players: list,
    human: bool,
    ai: bool,
    lvl7b_creatures: int,
    random_buildings: list,
    buildings: list,
    creatures: list,
) -> dict:
    return {
        "isTown": True,
        "name": name,
        "message": "",
        "resources": [0] * 7,
        "apply_to": players,
        "apply_human": human,
        "apply_ai": ai,
        "first_occurence": 0,
        "subsequent_occurences": 7,
        "trash_bytes": b"\x00" * 16,
        "allowed_difficulties": 31,
        "hota_lvl7b_amount": lvl7b_creatures,
        "hota_unknown_constant": 44,
        "hota_special": random_buildings,
        "apply_neutral_towns": False,
        "buildings": buildings,
        "creatures": creatures,
        "end_trash": b"\x00" * 4,
    }
