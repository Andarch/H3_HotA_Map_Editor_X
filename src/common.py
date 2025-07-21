# region Imports

import ctypes
from enum import Enum
import msvcrt
import os
import re
import shutil
import sys
import threading
import time
from typing import Union

# endregion

# region Constants/Enums

TITLE = "H3 HotA Map Editor X"
VERSION = "v0.3.1"
TITLE_VERSION = f"{TITLE} {VERSION}"
PRINT_WIDTH = 75
DONE = "DONE"
# MAP1 = "Map 1"
# MAP2 = "Map 2"

class KB(Enum):
    BACKSPACE = 8
    ENTER = "\r"
    ESC = 27

class Align(Enum):
    LEFT   = 1
    CENTER = 2
    MENU   = 3
    FLUSH  = 4

class Color(Enum):
    RESET     = "\033[0m"
    FAINT     = "\033[2m"
    ITALIC    = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK     = "\033[5m"
    INVERTED  = "\033[7m"
    STRIKE    = "\033[9m"
    DEFAULT   = "\033[39m"
    RED       = "\033[91m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    BLUE      = "\033[94m"
    MAGENTA2  = "\033[35m"
    MAGENTA   = "\033[95m"
    CYAN      = "\033[96m"
    WHITE     = "\033[97m"
    GREY      = "\033[90m"

class Sleep(Enum):
    TIC    = 0.01
    SHORTER  = 0.05
    SHORT = 0.25
    NORMAL = 0.75
    LONG   = 1.5

class Text(Enum):
    NORMAL  = 1
    INFO    = 2
    MENU    = 3
    PROMPT  = 4
    ACTION  = 5
    SPECIAL = 6
    HEADER  = 7
    ERROR   = 8

# endregion

# region Global Variables

map_data = {}
screen_content = []
terminal_width = 0
old_terminal_width = 0
redraw_scheduled = False
is_redrawing = False

# endregion

def initialize():
    global terminal_width, old_terminal_width
    terminal_width = old_terminal_width = get_terminal_width()
    hide_cursor(True)
    mutex_name = TITLE.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        draw_header()
        xprint(type=Text.ERROR, text="Another instance of the editor is already running.")
        return False
    monitor_thread1 = threading.Thread(target = monitor_terminal_size, daemon = True)
    monitor_thread1.start()
    return True

def hide_cursor(hide: bool) -> None:
    if hide: print("\033[?25l", end = "", flush = True)
    else: print("\033[?25h", end = "", flush = True)

def monitor_terminal_size() -> None:
    global terminal_width, old_terminal_width, redraw_scheduled
    while True:
        terminal_width = get_terminal_width()
        if terminal_width != old_terminal_width:
            old_terminal_width = terminal_width
            if not redraw_scheduled:
                redraw_scheduled = True
                threading.Timer(0, redraw_screen).start()
        time.sleep(Sleep.SHORTER.value)

def get_terminal_width() -> int:
    return shutil.get_terminal_size().columns

def draw_header(new_screen: bool = True) -> None:
    global screen_content, terminal_width
    if new_screen:
        screen_content = []
    clear_screen()

    # Set up header
    fill1_symbol = "#"
    fill1_color = Color.GREY.value + Color.FAINT.value
    title_color = Color.CYAN.value
    headerA_colors = (fill1_color, title_color)
    fill1_row = create_filled_row(fill1_symbol, headerA_colors)
    title_row = create_filled_row(fill1_symbol, headerA_colors, TITLE)
    version_row = create_filled_row(fill1_symbol, headerA_colors, VERSION)

    # Set up subheader
    map1 = map_data["Map 1"]
    map2 = map_data["Map 2"]
    headerB1_color1A = Color.MAGENTA.value
    headerB1_color1B = Color.MAGENTA2.value
    headerB2_color1 = Color.YELLOW.value
    fill2_symbol = "-"
    fill2_color = Color.GREY.value
    headerB_colors = (fill2_color, fill2_color)
    fill2_row = create_filled_row(fill2_symbol, headerB_colors)

    if map1:
        map1_row1 = f"{headerB1_color1A}{map1['map_specs']['name']}{Color.RESET.value}"
        map1_row2 = f"{headerB1_color1B}{{{map1['filename']}}}{Color.RESET.value}"
        if not map2:
            map2_row1 = ""
            map2_row2 = ""
        else:
            map2_row1 = f"{headerB1_color1A}{map2['map_specs']['name']}{Color.RESET.value}"
            map2_row2 = f"{headerB1_color1B}{{{map2['filename']}}}{Color.RESET.value}"
            if terminal_width >= PRINT_WIDTH:
                cell_width = PRINT_WIDTH // 2 + 6
            else:
                cell_width = terminal_width // 2 + 6
            map1_row1 = map1_row1.center(cell_width)
            map1_row2 = map1_row2.center(cell_width)
            map2_row1 = map2_row1.center(cell_width)
            map2_row2 = map2_row2.center(cell_width)
            final_row1 = f"{map1_row1} | {map2_row1}"
            final_row2 = f"{map1_row2} | {map2_row2}"
    else:
        map1_row1 = f"{headerB2_color1}Use the number keys on{Color.RESET.value}"
        map1_row2 = f"{headerB2_color1}your keyboard to navigate{Color.RESET.value}"
        map2_row1 = ""
        map2_row2 = ""

    if not map2:
        final_row1 = map1_row1
        final_row2 = map1_row2
    else:
        final_row1 = f"{map1_row1}{fill2_color} | {map2_row1}"
        final_row2 = f"{map1_row2}{fill2_color} | {map2_row2}"

    # Print header
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=title_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=version_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=fill1_row)

    # Print subheader
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=fill2_row)
    xprint(type=Text.HEADER, text=final_row1)
    xprint(type=Text.HEADER, text=final_row2)
    xprint(type=Text.HEADER, text=fill2_row)
    xprint(type=Text.HEADER, text="")

