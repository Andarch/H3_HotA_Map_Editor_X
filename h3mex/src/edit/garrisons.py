import random
from copy import deepcopy

from src.common import MsgType, map_data
from src.defs import creatures, objects
from src.defs.players import Players
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def fill_empty_garrison_guards():
    xprint(type=MsgType.ACTION, text="Filling empty garrison guards…")

    modified_count = 0

    garrison_ids = {objects.ID.Garrison, objects.ID.Garrison_Vertical}

    for obj in map_data["object_data"]:
        if obj["id"] not in garrison_ids:
            continue
        if obj["owner"] == Players.Neutral and _is_empty_guards(obj["guards"]):
            obj["guards"] = _get_random_guards(obj["zone_type"])
            modified_count += 1

    xprint(type=MsgType.DONE)
    xprint()
    xprint(type=MsgType.INFO, text=f"Filled {modified_count} empty garrisons with guards.")
    wait_for_keypress()


def copy_garrison_guards():
    xprint(type=MsgType.ACTION, text="Copying garrison guards…")

    modified_count = 0

    # Collect one non-empty guards template per owner (skip Red)
    templates: dict[Players, list | None] = {
        Players.Blue: None,
        Players.Tan: None,
        Players.Green: None,
        Players.Orange: None,
        Players.Purple: None,
        Players.Teal: None,
        Players.Pink: None,
    }

    garrison_ids = {objects.ID.Garrison, objects.ID.Garrison_Vertical}

    # Pass 1: capture first non-empty guards list per owner
    for obj in map_data["object_data"]:
        if obj["id"] not in garrison_ids:
            continue
        owner = obj["owner"]
        if owner not in templates:
            continue
        guards = obj["guards"]
        if not _is_empty_guards(guards) and templates[owner] is None:
            templates[owner] = deepcopy(guards)

    # Pass 2: fill empty guards from the owner’s template
    for obj in map_data["object_data"]:
        if obj["id"] not in garrison_ids:
            continue
        owner = obj["owner"]
        if owner not in templates:
            continue
        if _is_empty_guards(obj["guards"]):
            template = templates[owner]
            if template is not None:
                obj["guards"] = deepcopy(template)
                modified_count += 1

    xprint(type=MsgType.DONE)
    xprint()
    xprint(type=MsgType.INFO, text=f"Copied {modified_count} garrison guards.")
    wait_for_keypress()


def _rand_enum_value(enum_cls):
    return random.choice(list(enum_cls)).value


def _get_random_guards(zone_type):
    if zone_type in {"P1", "R1", "L1", "W1"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": 1000},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": 500},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": 100},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": 50},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": 250},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": 750},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": 1500},
        ]
    elif zone_type in {"P2", "R2", "L2", "W2"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": 1500},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": 750},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": 250},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": 100},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": 500},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": 1000},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": 2000},
        ]
    elif zone_type in {"P3", "R3", "L3", "W3"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": 2000},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": 1000},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": 500},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": 250},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": 750},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": 1500},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": 3000},
        ]
    elif zone_type in {"P4", "R4", "L4", "W4"}:
        return [
            {"id": _rand_enum_value(creatures.Level2Creatures), "amount": 3000},
            {"id": _rand_enum_value(creatures.Level4Creatures), "amount": 1500},
            {"id": _rand_enum_value(creatures.Level6Creatures), "amount": 750},
            {"id": _rand_enum_value(creatures.Level7Creatures), "amount": 500},
            {"id": _rand_enum_value(creatures.Level5Creatures), "amount": 1000},
            {"id": _rand_enum_value(creatures.Level3Creatures), "amount": 2000},
            {"id": _rand_enum_value(creatures.Level1Creatures), "amount": 4000},
        ]


def _is_empty_guards(guards) -> bool:
    EMPTY_GUARD_ID = 0xFFFF  # 65535
    if not isinstance(guards, list) or len(guards) != 7:
        return not guards  # None or empty list
    return all((g.get("id") == EMPTY_GUARD_ID) or (g.get("amount", 0) <= 0) for g in guards)
