import random

from src.common import TextType, map_data
from src.defs import creatures, objects, players
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def modify_pandoras():
    xprint(type=TextType.ACTION, text="Modifying Pandora's Boxes…")

    modified_count = 0

    target_boxes = {
        (154, 152, 1),
        (159, 154, 1),
        (157, 150, 1),
    }

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Pandoras_Box:
            modified = False

            # is_default = _check_default(obj)
            # if not is_default:
            #     continue
            # if obj["contents"]["Artifacts"] or obj["contents"]["Spells"]:
            #     continue
            # if obj["zone_type"] not in {"P1", "P2", "P3", "P4"}:
            #     continue

            # obj["has_common"] = 1
            # if not obj["contents"]["Spells"]:
            #     obj["guards"] = _get_random_guards(obj["zone_type"])
            #     modified = True
            # if not obj["contents"]["Spells"] and not obj["contents"]["Artifacts"]:
            #     obj["contents"] = _get_random_contents(obj["zone_type"])
            #     modified = True

            # Check if obj["coords"] is in target_boxes with [0] being x, [1] being y, and [2] being z
            if tuple(obj["coords"]) in target_boxes:
                obj["has_common"] = 1
                obj["guards"] = _get_random_guards(obj["zone_type"], obj["zone_owner"])
                obj["contents"] = _get_random_contents(obj["zone_type"], obj["zone_owner"])
                modified = True

            if modified:
                modified_count += 1

    xprint(type=TextType.DONE)
    xprint()
    xprint(type=TextType.INFO, text=f"Modified {modified_count} Pandora's Boxes.")
    wait_for_keypress()


def _check_default(obj):
    DEFAULT_PANDORAS_BOX = {
        "has_common": 0,
        "contents": {
            "Experience": 0,
            "Spell_Points": 0,
            "Morale": 0,
            "Luck": 0,
            "Resources": [0, 0, 0, 0, 0, 0, 0],
            "Primary_Skills": [0, 0, 0, 0],
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": 0,
        },
    }

    # Compare obj to DEFAULT_PANDORAS_BOX
    for key, value in DEFAULT_PANDORAS_BOX.items():
        if key == "contents":
            # Deep comparison for nested contents dictionary
            obj_contents = obj.get("contents", {})
            for content_key, content_value in value.items():
                if obj_contents.get(content_key) != content_value:
                    return False
        else:
            if obj.get(key) != value:
                return False

    return True


def _rand_enum_value(enum_cls):
    return random.choice(list(enum_cls)).value


def _get_random_guards(zone_type, zone_owner) -> list:
    if zone_type == "I" and zone_owner != players.ID.Red:
        return [
            {"id": _rand_enum_value(creatures.Level2), "amount": random.randint(50, 75)},
            {"id": _rand_enum_value(creatures.Level4), "amount": random.randint(20, 30)},
            {"id": _rand_enum_value(creatures.Level6), "amount": random.randint(5, 10)},
            {"id": _rand_enum_value(creatures.Level7), "amount": random.randint(2, 5)},
            {"id": _rand_enum_value(creatures.Level5), "amount": random.randint(10, 20)},
            {"id": _rand_enum_value(creatures.Level3), "amount": random.randint(30, 50)},
            {"id": _rand_enum_value(creatures.Level1), "amount": random.randint(75, 100)},
        ]
    elif zone_type == "II" and zone_owner != players.ID.Red:
        return [
            {"id": _rand_enum_value(creatures.Level2), "amount": random.randint(550, 700)},
            {"id": _rand_enum_value(creatures.Level4), "amount": random.randint(200, 350)},
            {"id": _rand_enum_value(creatures.Level6), "amount": random.randint(100, 150)},
            {"id": _rand_enum_value(creatures.Level7), "amount": random.randint(50, 75)},
            {"id": _rand_enum_value(creatures.Level5), "amount": random.randint(150, 200)},
            {"id": _rand_enum_value(creatures.Level3), "amount": random.randint(350, 550)},
            {"id": _rand_enum_value(creatures.Level1), "amount": random.randint(700, 900)},
        ]
    elif (zone_type == "III" and zone_owner != players.ID.Red) or (
        zone_type in {"I", "II"} and zone_owner == players.ID.Red
    ):
        return [
            {"id": _rand_enum_value(creatures.Level2), "amount": random.randint(2000, 2700)},
            {"id": _rand_enum_value(creatures.Level4), "amount": random.randint(800, 1300)},
            {"id": _rand_enum_value(creatures.Level6), "amount": random.randint(300, 600)},
            {"id": _rand_enum_value(creatures.Level7), "amount": random.randint(200, 350)},
            {"id": _rand_enum_value(creatures.Level5), "amount": random.randint(600, 800)},
            {"id": _rand_enum_value(creatures.Level3), "amount": random.randint(1400, 2000)},
            {"id": _rand_enum_value(creatures.Level1), "amount": random.randint(2700, 3400)},
        ]
    elif zone_type == "IV" or (zone_type == "III" and zone_owner == players.ID.Red):
        return [
            {"id": _rand_enum_value(creatures.Level2), "amount": random.randint(6000, 8000)},
            {"id": _rand_enum_value(creatures.Level4), "amount": random.randint(2400, 4000)},
            {"id": _rand_enum_value(creatures.Level6), "amount": random.randint(1000, 1600)},
            {"id": _rand_enum_value(creatures.Level7), "amount": random.randint(600, 1000)},
            {"id": _rand_enum_value(creatures.Level5), "amount": random.randint(1600, 2400)},
            {"id": _rand_enum_value(creatures.Level3), "amount": random.randint(4000, 6000)},
            {"id": _rand_enum_value(creatures.Level1), "amount": random.randint(8000, 9999)},
        ]


