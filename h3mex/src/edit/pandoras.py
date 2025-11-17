import random

from src.common import TextType, map_data
from src.defs import creatures, objects
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def modify_pandoras():
    xprint(type=TextType.ACTION, text="Modifying Pandora's Boxes…")

    modified_count = 0

    for obj in map_data["object_data"]:
        if obj["id"] == objects.ID.Pandoras_Box:
            is_default = _check_default(obj)
            if not is_default:
                continue

            obj["has_common"] = 1
            obj["guards"] = _get_random_guards(obj["zone_type"])
            obj["contents"] = _get_random_contents(obj["zone_type"])
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


def _get_random_guards(zone_type):
    if zone_type in {"P1", "R1", "L1", "W1"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": random.randint(50, 75)},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": random.randint(20, 30)},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": random.randint(5, 10)},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": random.randint(2, 5)},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": random.randint(10, 20)},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": random.randint(30, 50)},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": random.randint(75, 100)},
        ]
    elif zone_type in {"P2", "R2", "L2", "W2"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": random.randint(550, 700)},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": random.randint(200, 350)},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": random.randint(100, 150)},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": random.randint(50, 75)},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": random.randint(150, 200)},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": random.randint(350, 550)},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": random.randint(700, 900)},
        ]
    elif zone_type in {"P3", "R3", "L3", "W3"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": random.randint(1000, 1350)},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": random.randint(400, 650)},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": random.randint(150, 300)},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": random.randint(100, 175)},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": random.randint(300, 400)},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": random.randint(700, 1000)},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": random.randint(1350, 1700)},
        ]
    elif zone_type in {"P4", "R4", "L4", "W4"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": random.randint(1500, 2000)},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": random.randint(600, 1000)},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": random.randint(250, 400)},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": random.randint(150, 250)},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": random.randint(400, 600)},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": random.randint(1000, 1500)},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": random.randint(2000, 2500)},
        ]


def _get_random_contents(zone_type):
    if zone_type in {"P1", "R1", "L1", "W1"}:
        primary_skills = [random.randint(1, 3) for _ in range(4)]

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
            resources = [random.randint(10, 20) for _ in range(7)]

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
    elif zone_type in {"P2", "R2", "L2", "W2"}:
        primary_skills = [random.randint(2, 4) for _ in range(4)]

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
            resources = [random.randint(40, 70) for _ in range(7)]

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
    elif zone_type in {"P3", "R3", "L3", "W3"}:
        primary_skills = [random.randint(3, 7) for _ in range(4)]

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
            resources = [random.randint(70, 130) for _ in range(7)]

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
    elif zone_type in {"P4", "R4", "L4", "W4"}:
        primary_skills = [random.randint(4, 9) for _ in range(4)]

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
            resources = [random.randint(100, 200) for _ in range(7)]

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
