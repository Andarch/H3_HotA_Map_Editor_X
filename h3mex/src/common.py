import ctypes
import msvcrt
import os
import re
import shutil
import sys
import threading
import time
from enum import Enum, StrEnum

from src.ui.menu import Menu

APPNAME = "H3 HotA Map Editor X"
VERSION = "v0.3.1"
MAX_PRINT_WIDTH = 80
DONE = "DONE"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
ERASE_LINE = "\033[F\033[K"


class KB(StrEnum):
    BACKSPACE = "\x08"
    ENTER = "\r"
    ESC = "\x1b"


class Align(Enum):
    LEFT = 1
    CENTER = 2
    MENU = 3
    FLUSH = 4


class Color(StrEnum):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    INVERTED = "\033[7m"
    STRIKE = "\033[9m"
    BOLD_OFF = "\033[22m"
    DEFAULT = "\033[39m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[35m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GREY = "\033[90m"


class Sleep(Enum):
    TIC = 0.01
    SHORT = 0.05
    NORMAL = 0.75
    LONG = 1.5


class MsgType(Enum):
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
        xprint(type=MsgType.ERROR, text="Another instance of the editor is already running.")
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

        time.sleep(Sleep.SHORT.value)


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
    header_default = make_header_line(fill_color=(Color.FAINT + Color.GREY), fill="#")
    header_appname = make_header_line(fill_color=(Color.FAINT + Color.GREY), fill="#", text=APPNAME)
    header_version = make_header_line(fill_color=(Color.FAINT + Color.GREY), fill="#", text=VERSION)

    # Build subheader
    subheader_filled = make_header_line(fill_color=(Color.FAINT + Color.WHITE), fill="-")

    subtext1 = map_data["general"]["map_name"] if map_data else "No map"
    subtext1_color = Color.MAGENTA if map_data else Color.FAINT + Color.MAGENTA
    subheader_line1 = f"{subtext1_color}{subtext1}{Color.RESET}"

    subtext2 = map_data["filename"] if map_data else "loaded"
    subheader_line2 = f"{Color.FAINT + Color.MAGENTA}{subtext2}{Color.RESET}"

    # Print header
    # xprint(type=Text.HEADER, text="")
    # xprint(type=Text.HEADER, text="")
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_appname)
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_version)
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_default)

    # Print subheader
    xprint(type=MsgType.HEADER, text="")
    xprint(type=MsgType.HEADER, text=subheader_filled)
    xprint(type=MsgType.HEADER, text=subheader_line1)
    xprint(type=MsgType.HEADER, text=subheader_line2)
    xprint(type=MsgType.HEADER, text=subheader_filled)
    xprint(type=MsgType.HEADER, text="")


