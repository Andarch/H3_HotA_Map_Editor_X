import ctypes
import msvcrt
import os
import re
import shutil
import sys
import threading
import time
from enum import Enum
from typing import Union

APPNAME = "H3 HotA Map Editor X"
VERSION = "v0.3.1"
TITLE_VERSION = f"{APPNAME} {VERSION}"
MAX_PRINT_WIDTH = 78
DONE = "DONE"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


class KB(Enum):
    BACKSPACE = 8
    ENTER = 13
    ESC = 27


class Align(Enum):
    LEFT = 1
    CENTER = 2
    MENU = 3
    FLUSH = 4


class Color(Enum):
    RESET = "\033[0m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    INVERTED = "\033[7m"
    STRIKE = "\033[9m"
    DEFAULT = "\033[39m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[35m"
    MAGENTA_FAINT = "\033[95;2m"
    CYAN = "\033[96m"
    CYAN_FAINT = "\033[96;2m"
    WHITE = "\033[97m"
    WHITE_FAINT = "\033[97;2m"
    GREY = "\033[90m"
    GREY_FAINT = "\033[90;2m"


class Sleep(Enum):
    TIC = 0.01
    SHORTER = 0.05
    SHORT = 0.25
    NORMAL = 0.75
    LONG = 1.5


class Text(Enum):
    NORMAL = 1
    INFO = 2
    MENU = 3
    PROMPT = 4
    ACTION = 5
    SPECIAL = 6
    HEADER = 7
    ERROR = 8


map_data = {}
terminal_width = 0

_old_terminal_width = 0
_redrawing_screen = False
_screen_cache = []


def initialize():
    global terminal_width, _old_terminal_width

    print(HIDE_CURSOR, end="", flush=True)

    terminal_width = _old_terminal_width = shutil.get_terminal_size().columns

    mutex_name = APPNAME.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()

    if last_error == 183:
        draw_header()
        xprint(type=Text.ERROR, text="Another instance of the editor is already running.")
        return False

    monitor_thread1 = threading.Thread(target=_monitor_terminal_size, daemon=True)
    monitor_thread1.start()

    return True


def _monitor_terminal_size() -> None:
    global terminal_width, _old_terminal_width, _redrawing_screen

    while True:
        terminal_width = shutil.get_terminal_size().columns

        if terminal_width != _old_terminal_width:
            _old_terminal_width = terminal_width

            if not _redrawing_screen:
                _redrawing_screen = True
                threading.Timer(0, _redraw_screen).start()

        time.sleep(Sleep.SHORTER.value)


def _redraw_screen() -> None:
    global _redrawing_screen

    draw_header()

    for type, text, align, overwrite, skip_line, menu_num, menu_width, menu in _screen_cache:
        xprint(type, text, align, overwrite, skip_line, menu_num, menu_width, menu)

    _redrawing_screen = False


def draw_header() -> None:
    global _screen_cache

    # Clear screen cache if not redrawing the screen
    if not _redrawing_screen:
        _screen_cache = []

    # Clear terminal
    os.system("cls" if os.name == "nt" else "clear")

    # Build header
    header_default = fill_header_row(fill_color=Color.GREY_FAINT.value, fill="#")
    header_appname = fill_header_row(fill_color=Color.GREY_FAINT.value, fill="#", text=APPNAME)
    header_version = fill_header_row(fill_color=Color.GREY_FAINT.value, fill="#", text=VERSION)

    # Build subheader
    mapname = map_data["map_specs"]["map_name"] if map_data else "No map"
    mapfile = map_data["filename"] if map_data else "loaded"
    mapname_color = Color.MAGENTA.value if map_data else Color.MAGENTA_FAINT.value
    subheader_default = fill_header_row(fill_color=Color.WHITE_FAINT.value, fill="-")
    subheader_mapname = f"{mapname_color}{mapname}{Color.RESET.value}"
    subheader_mapfile = f"{Color.MAGENTA_FAINT.value}{mapfile}{Color.RESET.value}"

    # Print header
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=header_default)
    xprint(type=Text.HEADER, text=header_default)
    xprint(type=Text.HEADER, text=header_appname)
    xprint(type=Text.HEADER, text=header_default)
    xprint(type=Text.HEADER, text=header_version)
    xprint(type=Text.HEADER, text=header_default)
    xprint(type=Text.HEADER, text=header_default)

    # Print subheader
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=subheader_default)
    xprint(type=Text.HEADER, text=subheader_mapname)
    xprint(type=Text.HEADER, text=subheader_mapfile)
    xprint(type=Text.HEADER, text=subheader_default)
    xprint(type=Text.HEADER, text="")


