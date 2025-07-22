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


APPNAME = "H3 HotA Map Editor X"
VERSION = "v0.3.1"
TITLE_VERSION = f"{APPNAME} {VERSION}"
MAX_PRINT_WIDTH = 75
DONE = "DONE"


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
    MAGENTA2  = "\033[35m"
    DEFAULT   = "\033[39m"
    RED       = "\033[91m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    BLUE      = "\033[94m"
    MAGENTA1  = "\033[95m"
    CYAN      = "\033[96m"
    WHITE     = "\033[97m"
    GREY1     = "\033[90m"
    GREY2     = "\033[90;2m"


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


map_data = {}

_terminal_width     = 0
_old_terminal_width = 0
_redrawing_screen   = False
_screen_cache       = []


def initialize():
    global _terminal_width, _old_terminal_width

    HIDE_CURSOR = "\033[?25l"
    print(HIDE_CURSOR, end = "", flush = True)

    _terminal_width = _old_terminal_width = shutil.get_terminal_size().columns

    mutex_name = APPNAME.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()

    if last_error == 183:
        draw_header()
        xprint(type=Text.ERROR, text="Another instance of the editor is already running.")
        return False

    monitor_thread1 = threading.Thread(target = monitor_terminal_size, daemon = True)
    monitor_thread1.start()

    return True


def monitor_terminal_size() -> None:
    global _terminal_width, _old_terminal_width, _redrawing_screen

    while True:
        _terminal_width = shutil.get_terminal_size().columns

        if _terminal_width != _old_terminal_width:
            _old_terminal_width = _terminal_width

            if not _redrawing_screen:
                _redrawing_screen = True
                threading.Timer(0, redraw_screen).start()

        time.sleep(Sleep.SHORTER.value)


def redraw_screen() -> None:
    global _redrawing_screen

    draw_header()

    for type, text, align, menu_num, menu_width in _screen_cache:
        xprint(type, text, align, menu_num, menu_width)

    _redrawing_screen = False


def draw_header() -> None:
    global _screen_cache

    # Clear screen cache if not redrawing the screen
    if not _redrawing_screen:
        _screen_cache = []

    # Clear terminal
    os.system("cls" if os.name == "nt" else "clear")

    # Build header
    header_pattern_row = fill_header_row(fill_color=Color.GREY2.value, fill="#")
    header_appname_row = fill_header_row(fill_color=Color.GREY2.value, fill="#", text=APPNAME)
    header_version_row = fill_header_row(fill_color=Color.GREY2.value, fill="#", text=VERSION)

    # Build subheader
    mapname = map_data["map_specs"]["map_name"] if map_data else "No map"
    mapfile = map_data["filename"] if map_data else "loaded"
    subheader_pattern_row = fill_header_row(fill_color=Color.GREY1.value, fill="-")
    subheader_mapname_row = f"{Color.MAGENTA1.value}{mapname}{Color.RESET.value}"
    subheader_mapfile_row = f"{Color.MAGENTA2.value}{mapfile}{Color.RESET.value}"

    # Print header
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=header_pattern_row)
    xprint(type=Text.HEADER, text=header_pattern_row)
    xprint(type=Text.HEADER, text=header_appname_row)
    xprint(type=Text.HEADER, text=header_pattern_row)
    xprint(type=Text.HEADER, text=header_version_row)
    xprint(type=Text.HEADER, text=header_pattern_row)
    xprint(type=Text.HEADER, text=header_pattern_row)

    # Print subheader
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=subheader_pattern_row)
    xprint(type=Text.HEADER, text=subheader_mapname_row)
    xprint(type=Text.HEADER, text=subheader_mapfile_row)
    xprint(type=Text.HEADER, text=subheader_pattern_row)
    xprint(type=Text.HEADER, text="")


def fill_header_row(fill_color: str, fill: str, text: str = "") -> str:
    print_width = MAX_PRINT_WIDTH if _terminal_width >= MAX_PRINT_WIDTH else _terminal_width

    if text == "":
        row = f"{fill_color}{fill}" * print_width + Color.RESET.value
    else:
        fill_length = print_width - (len(text) + 2)

        row_left = f"{fill_color}{fill}" * (fill_length // 2) + Color.RESET.value
        row_right = f"{fill_color}{fill}" * (fill_length // 2) + Color.RESET.value

        if fill_length % 2 != 0:
            row_right += f"{fill_color}{fill}" + Color.RESET.value

        row = f"{row_left} {Color.CYAN.value}{text}{Color.RESET.value} {row_right}"

    return row


def xprint(type=Text.NORMAL, text="", align=Align.LEFT, overwrite=0, skipline=False, menu_num=-1, menu_width=0, menu={}) -> Union[None, Union[int, str]]:
    def main() -> Union[None, Union[int, str]]:
        global _screen_cache
        if menu: return menu_prompt(menu)
        if not _redrawing_screen and type != Text.HEADER:
            _screen_cache.append((type, text, align, menu_num, menu_width))
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
        global _terminal_width
        stripped_text = strip_ansi_codes(str(text))
        text_length = len(stripped_text)
        if align == Align.LEFT:
            padding = (_terminal_width // 2) - (MAX_PRINT_WIDTH // 2)
            return " " * padding + str(text)
        elif align == Align.CENTER:
            padding = _terminal_width // 2 - text_length // 2
            return " " * padding + str(text)
        elif align == Align.MENU:
            padding = _terminal_width // 2 - menu_width // 2 - 2
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
            with open(filepath, "r+b") as f:
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