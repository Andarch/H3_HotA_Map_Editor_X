import data.objects as objects

from ...common import DONE, Text, map_data, xprint

TOWNS = [objects.ID.Town, objects.ID.Random_Town]

PLAYER_LVL7_AMOUNT = 0  # Note: Max of 666
AI_LVL7_AMOUNT = 0  # Note: Max of 666


def modify_towns(events: bool = False) -> None:
    if not events:
        msg = "Enabling spell research, spells, and buildings for all towns..."
    else:
        msg = "Enabling spell research, spells, buildings, and events for all towns..."
    xprint(type=Text.ACTION, text=msg)

    for obj in map_data["object_data"]:
        if obj["id"] in TOWNS:
            # Fix blank names
            if obj["name"] == "":
                obj["has_name"] = False

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

            # If events is true, add events
            if events and obj["owner"] != 255:
                # Remove existing events
                obj["events"] = [e for e in obj["events"] if e["name"] != "Player Bonus [H3HOTAMEX]"]
                obj["events"] = [e for e in obj["events"] if e["name"] != "AI Bonus [H3HOTAMEX]"]

                player_event = {
                    "isTown": True,
                    "name": "Player Bonus [H3HOTAMEX]",
                    "message": "",
                    "resources": [0] * 7,
                    "apply_to": [1, 1, 1, 1, 1, 1, 1, 0],
                    "apply_human": True,
                    "apply_ai": False,
                    "first_occurence": 0,
                    "subsequent_occurences": 7,
                    "trash_bytes": b"\x00" * 16,
                    "allowed_difficulties": 31,
                    "hota_lvl7b_amount": PLAYER_LVL7_AMOUNT,
                    "hota_unknown_constant": 44,
                    "hota_special": [0] * 48,
                    "apply_neutral_towns": False,
                    "buildings": [0] * 48,
                    "creatures": [
                        round(PLAYER_LVL7_AMOUNT * 15),
                        round(PLAYER_LVL7_AMOUNT * 12.5),
                        round(PLAYER_LVL7_AMOUNT * 10),
                        round(PLAYER_LVL7_AMOUNT * 7.5),
                        round(PLAYER_LVL7_AMOUNT * 5),
                        round(PLAYER_LVL7_AMOUNT * 2.5),
                        PLAYER_LVL7_AMOUNT,
                    ],
                    "end_trash": b"\x00" * 4,
                }
                ai_event = {
                    "isTown": True,
                    "name": "AI Bonus [H3HOTAMEX]",
                    "message": "",
                    "resources": [0] * 7,
                    "apply_to": [0, 0, 0, 0, 0, 0, 0, 1],
                    "apply_human": False,
                    "apply_ai": True,
                    "first_occurence": 0,
                    "subsequent_occurences": 7,
                    "trash_bytes": b"\x00" * 16,
                    "allowed_difficulties": 31,
                    "hota_lvl7b_amount": AI_LVL7_AMOUNT,
                    "hota_unknown_constant": 44,
                    "hota_special": [0] * 48,
                    "apply_neutral_towns": False,
                    "buildings": [0] * 48,
                    "creatures": [
                        round(AI_LVL7_AMOUNT * 15),
                        round(AI_LVL7_AMOUNT * 12.5),
                        round(AI_LVL7_AMOUNT * 10),
                        round(AI_LVL7_AMOUNT * 7.5),
                        round(AI_LVL7_AMOUNT * 5),
                        round(AI_LVL7_AMOUNT * 2.5),
                        AI_LVL7_AMOUNT,
                    ],
                    "end_trash": b"\x00" * 4,
                }

                obj["events"].extend([player_event, ai_event])

    xprint(type=Text.SPECIAL, text=DONE)