def redraw_screen() -> None:
    global redraw_scheduled, is_redrawing, screen_content
    redraw_scheduled = False
    is_redrawing = True
    draw_header(False)
    for type, text, align, menu_num, menu_width in screen_content:
        xprint(type, text, align, menu_num, menu_width)
    is_redrawing = False

def clear_screen() -> None:
    global screen_content
    os.system("cls" if os.name == "nt" else "clear")

def create_filled_row(symbol: str, colors=(Color.DEFAULT.value, Color.DEFAULT.value), text="") -> str:
    global terminal_width
    if not text:
        if terminal_width >= PRINT_WIDTH:
            filler_row = f"{colors[0]}{symbol}" * PRINT_WIDTH + Color.RESET.value
        else:
            filler_row = f"{colors[0]}{symbol}" * terminal_width + Color.RESET.value
        return filler_row
    else:
        text_length = len(text)
        if terminal_width >= PRINT_WIDTH:
            fill_length = PRINT_WIDTH - (text_length + 2)
        else:
            fill_length = terminal_width - (text_length + 2)
        row_left = f"{colors[0]}{symbol}" * (fill_length // 2) + Color.RESET.value
        row_right = f"{colors[0]}{symbol}" * (fill_length // 2) + Color.RESET.value
        if fill_length % 2 != 0:
            row_right += f"{colors[0]}{symbol}" + Color.RESET.value
        text_row = f"{row_left} {colors[1]}{text}{Color.RESET.value} {row_right}"
        return text_row

# def get_map_key() -> str:
#     if not map_data["Map 2"]:
#         return "Map 1"

def xprint(type=Text.NORMAL, text="", align=Align.LEFT, overwrite=0, skipline=False, menu_num=-1, menu_width=0, menu={}) -> Union[None, Union[int, str]]:
    def main() -> Union[None, Union[int, str]]:
        global screen_content, is_redrawing
        if menu: return menu_prompt(menu)
        if not is_redrawing and type != Text.HEADER:
            screen_content.append((type, text, align, menu_num, menu_width))
        match type:
            case Text.NORMAL:
                if overwrite > 0:
                    time.sleep(Sleep.SHORTER.value)
                    for _ in range(overwrite):
                        print("\033[F\033[K", end="")
                print(align_text(text=f"{Color.WHITE.value}{text}{Color.RESET.value}"))
            case Text.INFO:
                print(align_text(text=f"{Color.CYAN.value}{text}{Color.RESET.value}"))
            case Text.MENU:
                print(align_text(
                    align=Align.MENU,
                    text=f"[{Color.YELLOW.value}{str(menu_num)}{Color.RESET.value}] {Color.WHITE.value}{text}{Color.RESET.value}",
                    menu_width=menu_width
                ))
            case Text.PROMPT:
                xprint()
                input = string_prompt(align_text(text=f"{Color.YELLOW.value}[{text}] > {Color.WHITE.value}"))
                return input
            case Text.ACTION:
                if overwrite > 0:
                    time.sleep(Sleep.SHORTER.value)
                    for _ in range(overwrite):
                        print("\033[F\033[K", end="")
                print(align_text(text=f"{Color.WHITE.value}{text}{Color.RESET.value}"), end = " ", flush = True)
                time.sleep(Sleep.NORMAL.value)
            case Text.SPECIAL:
                print(f"{Color.GREEN.value}{text}{Color.RESET.value}")
                time.sleep(Sleep.NORMAL.value)
            case Text.HEADER:
                print(align_text(align=Align.CENTER, text=text))
            case Text.ERROR:
                if overwrite > 0:
                    time.sleep(Sleep.SHORTER.value)
                    for _ in range(overwrite):
                        print("\033[F\033[K", end="")
                match align:
                    case Align.LEFT:
                        if skipline:
                            xprint()
                        print(align_text(text=f"{Color.RED.value}Error: {text}{Color.RESET.value}"))
                    case Align.FLUSH:
                        print(f"{Color.RED.value}Error: {text}{Color.RESET.value}")
                time.sleep(Sleep.LONG.value)
        return None

    def align_text(align=Align.LEFT, text="", menu_width=0) -> str:
        global terminal_width
        stripped_text = strip_ansi_codes(str(text))
        text_length = len(stripped_text)
        if align == Align.LEFT:
            padding = (terminal_width // 2) - (PRINT_WIDTH // 2)
            return " " * padding + str(text)
        elif align == Align.CENTER:
            padding = terminal_width // 2 - text_length // 2
            return " " * padding + str(text)
        elif align == Align.MENU:
            padding = terminal_width // 2 - menu_width // 2 - 2
            return " " * padding + str(text)

    def strip_ansi_codes(text: str) -> str:
        ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", text)

    def menu_prompt(menu: dict) -> str:
        def main() -> str:
            draw_header()
            width = get_menu_width(menu)
            valid_keys = print_menu(menu, width)
            input = detect_key_press(valid_keys)
            return input
        def get_menu_width(menu: dict) -> int:
            width = 0
            for _, text in menu.items():
                stripped_text = strip_ansi_codes(text)
                text_length = len(stripped_text)
                if text_length > width:
                    width = text_length
            return width
        def print_menu(menu: dict, width: int) -> str:
            valid_keys = ""
            for key, value in menu.items():
                if value:
                    valid_keys += str(key)
                    xprint(
                        type=Text.MENU,
                        text=value,
                        menu_num=key,
                        menu_width=width
                    )
                else:
                    xprint()
            xprint()
            return valid_keys
        def detect_key_press(valid_keys: str) -> str:
            while True:
                char = msvcrt.getwch()
                if char in valid_keys:
                    return int(char)
                elif ord(char) == KB.ESC.value:
                    return KB.ESC.value
        return main()

    def string_prompt(prompt: str) -> str:
        print(prompt, end = "", flush = True)
        input_chars = []
        while True:
            char = msvcrt.getwch()
            if char == KB.ENTER.value:
                xprint()
                xprint()
                return "".join(input_chars)
            elif ord(char) == KB.BACKSPACE.value:
                if input_chars:
                    input_chars.pop()
                    print("\b \b", end="", flush=True)
            elif ord(char) == KB.ESC.value:
                return ""
            else:
                input_chars.append(char)
                print(char, end="", flush=True)

    return main()


def is_file_writable(filepath: str) -> bool:
    try:
        # Try to open the file in write mode
        if os.path.exists(filepath):
            with open(filepath, 'r+b') as f:
                pass
        return True
    except (IOError, OSError, PermissionError):
        xprint(type=Text.ERROR, text="File is open in another program.")
        return False


def press_any_key() -> None:
    xprint()
    xprint()
    xprint(text=f"{Color.YELLOW.value}Press any key to return to the menu...{Color.RESET.value}")
    while True:
        if msvcrt.getwch():
            break


def exit() -> None:
    xprint()
    xprint(text="Exiting...")
    time.sleep(Sleep.NORMAL.value)
    xprint(text=Color.RESET.value)
    sys.exit(0)