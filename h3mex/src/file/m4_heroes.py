from src.defs import artifacts, heroes, skills, spells

from . import io


def parse_starting_heroes() -> dict:
    info = {"total_heroes": 0, "hero_flags": [], "placeholders": [], "custom_heroes": [], "unhandled_bytes": b""}

    info["total_heroes"] = io.read_int(4)
    info["hero_flags"] = io.read_bits(27)

    for _ in range(io.read_int(4)):  # Amount of placeholder heroes
        info["placeholders"].append(heroes.ID(io.read_int(1)))

    for _ in range(io.read_int(1)):  # Amount of custom heroes
        hero = {}
        hero["id"] = io.read_int(1)
        hero["face"] = io.read_int(1)
        hero["custom_name"] = io.read_str(io.read_int(4))
        hero["may_be_hired_by"] = io.read_int(1)
        info["custom_heroes"].append(hero)

    info["unhandled_bytes"] = io.read_raw(31)

    return info


def write_starting_heroes(info: dict) -> None:
    if info["total_heroes"] != 0:
        io.write_int(info["total_heroes"], 4)

    io.write_bits(info["hero_flags"])

    io.write_int(len(info["placeholders"]), 4)
    for hero in info["placeholders"]:
        io.write_int(hero, 1)

    io.write_int(len(info["custom_heroes"]), 1)

    for hero in info["custom_heroes"]:
        io.write_int(hero["id"], 1)
        io.write_int(hero["face"], 1)
        io.write_int(len(hero["custom_name"]), 4)
        io.write_str(hero["custom_name"])
        io.write_int(hero["may_be_hired_by"], 1)

    io.write_raw(info["unhandled_bytes"])


