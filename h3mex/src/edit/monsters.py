import random  # noqa: F401

from src.common import TextType, map_data
from src.defs import creatures, groups, objects, players
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def set_random_monsters() -> None:
    xprint(type=TextType.ACTION, text="Setting non-level-specific random monsters to random monsters 1-7…")

    # Find each first level-specific Random Monster to get its def_id
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Random_Monster_1:
            # def_id1 = obj["def_id"]
            continue
        if obj["id"] == objects.ID.Random_Monster_2:
            # def_id2 = obj["def_id"]
            continue
        if obj["id"] == objects.ID.Random_Monster_3:
            def_id3 = obj["def_id"]
            continue
        if obj["id"] == objects.ID.Random_Monster_4:
            def_id4 = obj["def_id"]
            continue
        if obj["id"] == objects.ID.Random_Monster_5:
            def_id5 = obj["def_id"]
            continue
        if obj["id"] == objects.ID.Random_Monster_6:
            def_id6 = obj["def_id"]
            continue
        if obj["id"] == objects.ID.Random_Monster_7:
            def_id7 = obj["def_id"]
            continue

    count = 0

    # Update Random Monster 1-7 objects
    for obj in map_data["object_data"]:
        if (
            obj["id"] == objects.ID.Random_Monster
            and obj["zone_type"] in {"III", "IV"}
            and obj["zone_owner"] in {0, 255}
        ):
            count += 1
            obj["sub_id"] = 0
            if obj["zone_type"] == "III":
                rand = random.randint(3, 7)
            elif obj["zone_type"] == "IV":
                rand = random.randint(5, 7)
            # if rand == 1:
            #     obj["def_id"] = def_id1
            #     obj["id"] = objects.ID.Random_Monster_1
            #     obj["type"] = obj["subtype"] = f"Random Monster {rand}"
            # if rand == 2:
            #     obj["def_id"] = def_id2
            #     obj["id"] = objects.ID.Random_Monster_2
            #     obj["type"] = obj["subtype"] = f"Random Monster {rand}"
            if rand == 3:
                obj["def_id"] = def_id3
                obj["id"] = objects.ID.Random_Monster_3
                obj["type"] = obj["subtype"] = f"Random Monster {rand}"
            if rand == 4:
                obj["def_id"] = def_id4
                obj["id"] = objects.ID.Random_Monster_4
                obj["type"] = obj["subtype"] = f"Random Monster {rand}"
            if rand == 5:
                obj["def_id"] = def_id5
                obj["id"] = objects.ID.Random_Monster_5
                obj["type"] = obj["subtype"] = f"Random Monster {rand}"
            if rand == 6:
                obj["def_id"] = def_id6
                obj["id"] = objects.ID.Random_Monster_6
                obj["type"] = obj["subtype"] = f"Random Monster {rand}"
            if rand == 7:
                obj["def_id"] = def_id7
                obj["id"] = objects.ID.Random_Monster_7
                obj["type"] = obj["subtype"] = f"Random Monster {rand}"

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def set_monster_quantities() -> None:
    xprint(type=TextType.ACTION, text="Setting monster values…")

    # PLAYER_ZONE_VALUE_RANGES = {
    #     "I": (2000, 25000),
    #     "II": (50000, 200000),
    #     "III": (300000, 500000),
    #     "IV": (850000, 999999),
    # }

    # NEUTRAL_ZONE_VALUE_RANGES = {
    #     "I": (250000, 500000),
    #     "II": (750000, 999999),
    # }

    NEUTRAL_ZONE_III_QUANTITY_RANGES = {
        1: (3900, 4000),
        2: (3750, 4000),
        3: (3600, 4000),
        4: (3450, 4000),
        5: (3300, 4000),
        6: (3150, 4000),
        7: (3000, 4000),
    }

    NEUTRAL_ZONE_IV_QUANTITY_RANGES = {
        1: (3900, 4000),
        2: (3750, 4000),
        3: (3600, 4000),
        4: (3450, 4000),
        5: (3300, 4000),
        6: (3150, 4000),
        7: (3000, 4000),
    }

    random_monster_level_map = {
        objects.ID.Random_Monster_1: 1,
        objects.ID.Random_Monster_2: 2,
        objects.ID.Random_Monster_3: 3,
        objects.ID.Random_Monster_4: 4,
        objects.ID.Random_Monster_5: 5,
        objects.ID.Random_Monster_6: 6,
        objects.ID.Random_Monster_7: 7,
    }

    count = 0
    for obj in map_data["object_data"]:
        if obj["id"] in {*groups.MONSTERS} and obj["disposition"] != creatures.Disposition.Compliant:
            if obj["zone_owner"] not in {players.ID.Red, players.ID.Neutral}:
                # obj["ai_value"] = random.randint(*PLAYER_ZONE_VALUE_RANGES[obj["zone_type"]])
                pass
            elif obj["zone_owner"] == players.ID.Neutral:
                if obj["zone_type"] in {"I", "II"}:
                    # obj["ai_value"] = random.randint(*NEUTRAL_ZONE_VALUE_RANGES[obj["zone_type"]])
                    pass
                elif obj["zone_type"] in {"III", "IV"}:
                    count += 1
                    obj["is_value"] = False
                    obj["ai_value"] = 0
                    quantity_ranges = (
                        NEUTRAL_ZONE_III_QUANTITY_RANGES
                        if obj["zone_type"] == "III"
                        else NEUTRAL_ZONE_IV_QUANTITY_RANGES
                    )

                    if obj["id"] in groups.RANDOM_MONSTERS_LEVEL:
                        level = random_monster_level_map.get(obj["id"])
                        if level is not None:
                            obj["quantity"] = random.randint(*quantity_ranges[level])
                    elif obj["id"] == objects.ID.Monster:
                        level = None
                        if obj["sub_id"] in creatures.Level1:
                            level = 1
                        elif obj["sub_id"] in creatures.Level2:
                            level = 2
                        elif obj["sub_id"] in creatures.Level3:
                            level = 3
                        elif obj["sub_id"] in creatures.Level4:
                            level = 4
                        elif obj["sub_id"] in creatures.Level5:
                            level = 5
                        elif obj["sub_id"] in creatures.Level6:
                            level = 6
                        elif obj["sub_id"] in creatures.Level7:
                            level = 7
                        if level is not None:
                            obj["quantity"] = random.randint(*quantity_ranges[level])
            # count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def set_compliant_monster_values() -> None:
    xprint(type=TextType.ACTION, text="Setting compliant monster values…")

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj.get("id") == objects.ID.Monster
            and obj.get("zone_type") == "Player"
            and obj.get("disposition") == creatures.Disposition.Compliant
        ):

            match obj["ai_value"]:
                case 1000:
                    obj["ai_value"] = 3000
                case 1500:
                    obj["ai_value"] = 10000
                case 2000:
                    obj["ai_value"] = 15000
                case 2500:
                    obj["ai_value"] = 25000
                case 10000:
                    obj["ai_value"] = 100000

            count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def set_monster_flee_values() -> None:
    xprint(type=TextType.ACTION, text="Setting monster flee values…")

    count = 0
    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Monster:
            if obj["disposition"] != creatures.Disposition.Compliant and not obj["monster_never_flees"]:
                obj["monster_never_flees"] = True
                count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def make_compliant_monsters_not_grow() -> None:
    xprint(type=TextType.ACTION, text="Making compliant monsters not grow…")

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj["id"] == objects.ID.Monster
            and obj["disposition"] == creatures.Disposition.Compliant
            and not obj["quantity_does_not_grow"]
        ):
            obj["quantity_does_not_grow"] = True
            count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def make_non_compliant_monsters_grow() -> None:
    xprint(type=TextType.ACTION, text="Making non-compliant monsters grow…")

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj["id"] == objects.ID.Monster
            and obj["disposition"] != creatures.Disposition.Compliant
            and obj["quantity_does_not_grow"]
        ):
            obj["quantity_does_not_grow"] = False
            count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()


def increase_creature_stashes() -> None:
    xprint(type=TextType.ACTION, text="Increasing creature stashes…")
    xprint()

    count = 0
    for obj in map_data["object_data"]:
        if (
            obj["id"] == objects.ID.Monster
            and obj["disposition"] == creatures.Disposition.Compliant
            and obj["zone_owner"] == players.ID.Neutral
            and obj["zone_type"] in {"I", "II"}
            and not obj["is_value"]
            and obj["sub_id"]
            not in {
                *creatures.Stronghold,
                *creatures.Fortress,
                *creatures.Conflux,
                *creatures.Bulwark,
                *creatures.Neutral,
            }
        ):
            obj["quantity"] *= 2
            xprint(type=TextType.INFO, text=obj["subtype"])
            count += 1

    xprint()
    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()