def _get_random_contents(zone_type, zone_owner) -> dict:
    if zone_type == "I" and zone_owner not in {players.ID.Red, players.ID.Neutral}:
        return {
            "Experience": 15000,
            "Spell_Points": 100,
            "Morale": 1,
            "Luck": 1,
            "Resources": [10, 10, 10, 10, 10, 10, 10000],
            "Primary_Skills": [1, 1, 1, 1],
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": 500,
        }
    if zone_type == "II" and zone_owner not in {players.ID.Red, players.ID.Neutral}:
        return {
            "Experience": 50000,
            "Spell_Points": 300,
            "Morale": 2,
            "Luck": 2,
            "Resources": [20, 20, 20, 20, 20, 20, 20000],
            "Primary_Skills": [1, 1, 1, 1],
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": 1000,
        }
    if zone_type == "III" and zone_owner not in {players.ID.Red, players.ID.Neutral}:
        return {
            "Experience": 100000,
            "Spell_Points": 500,
            "Morale": 3,
            "Luck": 3,
            "Resources": [30, 30, 30, 30, 30, 30, 30000],
            "Primary_Skills": [1, 1, 1, 1],
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": 1500,
        }
    if zone_type == "IV" and zone_owner not in {players.ID.Red, players.ID.Neutral}:
        return {
            "Experience": 200000,
            "Spell_Points": 1000,
            "Morale": 3,
            "Luck": 3,
            "Resources": [50, 50, 50, 50, 50, 50, 50000],
            "Primary_Skills": [2, 2, 2, 2],
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": 2000,
        }
    if zone_type == "I" and zone_owner == players.ID.Neutral:
        # Generate primary skills
        primary_skills = random.choice([[1, 1, 0, 0], [2, 0, 0, 0]])

        # Initialize values
        experience = 0
        spell_points = 0
        morale = 0
        luck = 0
        resources = [0, 0, 0, 0, 0, 0, 0]
        movement_points = 0

        # 25% chance for Experience boost
        if random.random() < 0.25:
            experience = random.choice([10000, 15000, 20000])

        # 25% chance for Spell_Points boost
        if random.random() < 0.25:
            spell_points = random.choice([100, 200, 300])

        # 25% chance for Morale boost
        if random.random() < 0.25:
            morale = random.choice([1, 2, 3])

        # 25% chance for Luck boost
        if random.random() < 0.25:
            luck = random.choice([1, 2, 3])

        # 25% chance for Resources boost
        if random.random() < 0.25:
            resources = [random.randint(10, 20) for _ in range(6)] + [random.randint(10, 20) * 100]

        # 25% chance for Movement_Points boost
        if random.random() < 0.25:
            movement_points = random.choice([500, 750, 1000])

        return {
            "Experience": experience,
            "Spell_Points": spell_points,
            "Morale": morale,
            "Luck": luck,
            "Resources": resources,
            "Primary_Skills": primary_skills,
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": movement_points,
        }
    elif zone_type == "II" and zone_owner == players.ID.Neutral:
        # Generate primary skills
        primary_skills = random.choice([[1, 1, 1, 0], [2, 1, 0, 0]])

        # Initialize values
        experience = 0
        spell_points = 0
        morale = 0
        luck = 0
        resources = [0, 0, 0, 0, 0, 0, 0]
        movement_points = 0

        # 25% chance for Experience boost
        if random.random() < 0.25:
            experience = random.choice([40000, 55000, 70000])

        # 25% chance for Spell_Points boost
        if random.random() < 0.25:
            spell_points = random.choice([400, 500, 600])

        # 25% chance for Morale boost
        if random.random() < 0.25:
            morale = random.choice([1, 2, 3])

        # 25% chance for Luck boost
        if random.random() < 0.25:
            luck = random.choice([1, 2, 3])

        # 25% chance for Resources boost
        if random.random() < 0.25:
            resources = [random.randint(40, 70) for _ in range(6)] + [random.randint(40, 70) * 100]

        # 25% chance for Movement_Points boost
        if random.random() < 0.25:
            movement_points = random.choice([750, 1500, 2250])

        return {
            "Experience": experience,
            "Spell_Points": spell_points,
            "Morale": morale,
            "Luck": luck,
            "Resources": resources,
            "Primary_Skills": primary_skills,
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": movement_points,
        }
    elif (zone_type == "III" and zone_owner == players.ID.Neutral) or (
        zone_type in {"I", "II"} and zone_owner == players.ID.Red
    ):
        # Generate primary skills
        primary_skills = random.choice([[2, 1, 1, 0], [1, 1, 1, 1]])

        # Initialize values
        experience = 0
        spell_points = 0
        morale = 0
        luck = 0
        resources = [0, 0, 0, 0, 0, 0, 0]
        movement_points = 0

        # 25% chance for Experience boost
        if random.random() < 0.25:
            experience = random.choice([70000, 100000, 130000])

        # 25% chance for Spell_Points boost
        if random.random() < 0.25:
            spell_points = random.choice([700, 850, 1000])

        # 25% chance for Morale boost
        if random.random() < 0.25:
            morale = random.choice([1, 2, 3])

        # 25% chance for Luck boost
        if random.random() < 0.25:
            luck = random.choice([1, 2, 3])

        # 25% chance for Resources boost
        if random.random() < 0.25:
            resources = [random.randint(70, 130) for _ in range(6)] + [random.randint(70, 130) * 100]

        # 25% chance for Movement_Points boost
        if random.random() < 0.25:
            movement_points = random.choice([1000, 2250, 3500])

        return {
            "Experience": experience,
            "Spell_Points": spell_points,
            "Morale": morale,
            "Luck": luck,
            "Resources": resources,
            "Primary_Skills": primary_skills,
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": movement_points,
        }
    elif (zone_type == "IV" and zone_owner in {players.ID.Red, players.ID.Neutral}) or (
        zone_type == "III" and zone_owner == players.ID.Red
    ):
        # Generate primary skills
        primary_skills = random.choice([[2, 1, 1, 1], [2, 2, 1, 0]])

        # Initialize values
        experience = 0
        spell_points = 0
        morale = 0
        luck = 0
        resources = [0, 0, 0, 0, 0, 0, 0]
        movement_points = 0

        # 25% chance for Experience boost
        if random.random() < 0.25:
            experience = random.choice([100000, 150000, 200000])

        # 25% chance for Spell_Points boost
        if random.random() < 0.25:
            spell_points = random.choice([1000, 1250, 1500])

        # 25% chance for Morale boost
        if random.random() < 0.25:
            morale = random.choice([1, 2, 3])

        # 25% chance for Luck boost
        if random.random() < 0.25:
            luck = random.choice([1, 2, 3])

        # 25% chance for Resources boost
        if random.random() < 0.25:
            resources = [random.randint(100, 200) for _ in range(6)] + [random.randint(100, 200) * 100]

        # 25% chance for Movement_Points boost
        if random.random() < 0.25:
            movement_points = random.choice([1500, 3000, 4500])

        return {
            "Experience": experience,
            "Spell_Points": spell_points,
            "Morale": morale,
            "Luck": luck,
            "Resources": resources,
            "Primary_Skills": primary_skills,
            "Secondary_Skills": [],
            "Artifacts": [],
            "Spells": [],
            "Creatures": [],
            "garbage_bytes": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Movement_Mode": 0,
            "Movement_Points": movement_points,
        }