def make_header_line(fill_color: str, fill: str, text: str = "") -> str:
    print_width = MAX_PRINT_WIDTH if terminal_width >= MAX_PRINT_WIDTH else terminal_width

    if text == "":
        row = fill_color + (fill * print_width) + Color.RESET
    else:
        fill_length = print_width - (len(text) + 2)

        row_left = fill_color + (fill * (fill_length // 2)) + Color.RESET
        if fill_length % 2 == 0:
            row_right = row_left
        else:
            row_right = fill_color + (fill * ((fill_length // 2) + 1)) + Color.RESET

        row = f"{row_left} {Color.CYAN}{text}{Color.RESET} {row_right}"

    return row


def xprint(
    type: int = MsgType.NORMAL,
    text: str = "",
    align: int = Align.LEFT,
    overwrite: int = 0,
    skip_line: bool = False,
    menu_num: int = -1,
    menu_width: int = 0,
    menu: tuple[str, list] = None,
) -> None | str:
    def main() -> None | str:
        global _screen_cache
        if menu:
            return menu_prompt(menu[0], menu[1])
        if not _redrawing_screen and type != MsgType.HEADER:
            _screen_cache.append((type, text, align, overwrite, skip_line, menu_num, menu_width, menu))
        if overwrite > 0:
            _overwrite(overwrite)
        match type:
            case MsgType.NORMAL:
                print(align_text(align=align, text=f"{Color.WHITE}{text}{Color.RESET}"))
            case MsgType.INFO:
                print(align_text(text=f"{Color.CYAN}{text}{Color.RESET}"))
            case MsgType.MENU:
                menu_num_formatted = f"[{Color.YELLOW}{str(menu_num)}{Color.RESET}]"
                text_formatted = f"{Color.WHITE}{text}{Color.RESET}"
                print(
                    align_text(align=Align.MENU, text=f"{menu_num_formatted} {text_formatted}", menu_width=menu_width)
                )
            case MsgType.PROMPT:
                xprint()
                input = string_prompt(align_text(text=f"{Color.YELLOW}[{text}] > {Color.WHITE}"))
                return input
            case MsgType.ACTION:
                print(
                    align_text(text=f"{Color.WHITE}{text}{Color.RESET}"),
                    end=" ",
                    flush=True,
                )
                time.sleep(Sleep.NORMAL.value)
            case MsgType.SPECIAL:
                print(f"{Color.GREEN}{text}{Color.RESET}")
                time.sleep(Sleep.NORMAL.value)
            case MsgType.HEADER:
                print(align_text(align=Align.CENTER, text=text))
            case MsgType.ERROR:
                match align:
                    case Align.LEFT:
                        if skip_line:
                            xprint()
                        print(align_text(text=f"{Color.RED}Error: {text}{Color.RESET}"))
                    case Align.FLUSH:
                        print(f"{Color.RED}Error: {text}{Color.RESET}")
                time.sleep(Sleep.LONG.value)
        return None

    def _overwrite(overwrite: int) -> None:
        time.sleep(Sleep.SHORT.value)
        for _ in range(overwrite):
            print(ERASE_LINE, end="")

    def align_text(align=Align.LEFT, text="", menu_width=0) -> str:
        global terminal_width
        cleaned_text = clean(str(text))
        text_length = len(cleaned_text)
        if align == Align.LEFT:
            padding = (terminal_width // 2) - (MAX_PRINT_WIDTH // 2)
            return " " * padding + str(text)
        elif align == Align.CENTER:
            padding = terminal_width // 2 - text_length // 2
            return " " * padding + str(text)
        elif align == Align.MENU:
            padding = terminal_width // 2 - menu_width // 2
            return " " * padding + str(text)

    def menu_prompt(name: str, items: list) -> str:
        def main() -> str:
            draw_header()
            width = get_menu_width(items)
            valid_keys = print_menu(name, items, width)
            keypress = detect_key_press(valid_keys)
            return keypress

        def get_menu_width(items: list) -> int:
            width = 0
            for item in items:
                if item is None:
                    continue
                text = clean(item[1])
                w = len(text)
                if w > width:
                    width = w
            return width

        def print_menu(name: str, items: list, width: int) -> list[str]:
            valid_keys = [] if items == Menu.MAIN["menus"][0] else [KB.ESC]
            xprint(text=f"{name}\n", align=Align.CENTER)
            for item in items:
                if item:
                    valid_keys.append(item[0])
                    xprint(type=MsgType.MENU, text=item[1], menu_num=item[0], menu_width=width)
                else:
                    xprint()
            xprint()
            return valid_keys

        def detect_key_press(valid_keys: list[str]) -> str:
            while True:
                key = msvcrt.getwch()
                if key in valid_keys:
                    return key

        return main()

    def string_prompt(prompt: str) -> str:
        print(prompt, end="", flush=True)
        print(SHOW_CURSOR, end="", flush=True)
        input_chars = []
        while True:
            char = msvcrt.getwch()
            num = ord(char)
            match num:
                case KB.ENTER:
                    if input_chars:
                        print(HIDE_CURSOR, end="", flush=True)
                        xprint()
                        xprint()
                        return "".join(input_chars)
                    continue
                case KB.BACKSPACE:
                    if input_chars:
                        input_chars.pop()
                        print("\b \b", end="", flush=True)
                    continue
                case KB.ESC:
                    print(HIDE_CURSOR, end="", flush=True)
                    if map_data:
                        return ""
                    print("\r\033[K", end="", flush=True)
                    exit()
                case _:
                    input_chars.append(char)
                    print(char, end="", flush=True)

    def clean(text: str) -> str:
        # Remove ANSI escape codes
        ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
        text = ansi_escape.sub("", text)
        # Remove control characters except space (preserve visible spaces)
        invisible = re.compile(r"[\x00-\x1F\x7F]")
        return invisible.sub("", text)

    return main()


def is_file_writable(filepath: str) -> bool:
    try:
        if os.path.exists(filepath):
            with open(filepath, "r+b"):
                pass
        return True
    except (IOError, OSError, PermissionError):
        xprint(type=MsgType.ERROR, text="File is open in another program.")
        return False


def wait_for_keypress(suffix: str = " to return to the menu") -> int:
    xprint()
    xprint()
    xprint(text=f"{Color.YELLOW + Color.FAINT}[Press any key{suffix}]{Color.RESET}")
    while True:
        return msvcrt.getwch()


def exit() -> None:
    xprint(text="Exiting...")
    xprint()
    time.sleep(Sleep.NORMAL.value)
    os.system("cls" if os.name == "nt" else "clear")
    print(SHOW_CURSOR, end="", flush=True)
    sys.exit(0)
