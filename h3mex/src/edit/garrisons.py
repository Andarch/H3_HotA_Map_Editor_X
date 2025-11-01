from copy import deepcopy

from src.common import MsgType, map_data
from src.defs import objects
from src.defs.players import Players
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def copy_garrisons():
    xprint(type=MsgType.ACTION, text="Modifying garrisons…")

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
    xprint(type=MsgType.INFO, text=f"Modified {modified_count} garrisons.")
    wait_for_keypress()


def _is_empty_guards(guards) -> bool:
    EMPTY_GUARD_ID = 0xFFFF  # 65535
    if not isinstance(guards, list) or len(guards) != 7:
        return not guards  # None or empty list
    return all((g.get("id") == EMPTY_GUARD_ID) or (g.get("amount", 0) <= 0) for g in guards)
