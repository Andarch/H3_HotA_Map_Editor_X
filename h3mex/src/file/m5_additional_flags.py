import math

from src.common import VariableValueMode

from . import io


def parse_flags() -> dict:
    info = {
        "allow_plague": False,
        "combo_artifact_count": 0,
        "combo_artifacts": [],
        "combat_round_limit": 0,
        "forbid_hiring": [],
        "has_hota_events": False,
        "hota_events": [],
        "artifact_count": 0,
        "artifacts": [],
        "spells": [],
        "skills": [],
    }

    info["allow_plague"] = bool(io.read_int(4))

    info["combo_artifact_count"] = io.read_int(4)
    combo_artifact_bytes = math.ceil(info["combo_artifact_count"] / 8)
    info["combo_artifacts"] = io.read_bits(combo_artifact_bytes)

    info["combat_round_limit"] = io.read_int(4)

    for _ in range(8):
        info["forbid_hiring"].append(bool(io.read_int(1)))

    info["has_hota_events"] = bool(io.read_int(1))
    if info["has_hota_events"]:
        info["hota_events"] = parse_hota_events()

    info["artifact_count"] = io.read_int(4)
    artifact_bytes = math.ceil(info["artifact_count"] / 8)
    info["artifacts"] = io.read_bits(artifact_bytes)

    info["spells"] = io.read_bits(9)
    info["skills"] = io.read_bits(4)

    return info


def parse_hota_events() -> list:
    hota_events = {
        "hero_events": [],
        "player_events": [],
        "town_events": [],
        "quest_events": [],
        "variable_count": 0,
        "hero_event_id_counter": 0,
        "player_event_id_counter": 0,
        "town_event_id_counter": 0,
        "quest_event_id_counter": 0,
        "variable_id_counter": 0,
        "variables": [],
        "hero_event_ids": [],
        "player_event_ids": [],
        "town_event_ids": [],
        "quest_event_ids": [],
        "variable_ids": [],
    }

    # Hero events
    for _ in range(io.read_int(4)):
        event = {}
        event["event_id"] = io.read_int(4)
        event["nine_bytes"] = io.read_raw(9)
        event["event_name"] = io.read_str(io.read_int(4))
        hota_events["hero_events"].append(event)

    # Player events
    for _ in range(io.read_int(4)):
        event = {}
        event["event_id"] = io.read_int(4)
        event["nine_bytes"] = io.read_raw(9)
        event["event_name"] = io.read_str(io.read_int(4))
        hota_events["player_events"].append(event)

    # Town events
    for _ in range(io.read_int(4)):
        event = {}
        event["event_id"] = io.read_int(4)
        event["nine_bytes"] = io.read_raw(9)
        event["event_name"] = io.read_str(io.read_int(4))
        hota_events["town_events"].append(event)

    # Quest events
    for _ in range(io.read_int(4)):
        event = {}
        event["event_id"] = io.read_int(4)
        event["nine_bytes"] = io.read_raw(9)
        event["event_name"] = io.read_str(io.read_int(4))
        hota_events["quest_events"].append(event)

    # Variable count
    hota_events["variable_count"] = io.read_int(4)

    # ID counters
    hota_events["hero_event_id_counter"] = io.read_int(4)
    hota_events["player_event_id_counter"] = io.read_int(4)
    hota_events["town_event_id_counter"] = io.read_int(4)
    hota_events["quest_event_id_counter"] = io.read_int(4)
    hota_events["variable_id_counter"] = io.read_int(4)

    # Variables
    for _ in range(hota_events["variable_count"]):
        variable = {}
        variable["variable_id"] = io.read_int(4)
        variable["variable_name"] = io.read_str(io.read_int(4))
        variable["save_in_campaign"] = bool(io.read_int(1))
        variable["value_mode"] = VariableValueMode(io.read_int(1))
        if variable["value_mode"] == VariableValueMode.InitialValue:
            variable["value"] = io.read_int(4)
        hota_events["variables"].append(variable)

    # IDs
    for _ in range(io.read_int(4)):
        hota_events["hero_event_ids"].append(io.read_int(4))
    for _ in range(io.read_int(4)):
        hota_events["player_event_ids"].append(io.read_int(4))
    for _ in range(io.read_int(4)):
        hota_events["town_event_ids"].append(io.read_int(4))
    for _ in range(io.read_int(4)):
        hota_events["quest_event_ids"].append(io.read_int(4))
    for _ in range(io.read_int(4)):
        hota_events["variable_ids"].append(io.read_int(4))

    return hota_events