def modify_primary_skills(zone_type) -> list:
    """
    Distribute primary skill points evenly but randomly.
    Creates a distribution array respecting constraints, then shuffles it.
    """
    if zone_type in {"P1"}:
        # 1 point in a random skill
        skills = [1, 0, 0, 0]
    elif zone_type in {"P2", "P3", "L1", "W1"}:
        # 2 points in random skills (can be both in same skill)
        skills = random.choice([[1, 1, 0, 0], [2, 0, 0, 0]])
    elif zone_type in {"P4", "L2", "W2"}:
        # 3 points in random skills (distribute however, but max 2 in one skill)
        skills = random.choice([[1, 1, 1, 0], [2, 1, 0, 0]])
    elif zone_type in {"L3", "W3"}:
        # 4 points in random skills (distribute however, but max 2 in one skill)
        skills = random.choice([[2, 1, 1, 0], [1, 1, 1, 1]])
    elif zone_type in {"L4", "W4"}:
        # 5 points in random skills (distribute however, but max 2 in one skill)
        skills = random.choice([[2, 1, 1, 1], [2, 2, 1, 0]])
    else:
        xprint(
            type=TextType.ERROR,
            text=f"Tried to modify pandoras box in invalid zone type '{zone_type}'.",
        )

    # Shuffle to randomize which skill gets which points
    random.shuffle(skills)
    return skills