def parse_hero_data() -> list:
    info = []

    hero_amount = io.read_int(4)

    for _ in range(hero_amount):
        if not io.read_int(1):
            info.append({})
            continue

        hero = {
            "has_custom_experience": False,
            "experience": 0,
            "has_custom_secondary_skills": False,
            "secondary_skills": [],
            "artifacts_equipped": {},
            "artifacts_backpack": [],
            "biography": "",
            "gender": 255,
            "spells": b"",
            "primary_skills": {},
            "add_skills": True,
            "cannot_gain_xp": False,
            "level": 1,
        }

        hero["has_custom_experience"] = bool(io.read_int(1))
        if hero["has_custom_experience"]:
            hero["experience"] = io.read_int(4)

        hero["has_custom_secondary_skills"] = bool(io.read_int(1))
        if hero["has_custom_secondary_skills"]:
            for _ in range(io.read_int(4)):
                skill = {}
                skill["id"] = io.read_int(1)
                skill["name"] = skills.Secondary(skill["id"]).name
                skill["level"] = io.read_int(1)
                skill["level_name"] = skills.SecondaryLevels(skill["level"]).name
                hero["secondary_skills"].append(skill)

        if io.read_int(1):  # Are artifacts set?
            hero["artifacts_equipped"]["head"] = parse_artifact()
            hero["artifacts_equipped"]["shoulders"] = parse_artifact()
            hero["artifacts_equipped"]["neck"] = parse_artifact()
            hero["artifacts_equipped"]["right_hand"] = parse_artifact()
            hero["artifacts_equipped"]["left_hand"] = parse_artifact()
            hero["artifacts_equipped"]["torso"] = parse_artifact()
            hero["artifacts_equipped"]["right_ring"] = parse_artifact()
            hero["artifacts_equipped"]["left_ring"] = parse_artifact()
            hero["artifacts_equipped"]["feet"] = parse_artifact()
            hero["artifacts_equipped"]["misc_1"] = parse_artifact()
            hero["artifacts_equipped"]["misc_2"] = parse_artifact()
            hero["artifacts_equipped"]["misc_3"] = parse_artifact()
            hero["artifacts_equipped"]["misc_4"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_1"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_2"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_3"] = parse_artifact()
            hero["artifacts_equipped"]["war_machine_4"] = parse_artifact()
            hero["artifacts_equipped"]["spellbook"] = parse_artifact()
            hero["artifacts_equipped"]["misc_5"] = parse_artifact()

            for _ in range(io.read_int(2)):
                hero["artifacts_backpack"].append(parse_artifact())

        if io.read_int(1):  # Is biography set?
            hero["biography"] = io.read_str(io.read_int(4))

        hero["gender"] = io.read_int(1)

        if io.read_int(1):  # Are spells set?
            hero["spells"] = io.read_bits(9)

        if io.read_int(1):  # Are primary skills set?
            hero["primary_skills"]["attack"] = io.read_int(1)
            hero["primary_skills"]["defense"] = io.read_int(1)
            hero["primary_skills"]["spell_power"] = io.read_int(1)
            hero["primary_skills"]["knowledge"] = io.read_int(1)

        info.append(hero)

    for i in range(hero_amount):
        info[i]["add_skills"] = bool(io.read_int(1))
        info[i]["cannot_gain_xp"] = bool(io.read_int(1))
        info[i]["level"] = io.read_int(4)

    return info


def write_hero_data(info: list) -> None:
    io.write_int(len(info), 4)

    for hero in info:
        if len(hero) == 3:
            io.write_int(0, 1)
            continue
        io.write_int(1, 1)

        #
        if hero["has_custom_experience"]:
            io.write_int(1, 1)
            io.write_int(hero["experience"], 4)
        else:
            io.write_int(0, 1)

        #
        if hero["has_custom_secondary_skills"]:
            io.write_int(1, 1)
            io.write_int(len(hero["secondary_skills"]), 4)

            for skill in hero["secondary_skills"]:
                io.write_int(skill["id"], 1)
                io.write_int(skill["level"], 1)
        else:
            io.write_int(0, 1)

        #
        if hero["artifacts_equipped"] or hero["artifacts_backpack"]:
            io.write_int(1, 1)

            write_artifact(hero["artifacts_equipped"]["head"])
            write_artifact(hero["artifacts_equipped"]["shoulders"])
            write_artifact(hero["artifacts_equipped"]["neck"])
            write_artifact(hero["artifacts_equipped"]["right_hand"])
            write_artifact(hero["artifacts_equipped"]["left_hand"])
            write_artifact(hero["artifacts_equipped"]["torso"])
            write_artifact(hero["artifacts_equipped"]["right_ring"])
            write_artifact(hero["artifacts_equipped"]["left_ring"])
            write_artifact(hero["artifacts_equipped"]["feet"])
            write_artifact(hero["artifacts_equipped"]["misc_1"])
            write_artifact(hero["artifacts_equipped"]["misc_2"])
            write_artifact(hero["artifacts_equipped"]["misc_3"])
            write_artifact(hero["artifacts_equipped"]["misc_4"])
            write_artifact(hero["artifacts_equipped"]["war_machine_1"])
            write_artifact(hero["artifacts_equipped"]["war_machine_2"])
            write_artifact(hero["artifacts_equipped"]["war_machine_3"])
            write_artifact(hero["artifacts_equipped"]["war_machine_4"])
            write_artifact(hero["artifacts_equipped"]["spellbook"])
            write_artifact(hero["artifacts_equipped"]["misc_5"])

            io.write_int(len(hero["artifacts_backpack"]), 2)
            for artifact in hero["artifacts_backpack"]:
                write_artifact(artifact)
        else:
            io.write_int(0, 1)

        #
        if hero["biography"]:
            io.write_int(1, 1)
            io.write_int(len(hero["biography"]), 4)
            io.write_str(hero["biography"])
        else:
            io.write_int(0, 1)

        #
        io.write_int(hero["gender"], 1)

        #
        if hero["spells"] != b"":
            io.write_int(1, 1)
            io.write_bits(hero["spells"])
        else:
            io.write_int(0, 1)

        #
        if hero["primary_skills"]:
            io.write_int(1, 1)
            io.write_int(hero["primary_skills"]["attack"], 1)
            io.write_int(hero["primary_skills"]["defense"], 1)
            io.write_int(hero["primary_skills"]["spell_power"], 1)
            io.write_int(hero["primary_skills"]["knowledge"], 1)
        else:
            io.write_int(0, 1)

    # HotA 1.7.0.
    for hero in info:
        io.write_int(hero["add_skills"], 1)
        io.write_int(hero["cannot_gain_xp"], 1)
        io.write_int(hero["level"], 4)


def parse_artifact() -> list:
    artifact = [artifacts.ID(io.read_int(2)), io.read_int(2)]
    if artifact[0] == artifacts.ID.Spell_Scroll:
        artifact[1] = spells.ID(artifact[1])
    return artifact


def write_artifact(artifact: list) -> None:
    io.write_int(artifact[0], 2)
    io.write_int(artifact[1], 2)
