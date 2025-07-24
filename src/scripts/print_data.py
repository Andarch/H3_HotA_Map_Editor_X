# import pprint
import json
import re

from ..common import (
    KB,
    MAX_PRINT_WIDTH,
    Color,
    Text,
    draw_header,
    map_data,
    press_any_key,
    xprint,
)
from ..menus import Menu


def print_data() -> None:
    user_input = xprint(menu=Menu.INFO.value)
    if user_input == KB.ESC.value:
        return False

    draw_header()

    section_name = None
    match user_input:
        case 1:
            section_name = "map_specs"
        case 2:
            section_name = "player_specs"
        case 3:
            section_name = "starting_heroes"
        case 4:
            section_name = "rumors"
        case 5:
            section_name = "hero_data"
        case 6:
            section_name = "terrain"
        case 7:
            section_name = "object_defs"
        case 8:
            section_name = "object_data"
        case 9:
            section_name = "events"

    # Prepare lines for printing
    if section_name == "hero_data":
        lines = _format_hero_short_skills_dicts(map_data[section_name])
    else:
        json_output = json.dumps(map_data[section_name], indent=4, default=str)
        json_output = _format_strings(json_output, max_length=MAX_PRINT_WIDTH)
        json_output = _format_bit_lists(json_output, max_length=MAX_PRINT_WIDTH)
        lines = json_output.splitlines()

    # Print the section name before the data lines
    xprint(type=Text.INFO, text=f'"{section_name}":')

    # Print the data lines
    for line in lines:
        xprint(type=Text.INFO, text=line)

    press_any_key()


def _format_hero_short_skills_dicts(hero_data: dict) -> list[str]:
    def is_short_skills_dict(d):
        if not isinstance(d, dict):
            return False
        keys = set(d.keys())
        return keys == {"add_skills", "cannot_gain_xp", "level"}

    def format_short_skills_dict(d):
        return (
            '{   "add_skills": '
            + str(d["add_skills"]).lower()
            + ',   "cannot_gain_xp": '
            + str(d["cannot_gain_xp"]).lower()
            + ',   "level": '
            + str(d["level"])
            + "   },"
        )

    lines = []
    # hero_data is a list of dicts, each representing a hero
    for hero in hero_data:
        if isinstance(hero, dict) and is_short_skills_dict(hero):
            # Only the 3-key case, print inline
            lines.append("    " + format_short_skills_dict(hero))
        else:
            # Print as formatted JSON for any non-3-key dict or non-dict
            json_str = json.dumps(hero, indent=4, default=str)
            json_str = _format_strings(json_str, max_length=MAX_PRINT_WIDTH)
            json_str = _format_bit_lists(json_str, max_length=MAX_PRINT_WIDTH)
            for line in json_str.splitlines():
                lines.append("    " + line)
    return lines


def _format_strings(json_text: str, max_length: int = 70) -> str:
    def wrap_match(m):
        key = m.group(1)
        value = m.group(2)
        comma = m.group(3) or ""
        # If no spaces or any word longer than max_length, fallback to old splitting
        if " " not in value or any(len(word) > max_length for word in value.split()):
            wrapped = [value[i : i + max_length].strip() for i in range(0, len(value), max_length)]
        else:
            words = value.split()
            wrapped = []
            line = ""
            first_line = True
            for word in words:
                if first_line:
                    available = max_length - 1  # account for opening quote
                else:
                    available = max_length
                # If line is empty, just add the word
                if not line:
                    if len(word) > available:
                        # word itself is too long, just add it
                        line = word
                    else:
                        line = word
                # If adding the word would exceed available, start new line
                elif len(line) + 1 + len(word) > available:
                    wrapped.append(line)
                    line = word
                    first_line = False
                else:
                    line += " " + word
            if line:
                wrapped.append(line)
        # Add opening quote only to the first line
        if wrapped:
            wrapped[0] = '"' + wrapped[0]
        result = (
            f"{key}\n\n"
            + Color.CYAN_FAINT.value
            + f"\n{Color.CYAN_FAINT.value}".join(wrapped)
            + f'"{comma}{Color.RESET.value}\n'
        )
        return result

    return re.sub(r'(\s*"[^"]+":)\s*"([^"\n]{70,})"(\,?)', wrap_match, json_text)


def _format_bit_lists(json_text: str, max_length: int = 70) -> str:
    def wrap_match(m):
        key = m.group(1)
        values = m.group(2)
        comma = m.group(3) or ""
        items = [v.strip() for v in values.split(",") if v.strip()]
        # Special case: keys containing 'coords' always inline, indented, no leading newline
        if "coords" in key:
            list_str = "[" + ", ".join(items) + "]"
            leading_ws = re.match(r"^(\s*)", key).group(1)
            key_clean = key.replace("\n", "").strip()
            return f"{leading_ws}{key_clean} {list_str}{comma}"
        if all(v.isdigit() and len(v) == 1 for v in items):
            list_str = "[" + ", ".join(items) + "]"
            if len(list_str) <= max_length:
                return f"{key} {list_str}{comma}"
            else:
                wrapped = []
                line = ""
                for idx, v in enumerate(items):
                    is_last_item = idx == len(items) - 1
                    # For wrapped lines after the first, add a space at the start
                    if line and len(line) + len(v) + 2 + 1 > max_length:  # +1 for the space
                        wrapped.append(line)
                        line = " "  # Add a space at the start of new lines after the first
                    line += v
                    if not is_last_item:
                        line += ", "
                if line:
                    wrapped.append(line)
                return (
                    f"{key}\n\n"
                    + Color.CYAN_FAINT.value
                    + "["
                    + f"\n{Color.CYAN_FAINT.value}".join(wrapped)
                    + "]"
                    + f"{comma}{Color.RESET.value}\n"
                )
        return m.group(0)

    return re.sub(r'(\s*"[^"]+":)\s*\[([0-9,\s]+)\](\,?)', wrap_match, json_text)
