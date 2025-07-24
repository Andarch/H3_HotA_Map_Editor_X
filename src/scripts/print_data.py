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
    while True:
        user_input = xprint(menu=Menu.INFO.value)
        if user_input == KB.ESC.value:
            break

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

        if section_name == "hero_data":
            lines = _format_hero_data(map_data[section_name])
        elif section_name == "player_specs":
            lines = _format_player_specs(map_data[section_name])
        else:
            lines = _format_json_section(map_data[section_name])

        xprint(type=Text.INFO, text=f'"{section_name}":')

        lines_printed = 0
        for line in lines:
            xprint(type=Text.INFO, text=line)
            lines_printed += 1
            if lines_printed % 100 == 0:
                press_any_key(suffix=" to continue printing")
                for _ in range(3):
                    print("\033[F\033[K", end="")
        press_any_key()


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
                json_lines = _format_json_section({k: v})
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
            for line in _format_json_section(hero):
                lines.append("    " + line)
    return lines


def _format_json_section(data) -> list[str]:
    json_output = json.dumps(data, indent=4, default=str)
    json_output = _format_strings(json_output)
    json_output = _format_lists(json_output)
    return json_output.splitlines()


def _format_strings(json_text: str, max_length: int = MAX_PRINT_WIDTH - 8) -> str:
    def wrap_match(m):
        key = m.group(1)
        value = m.group(2)
        comma = m.group(3) or ""
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

    pattern = rf'(\s*"[^"]+":)\s*"([^"\n]{{{max_length},}})"(\,?)'
    return re.sub(pattern, wrap_match, json_text)


def _format_lists(json_text: str, max_length: int = MAX_PRINT_WIDTH - 8) -> str:
    def wrap_match(m):
        key = m.group(1)
        values = m.group(2)
        comma = m.group(3) or ""
        items = [v.strip() for v in values.split(",") if v.strip()]
        # Special cases
        SPECIAL_KEYS = ("coords", "resources")  # Add more as needed
        if any(special in key for special in SPECIAL_KEYS):
            list_str = "[" + ", ".join(items) + "]"
            leading_ws = re.match(r"^(\s*)", key).group(1)
            key_clean = key.replace("\n", "").strip()
            return f"{leading_ws}{key_clean} {list_str}{comma}"
        # Single-digit numbers (e.g., bits)
        if all(v.isdigit() and len(v) == 1 for v in items):
            list_str = "[" + ", ".join(items) + "]"
            # Calculate the full line length including indentation, key, space, list, and comma
            full_line = f"{key} {list_str}{comma}"
            if len(full_line) <= max_length:
                return full_line
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

    pattern = r'(\s*"[^"]+":)\s*\[([0-9,\s]+)\](\,?)'
    return re.sub(pattern, wrap_match, json_text)
