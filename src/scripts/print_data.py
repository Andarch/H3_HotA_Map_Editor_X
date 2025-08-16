# import pprint
import json
import re

import data.objects as objects

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

# Define regex patterns for different data types at module level
REGEX_LISTS = r'([ \t]*)("[^"]+": )(\[[\s\S]*?\])(,?)'
REGEX_STRINGS = r'([ \t]*)("[^"]+":) (".*?")(,?)'  # Include quotes in the capture group
REGEX_DICTS = r'([ \t]*)("[^"]+":) (\{[\s\S]*?\})(,?)'
REGEX_ARRAY_DICTS = r"([ \t]+)()(\{[^{}]*\})(,?)"  # Only match simple dicts that are array elements


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
                obj_filter = []
                xprint(text="Loading object data...")
            case 9:
                section_name = "events"
            case 0:
                section_name = "object_data"
                obj_filter = [objects.ID.Town, objects.ID.Random_Town]
                xprint(text="Loading town data...")

        if section_name == "object_data":
            if not obj_filter:
                dump_source = map_data["object_data"]
            else:
                dump_source = [obj for obj in map_data["object_data"] if obj["id"] in obj_filter]
        else:
            dump_source = map_data[section_name]

        data = json.dumps(dump_source, indent=4, default=str)

        # Special case: if the entire section is just an empty list, format it inline
        if data.strip() == "[]":
            xprint(type=Text.INFO, text=f'"{section_name}": []')
            wait_for_keypress()
            continue

        # Apply formatting in sequence - array dicts first, then lists
        data = re.sub(REGEX_ARRAY_DICTS, _format_data, data)
        data = re.sub(REGEX_LISTS, _format_data, data)
        data = re.sub(REGEX_STRINGS, _format_data, data)
        data = re.sub(REGEX_DICTS, _format_data, data)

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
    value = m.group(3)
    suffix = m.group(4)

    # Determine data type based on the actual matched pattern
    if value.startswith("[") and value.endswith("]"):  # Lists
        return _format_lists(indent, prefix, value, suffix)
    elif value.startswith('"') and value.endswith('"'):  # Strings
        return _format_string(indent, prefix, value, suffix)
    elif value.startswith("{") and value.endswith("}"):  # Dictionaries
        return _format_dict(indent, prefix, value, suffix)
    else:
        return m.group(0)  # Fallback - return unchanged


def _format_lists(indent: str, list_prefix: str, _list: str, list_suffix: str) -> str:
    # Split on commas that are not inside dictionaries
    list_items = []
    content = _list.strip("[]")
    brace_level = 0
    current_item = ""
    for char in content:
        if char == "{":
            brace_level += 1
        elif char == "}":
            brace_level -= 1
        elif char == "," and brace_level == 0:
            if current_item.strip():
                list_items.append(current_item.strip())
            current_item = ""
            continue
        current_item += char
    # Add the last item
    if current_item.strip():
        list_items.append(current_item.strip())

    if not list_items:
        return f"{indent}{list_prefix}[]{list_suffix}"

    for list_item in list_items:
        if list_item.startswith("{") and list_item.endswith("}"):
            list_contains_dicts = True
        else:
            list_contains_dicts = False
            break
    if list_contains_dicts:
        original_format = f"{indent}{list_prefix}{_list}{list_suffix}"
        return original_format

    # Define for #1 and #2
    flat_list = "[" + ", ".join(list_items) + "]"

    # 1. Try flat list (single-line list on same line as key)
    flat_final = f"{indent}{list_prefix}{flat_list}{list_suffix}"
    if len(flat_final) <= MAX_PRINT_WIDTH:
        return flat_final

    # Define for #2 and #3
    hanging_indent = indent + (" " * 4)

    # 2. Try hanging flat list (single-line list on its own indented line)
    lines = [f"{indent}{list_prefix}["]
    line = f"{hanging_indent}{flat_list}{list_suffix}"
    if len(line) <= MAX_PRINT_WIDTH:
        lines.append(line)
        hanging_flat_final = "\n".join(lines)
        return hanging_flat_final

    # 3. Wrapped version - each item on its own line
    lines = [f"{indent}{list_prefix}["]
    for i, list_item in enumerate(list_items):
        is_last_item = i + 1 == len(list_items)
        item_suffix = "" if is_last_item else ","
        lines.append(f"{hanging_indent}{list_item}{item_suffix}")
    lines.append(f"{indent}]{list_suffix}")
    return "\n".join(lines)


def _format_string(indent: str, prefix: str, values: str, comma: str) -> str:
    result_flat = f"{indent}{prefix}{values}{comma}"

    # If it fits on one line, return it
    if len(result_flat) <= MAX_PRINT_WIDTH:
        return result_flat

    # For long strings, force multi-line
    hanging_indent = indent + (" " * 4)

    # Extract content without quotes for processing
    content = values[1:-1]  # Remove surrounding quotes

    # If string has no spaces, use character-by-character wrapping
    if " " not in content:
        available_width = MAX_PRINT_WIDTH - len(hanging_indent) - 2  # -2 for quotes
        lines = [f"{indent}{prefix}"]
        for i in range(0, len(content), available_width):
            chunk = content[i : i + available_width]
            if i == 0:
                lines.append(f'\n{hanging_indent}"{chunk}')
            elif i + available_width >= len(content):
                lines.append(f'\n{hanging_indent}{chunk}"{comma}')
            else:
                lines.append(f"\n{hanging_indent}{chunk}")
        return "".join(lines)
    else:
        # Word-based wrapping for strings with spaces
        words = content.split(" ")
        lines = [f"{indent}{prefix}"]
        current_line = '"'
        for word in words:
            test_line = current_line + (" " if current_line != '"' else "") + word
            if len(f"{hanging_indent}{test_line}") <= MAX_PRINT_WIDTH - 1:
                current_line = test_line
            else:
                if current_line:
                    lines.append(f"\n{hanging_indent}{current_line}")
                current_line = word
        lines.append(f'\n{hanging_indent}{current_line}"{comma}')
        return "".join(lines)


def _format_dict(indent: str, prefix: str, values: str, comma: str) -> str:
    # Parse dictionary into flat format
    flat_dict = re.sub(r"\s+", " ", values.strip())

    # For standalone dictionaries (no prefix), just try to flatten if it fits
    if not prefix.strip():
        result_flat = f"{indent}{flat_dict}{comma}"
        if len(result_flat) <= MAX_PRINT_WIDTH:
            return result_flat
        # If it doesn't fit flat, keep original formatting
        return f"{indent}{values}{comma}"

    # For key-value dictionaries, use the original logic
    result_flat = f"{indent}{prefix}{flat_dict}{comma}"

    # 1. Try flat on same line as key
    if len(result_flat) <= MAX_PRINT_WIDTH:
        return result_flat

    # 2. Try hanging flat (dict on its own indented line)
    hanging_indent = indent + (" " * 4)
    hanging_line = f"{hanging_indent}{flat_dict}{comma}"
    if len(hanging_line) <= MAX_PRINT_WIDTH:
        return f"{indent}{prefix}\n{hanging_line}"

    # 3. Keep original formatting and let strings inside be processed later
    return f"{indent}{prefix}{values}{comma}"