def write_flags(info: dict) -> None:
    io.write_int(info["allow_plague"], 4)

    io.write_int(info["combo_artifact_count"], 4)
    io.write_bits(info["combo_artifacts"])

    io.write_int(info["combat_round_limit"], 4)

    for player in range(8):
        io.write_int(info["forbid_hiring"][player], 1)

    io.write_int(info["has_hota_events"], 1)
    if info["has_hota_events"]:
        write_hota_events(info["hota_events"])

    io.write_int(info["artifact_count"], 4)
    io.write_bits(info["artifacts"])

    io.write_bits(info["spells"])
    io.write_bits(info["skills"])


def write_hota_events(hota_events: list) -> None:
    # Hero events
    io.write_int(len(hota_events["hero_events"]), 4)
    for event in hota_events["hero_events"]:
        io.write_int(event["event_id"], 4)
        io.write_raw(event["nine_bytes"])
        io.write_int(len(event["event_name"]), 4)
        io.write_str(event["event_name"])

    # Player events
    io.write_int(len(hota_events["player_events"]), 4)
    for event in hota_events["player_events"]:
        io.write_int(event["event_id"], 4)
        io.write_raw(event["nine_bytes"])
        io.write_int(len(event["event_name"]), 4)
        io.write_str(event["event_name"])

    # Town events
    io.write_int(len(hota_events["town_events"]), 4)
    for event in hota_events["town_events"]:
        io.write_int(event["event_id"], 4)
        io.write_raw(event["nine_bytes"])
        io.write_int(len(event["event_name"]), 4)
        io.write_str(event["event_name"])

    # Quest events
    io.write_int(len(hota_events["quest_events"]), 4)
    for event in hota_events["quest_events"]:
        io.write_int(event["event_id"], 4)
        io.write_raw(event["nine_bytes"])
        io.write_int(len(event["event_name"]), 4)
        io.write_str(event["event_name"])

    # Variable count
    io.write_int(hota_events["variable_count"], 4)

    # ID counters
    io.write_int(hota_events["hero_event_id_counter"], 4)
    io.write_int(hota_events["player_event_id_counter"], 4)
    io.write_int(hota_events["town_event_id_counter"], 4)
    io.write_int(hota_events["quest_event_id_counter"], 4)
    io.write_int(hota_events["variable_id_counter"], 4)

    # Variables
    for variable in hota_events["variables"]:
        io.write_int(variable["variable_id"], 4)
        io.write_int(len(variable["variable_name"]), 4)
        io.write_str(variable["variable_name"])
        io.write_int(variable["save_in_campaign"], 1)
        io.write_int(variable["value_mode"], 1)
        if variable["value_mode"] == VariableValueMode.InitialValue:
            io.write_int(variable["value"], 4)

    # IDs
    io.write_int(len(hota_events["hero_event_ids"]), 4)
    for id in hota_events["hero_event_ids"]:
        io.write_int(id, 4)
    io.write_int(len(hota_events["player_event_ids"]), 4)
    for id in hota_events["player_event_ids"]:
        io.write_int(id, 4)
    io.write_int(len(hota_events["town_event_ids"]), 4)
    for id in hota_events["town_event_ids"]:
        io.write_int(id, 4)
    io.write_int(len(hota_events["quest_event_ids"]), 4)
    for id in hota_events["quest_event_ids"]:
        io.write_int(id, 4)
    io.write_int(len(hota_events["variable_ids"]), 4)
    for id in hota_events["variable_ids"]:
        io.write_int(id, 4)
