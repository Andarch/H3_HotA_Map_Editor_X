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

        # Special case: if the entire section is just an empty list, format it inline
        if data.strip() == "[]":
            lines_printed = 0
            lines = [f'"{section_name}": []']

            for line in lines:
                xprint(type=Text.INFO, text=line)
                lines_printed += 1

            wait_for_keypress()
            continue

        # Define regex patterns for different data types
        REGEX_LISTS = r'([ \t]*)("[^"]+": )(\[[\s\S]*?\])(,?)'
        REGEX_STRINGS = r'([ \t]*)("[^"]+": )"(.*?)"(,?)'  # Most permissive - match anything between quotes
        REGEX_DICTS = r'([ \t]*)("[^"]+": )(\{[\s\S]*?\})(,?)'
        REGEX_ARRAY_DICTS = r"([ \t]+)()(\{[^{}]*\})(,?)"  # Only match simple dicts that are array elements

        # Apply formatting in sequence - array dicts first, then lists
        data = re.sub(REGEX_ARRAY_DICTS, _format_data(REGEX_ARRAY_DICTS), data)
        data = re.sub(REGEX_LISTS, _format_data(REGEX_LISTS), data)
        data = re.sub(REGEX_STRINGS, _format_data(REGEX_STRINGS), data)
        data = re.sub(REGEX_DICTS, _format_data(REGEX_DICTS), data)

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


def _format_data(pattern: str):
    def format_data(m: re.Match) -> str:
        indent = m.group(1)
        prefix = m.group(2)
        values = m.group(3)
        comma = m.group(4)

        # Determine data type based on pattern
        if "\\[" in pattern:  # Lists
            return _format_list(indent, prefix, values, comma)
        elif '"(.*?)"' in pattern:  # Strings - check for the string content pattern
            return _format_string(indent, prefix, values, comma)
        elif "\\{" in pattern:  # Dictionaries (both key-value and array elements)
            return _format_dict(indent, prefix, values, comma)
        else:
            return m.group(0)  # Fallback - return unchanged

    return format_data


def _format_list(indent: str, prefix: str, values: str, comma: str) -> str:
    # Special case for empty lists - always keep them flat
    if values.strip() == "[]":
        return f"{indent}{prefix}[]{comma}"

    # Parse list values - be more careful about splitting on commas within dictionaries
    # First, let's just check if the raw values string contains dictionaries
    has_dict_values = "{" in values and "}" in values

    if has_dict_values:
        # For lists containing dictionaries, always put each item on its own line
        # Parse more carefully to handle dictionaries
        cleaned_values = []
        current_value = ""
        brace_count = 0

        for char in values.strip("[]"):
            if char == "{":
                brace_count += 1
                current_value += char
            elif char == "}":
                brace_count -= 1
                current_value += char
                if brace_count == 0:
                    # End of a dictionary, add it
                    cleaned_values.append(current_value.strip())
                    current_value = ""
            elif char == "," and brace_count == 0:
                # Comma outside of dictionaries, end current value
                if current_value.strip():
                    cleaned_values.append(current_value.strip())
                current_value = ""
            else:
                current_value += char

        # Don't forget the last value
        if current_value.strip():
            cleaned_values.append(current_value.strip())

        key = prefix.rstrip()
        hanging_indent = indent + (" " * 4)
        lines = [f"{indent}{key}["]
        for i, value in enumerate(cleaned_values):
            is_last_value = i + 1 == len(cleaned_values)
            comma_suffix = "" if is_last_value else ","
            lines.append(f"{hanging_indent}{value}{comma_suffix}")
        lines.append(f"{indent}]{comma}")
        return "\n".join(lines)

    # For non-dictionary lists, use the original three-tier logic
    cleaned_values = [value.strip() for value in values.strip("[]").split(",") if value.strip()]
    flat_values = ", ".join(cleaned_values)
    result_flat = f"{indent}{prefix}[{flat_values}]{comma}"

    # 1. Try flat on same line as key
    if len(result_flat) <= MAX_PRINT_WIDTH:
        return result_flat

    # 2. Try hanging flat (list on its own indented line)
    key = prefix.rstrip()
    hanging_indent = indent + (" " * 4)
    hanging_line = f"{hanging_indent}[{flat_values}]{comma}"
    if len(hanging_line) <= MAX_PRINT_WIDTH:
        return f"{indent}{key}\n{hanging_line}"

    # 3. Wrapped version for non-dictionary values
    lines = [f"{indent}{prefix}["]
    line = ""  # Start empty, will add hanging_indent when we actually have content

    for i, value in enumerate(cleaned_values):
        is_first_value = i == 0
        is_last_value = i + 1 == len(cleaned_values)

        if is_first_value:
            # First value - check if it fits on the same line as opening bracket
            test_line = f"{indent}{prefix}[{value}" + ("" if is_last_value else ",")
            if len(test_line) <= MAX_PRINT_WIDTH and is_last_value:
                return f"{test_line}]{comma}"
            else:
                # Start new line with proper indentation
                line = hanging_indent + value + ("" if is_last_value else ",")
        else:
            # Subsequent values
            formatted_value = " " + value + ("" if is_last_value else ",")
            if len(line) + len(formatted_value) <= MAX_PRINT_WIDTH:
                line += formatted_value
            else:
                lines.append(line)
                line = hanging_indent + value + ("" if is_last_value else ",")

        if is_last_value:
            lines.append(line)

    lines.append(f"{indent}]{comma}")
    return "\n".join(lines)


def _format_string(indent: str, prefix: str, values: str, comma: str) -> str:
    result_flat = f'{indent}{prefix}"{values}"{comma}'

    # If it fits on one line, return it
    if len(result_flat) <= MAX_PRINT_WIDTH:
        return result_flat

    # For long strings, force multi-line
    key = prefix.rstrip()
    hanging_indent = indent + (" " * 4)

    # If string has no spaces, use character-by-character wrapping
    if " " not in values:
        available_width = MAX_PRINT_WIDTH - len(hanging_indent) - 2  # -2 for quotes
        lines = [f"{indent}{key}"]

        for i in range(0, len(values), available_width):
            chunk = values[i : i + available_width]
            if i == 0:
                lines.append(f'\n{hanging_indent}"{chunk}')
            elif i + available_width >= len(values):
                lines.append(f'\n{hanging_indent}{chunk}"{comma}')
            else:
                lines.append(f"\n{hanging_indent}{chunk}")

        return "".join(lines)
    else:
        # Word-based wrapping for strings with spaces
        words = values.split(" ")
        lines = [f"{indent}{key}"]
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(f'{hanging_indent}"{test_line}') <= MAX_PRINT_WIDTH - 1:  # -1 for closing quote
                current_line = test_line
            else:
                if current_line:
                    lines.append(f'\n{hanging_indent}"{current_line}')
                current_line = word

        if current_line:
            lines.append(f'\n{hanging_indent}"{current_line}"{comma}')

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
    key = prefix.rstrip()
    hanging_indent = indent + (" " * 4)
    hanging_line = f"{hanging_indent}{flat_dict}{comma}"
    if len(hanging_line) <= MAX_PRINT_WIDTH:
        return f"{indent}{key}\n{hanging_line}"

    # 3. Keep original formatting and let strings inside be processed later
    return f"{indent}{prefix}{values}{comma}"
