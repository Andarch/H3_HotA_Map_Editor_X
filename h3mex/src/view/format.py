import json
import re

from src.common import (
    MAX_PRINT_WIDTH,
    xprint,
)
from src.defs import objects

REGEX_LISTS = r'([ \t]*)("[^"]+":\s*)(\[[^\[\]{}]*\])(,?)'
REGEX_STRINGS = r'([ \t]*)("[^"]+":)\s*("(?:\\.|[^"\\])*")(,?)'
REGEX_DICTS = r'([ \t]*)("[^"]+":) (\{[\s\S]*?\})(,?)'
REGEX_ARRAY_DICTS = r"([ \t]+)()(\{[^\[\]{}]*\})(,?)"

###################################
OBJECT_FILTER = [*objects.ID]
###################################


def format_map_data(section: tuple[str, dict | list]) -> list[str]:
    # Perform JSON dump
    name = section[0]
    data = json.dumps(section[1], indent=4, default=str)

    # Special case: if the entire section is just an empty list, format it inline
    if data.strip() == "[]":
        xprint(overwrite=2)
        return [f'"{name}": []']

    # Apply formatting in sequence - array dicts first, then lists
    data = re.sub(REGEX_ARRAY_DICTS, _format_map_data, data)
    data = re.sub(REGEX_LISTS, _format_map_data, data)
    data = re.sub(REGEX_STRINGS, _format_map_data, data)
    data = re.sub(REGEX_DICTS, _format_map_data, data)

    # Special case: clear loading message
    if name in ("terrain", "object_defs", "object_data"):
        xprint(overwrite=2)

    return [f'"{name}":'] + data.splitlines()


def _format_map_data(m: re.Match) -> str:
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


def _format_lists(indent: str, list_prefix: str, list_: str, list_suffix: str) -> str:
    # Split on commas that are not inside dictionaries
    list_items = []
    content = list_.strip("[]")
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
        original_format = f"{indent}{list_prefix}{list_}{list_suffix}"
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

    # 3. Wrapped version - pack items per line up to MAX_PRINT_WIDTH (word-like wrapping)
    lines = [f"{indent}{list_prefix}["]
    current_line = ""
    for i, list_item in enumerate(list_items):
        is_last_item = i + 1 == len(list_items)
        token = f"{list_item}{'' if is_last_item else ','}"
        test_line = token if current_line == "" else f"{current_line} {token}"
        if len(f"{hanging_indent}{test_line}") <= MAX_PRINT_WIDTH:
            current_line = test_line
        else:
            if current_line:
                lines.append(f"{hanging_indent}{current_line}")
            current_line = token
    if current_line:
        lines.append(f"{hanging_indent}{current_line}")
    lines.append(f"{indent}]{list_suffix}")
    return "\n".join(lines)


def _format_string(indent: str, prefix: str, values: str, comma: str) -> str:
    result_flat = f"{indent}{prefix} {values}{comma}"

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
