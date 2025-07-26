# import pprint
import json
import re

from ..common import (
    KB,
    MAX_PRINT_WIDTH,
    Text,
    draw_header,
    map_data,
    wait_for_keypress,
    xprint,
)
from ..menus import Menu


def print_data() -> None:
    while True:
        user_input = xprint(menu=Menu.INFO.value)
        if user_input == KB.ESC.value:
            break

        draw_header()

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
                xprint(text="Loading terrain data...")
            case 7:
                section_name = "object_defs"
                xprint(text="Loading object defs...")
            case 8:
                section_name = "object_data"
                xprint(text="Loading object data...")
            case 9:
                section_name = "events"

        data = json.dumps(map_data[section_name], indent=4, default=str)

        REGEX_STRINGS = rf'([ \t]*)("[^"]+": ")([^"\n]{{{MAX_PRINT_WIDTH},}})"(\,?)'
        REGEX_LISTS = r'([ \t]*)("[^"]+": \[)\s*([0-9,\s]+)(\],?)'

        for regex in (REGEX_STRINGS, REGEX_LISTS):
            data = re.sub(regex, _format_data, data)

        lines_printed = 0
        lines = [f'"{section_name}":'] + data.splitlines()

        for line in lines:
            xprint(type=Text.INFO, text=line)
            lines_printed += 1

            if lines_printed % 100 == 0:
                user_input = wait_for_keypress(suffix=" to continue printing")
                if user_input == KB.ESC.value:
                    break
                for _ in range(3):
                    print("\033[F\033[K", end="")

            if lines_printed == len(lines):
                wait_for_keypress()


def _format_data(m: re.Match) -> str:
    indent = m.group(1)
    prefix = m.group(2)
    values = m.group(3)
    suffix = m.group(4)

    cleaned_values = [value.strip() for value in values.split(",") if value.strip()]
    flattened_data = f"{indent}{prefix}{", ".join(cleaned_values)}{suffix}"

    if len(flattened_data) > MAX_PRINT_WIDTH:
        lines = []

        first_line = f"{indent}{prefix}"
        lines.append(first_line)

        wrapped_indent = indent + (" " * 4)
        wrapped_line = f"\n{wrapped_indent}"

        for i, value in enumerate(cleaned_values):
            is_line_start = wrapped_line == f"{wrapped_indent}"
            is_last_value = i + 1 == len(cleaned_values)
            addition = ("" if is_line_start else " ") + value + ("" if is_last_value else ",")

            if len(wrapped_line) + len(addition) <= MAX_PRINT_WIDTH:
                wrapped_line += addition
            else:
                lines.append(wrapped_line)
                wrapped_line = f"\n{wrapped_indent}{addition}"

            if is_last_value:
                lines.append(wrapped_line)

        last_line = f"\n{indent}{suffix}"
        lines.append(last_line)
        wrapped = "".join(lines)
        return wrapped
    else:
        return flattened_data


"""
<Old code>

if section_name == "hero_data":
    lines = _format_hero_data(map_data[section_name])
elif section_name == "player_specs":
    lines = _format_player_specs(map_data[section_name])
else:
    lines = _format_json_section(map_data[section_name])
"""