def fill_header_row(fill_color: str, fill: str, text: str = "") -> str:
    print_width = MAX_PRINT_WIDTH if terminal_width >= MAX_PRINT_WIDTH else terminal_width

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


def xprint(
    type: int = Text.NORMAL,
    text: str = "",
    align: int = Align.LEFT,
    overwrite: int = 0,
    skip_line: bool = False,
    menu_num: int = -1,
    menu_width: int = 0,
    menu: dict = {},
) -> Union[None, Union[int, str]]:
    def main() -> Union[None, Union[int, str]]:
        global _screen_cache
        if menu:
            return menu_prompt(menu)
        if not _redrawing_screen and type != Text.HEADER:
            _screen_cache.append((type, text, align, overwrite, skip_line, menu_num, menu_width, menu))
        match type:
            case Text.NORMAL:
                if overwrite > 0:
                    time.sleep(Sleep.SHORTER.value)
                    for _ in range(overwrite):
                        print("\033[F\033[K", end="")
                print(align_text(text=f"{Color.WHITE.value}{text}{Color.RESET.value}"))
            case Text.INFO:
                if overwrite > 0:
                    time.sleep(Sleep.SHORTER.value)
                    for _ in range(overwrite):
                        print("\033[F\033[K", end="")
                print(align_text(text=f"{Color.CYAN.value}{text}{Color.RESET.value}"))
            case Text.MENU:
                menu_num_formatted = f"[{Color.YELLOW.value}{str(menu_num)}{Color.RESET.value}]"
                text_formatted = f"{Color.WHITE.value}{text}{Color.RESET.value}"
                print(
                    align_text(align=Align.MENU, text=f"{menu_num_formatted} {text_formatted}", menu_width=menu_width)
                )
            case Text.PROMPT:
                xprint()
                input = string_prompt(align_text(text=f"{Color.YELLOW.value}[{text}] > {Color.WHITE.value}"))
                return input
            case Text.ACTION:
                if overwrite > 0:
                    time.sleep(Sleep.SHORTER.value)
                    for _ in range(overwrite):
                        print("\033[F\033[K", end="")
                print(
                    align_text(text=f"{Color.WHITE.value}{text}{Color.RESET.value}"),
                    end=" ",
                    flush=True,
                )
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
                        if skip_line:
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
            padding = (terminal_width // 2) - (MAX_PRINT_WIDTH // 2)
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

        def print_menu(menu: dict, width: int) -> list[int]:
            valid_keys = [KB.ESC.value]
            for key, value in menu.items():
                if value:
                    valid_keys.append(key)
                    xprint(type=Text.MENU, text=value, menu_num=key, menu_width=width)
                else:
                    xprint()
            xprint()
            return valid_keys

        def detect_key_press(valid_keys: list[int]) -> int:
            while True:
                char = msvcrt.getwch()
                if char.isdigit():
                    num = int(char)
                else:
                    num = ord(char)
                if num in valid_keys:
                    return num

        return main()

    def string_prompt(prompt: str) -> str:
        print(prompt, end="", flush=True)
        print(SHOW_CURSOR, end="", flush=True)
        input_chars = []
        while True:
            char = msvcrt.getwch()
            num = ord(char)
            match num:
                case KB.ENTER.value:
                    if input_chars:
                        print(HIDE_CURSOR, end="", flush=True)
                        xprint()
                        xprint()
                        return "".join(input_chars)
                    continue
                case KB.BACKSPACE.value:
                    if input_chars:
                        input_chars.pop()
                        print("\b \b", end="", flush=True)
                    continue
                case KB.ESC.value:
                    print(HIDE_CURSOR, end="", flush=True)
                    if map_data:
                        return ""
                    print("\r\033[K", end="", flush=True)
                    exit()
                case _:
                    input_chars.append(char)
                    print(char, end="", flush=True)

    return main()


def is_file_writable(filepath: str) -> bool:
    try:
        if os.path.exists(filepath):
            with open(filepath, "r+b"):
                pass
        return True
    except (IOError, OSError, PermissionError):
        xprint(type=Text.ERROR, text="File is open in another program.")
        return False


def wait_for_keypress(suffix: str = " to return to the menu") -> int:
    xprint()
    xprint()
    xprint(text=f"{Color.YELLOW.value + Color.FAINT.value}[Press any key{suffix}]{Color.RESET.value}")
    while True:
        char = msvcrt.getwch()
        if char:
            if char.isdigit():
                num = int(char)
            else:
                num = ord(char)
            return num


def exit() -> None:
    xprint(text="Exiting...")
    xprint()
    time.sleep(Sleep.NORMAL.value)
    os.system("cls" if os.name == "nt" else "clear")
    print(SHOW_CURSOR, end="", flush=True)
    sys.exit(0)