"""
<Old code>

def _format_player_specs(player_specs: list) -> list[str]:
    def format_hero_dict(d):
        return '{   "id": ' + str(d["id"]) + ',   "custom_name": ' + str(d["custom_name"]) + "   }"

    lines = []
    lines.append("[")
    for pidx, player in enumerate(player_specs):
        player_lines = []
        player_lines.append("{")
        keys = list(player.keys())
        for idx, k in enumerate(keys):
            v = player[k]
            is_last_key = idx == len(keys) - 1
            if k == "available_heroes":
                if not v:
                    player_lines.append('    "available_heroes": []' + ("," if not is_last_key else ""))
                else:
                    player_lines.append('    "available_heroes": [')
                    for hidx, hero in enumerate(v):
                        comma = "," if hidx < len(v) - 1 else ""
                        player_lines.append(f"        {format_hero_dict(hero)}{comma}")
                    player_lines.append("    ]" + ("," if not is_last_key else ""))
            else:
                # Format this key/value as JSON, but only this key/value
                json_lines = _format_data({k: v})
                # Remove the opening and closing braces
                content_lines = [line for line in json_lines if line.strip() not in ("{", "}")]
                # Add a comma if not the last key, but preserve all lines (including empty)
                if content_lines:
                    if not is_last_key:
                        # Find the last non-empty line
                        for i in range(len(content_lines) - 1, -1, -1):
                            line = content_lines[i]
                            if line.strip():
                                # If the line ends with a color reset, insert the comma before it
                                reset = Color.RESET.value
                                if line.endswith(reset):
                                    # Insert comma before reset, but after any trailing comma
                                    if line[-len(reset) - 1] == ",":
                                        # Already has a comma before reset, do nothing
                                        pass
                                    else:
                                        content_lines[i] = line[: -len(reset)] + "," + reset
                                else:
                                    # No color reset, just add comma
                                    content_lines[i] = line.rstrip(",") + ","
                                break
                    player_lines.extend(content_lines)
        player_lines.append("}" + ("," if pidx < len(player_specs) - 1 else ""))
        lines.extend("    " + line if line else "" for line in player_lines)
    lines.append("]")
    return lines


def _format_hero_data(hero_data: dict) -> list[str]:
    def is_short_skills_dict(d):
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
    for hero in hero_data:
        if is_short_skills_dict(hero):
            lines.append("    " + format_short_skills_dict(hero))
        else:
            for line in _format_data(hero):
                lines.append("    " + line)
    return lines


def _format_json_section(data) -> list[str]:
    json_output = json.dumps(data, indent=4, default=str)
    json_output = _format_strings(json_output)
    json_output = _format_lists(json_output)
    return json_output.splitlines()


def _format_strings(json_text: str, max_length: int = MAX_PRINT_WIDTH - 8) -> str:
    def wrap_match(m):
        key_indent = m.group(1)
        key = m.group(2)
        value = m.group(3)
        comma = m.group(4) or ""
        string_indent = key_indent + "    "
        # If no spaces or any word longer than max_length, fall back to simple wrapping
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

    pattern = rf'(\s*)("[^"]+":)\s*"([^"\n]{{{max_length},}})"(\,?)'
    return re.sub(pattern, wrap_match, json_text)


def _format_lists(json_text: str, max_length: int = MAX_PRINT_WIDTH - 8) -> str:
    def wrap_match(m):
        key_indent = m.group(1)
        key = m.group(2)
        values = m.group(3)
        comma = m.group(4) or ""
        list_indent = key_indent + "    "
        items = [v.strip() for v in values.split(",") if v.strip()]

        # Special cases
        SPECIAL_KEYS = ("coords", "resources")  # Add more as needed
        if any(special in key for special in SPECIAL_KEYS):
            list_str = "[" + ", ".join(items) + "]"
            key_clean = key.replace("\n", "").strip()
            return f"{key_indent}{key_clean} {list_str}{comma}"

        # Single-digit numbers (e.g., bits)
        if all(v.isdigit() and len(v) == 1 for v in items):
            key_line = f"{key_indent}{key} ["
            list_lines = []
            line = f"{list_indent}"
            for idx, v in enumerate(items):
                is_last = idx == len(items) - 1
                addition = v + ("," if not is_last else "")
                if len(line) + len(addition) > max_length:
                    list_lines.append(line)
                    line = f"{list_indent}{v}"
                else:
                    if line != f"{list_indent}":
                        line += " "
                    line += v
                if not is_last:
                    line += ","
                else:
                    list_lines.append(line)
            line = f"{key_indent}]{comma}"
            list_lines.append(line)
            return "\n".join([key_line] + list_lines)
        return m.group(0)

    pattern = r'([ \t]*)("[^"]+":)\s*\[([0-9,\s]+)\](\,?)'
    return re.sub(pattern, wrap_match, json_text)
"""
