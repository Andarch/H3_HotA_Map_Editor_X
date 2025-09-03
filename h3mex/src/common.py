import msvcrt
import os
import sys
import time
from enum import Enum, StrEnum

from src.ui.xprint import xprint


class App(StrEnum):
    NAME = "H3 HotA Map Editor X"
    VERSION = "v0.3.1"


class Cursor(StrEnum):
    HIDE = "\x1b[?25l"
    SHOW = "\x1b[?25h"
    # RESET_CURRENT = "\r\x1b[K"
    RESET_PREVIOUS = "\x1b[F\x1b[K"


class Keypress(StrEnum):
    BACKSPACE = "\x08"
    ENTER = "\r"
    ESC = "\x1b"


class Align(Enum):
    LEFT = 1
    CENTER = 2
    MENU = 3
    FLUSH = 4


class Color(StrEnum):
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    FAINT = "\x1b[2m"
    ITALIC = "\x1b[3m"
    UNDERLINE = "\x1b[4m"
    BLINK = "\x1b[5m"
    INVERTED = "\x1b[7m"
    STRIKE = "\x1b[9m"
    BOLD_OFF = "\x1b[22m"
    DEFAULT = "\x1b[39m"
    RED = "\x1b[91m"
    GREEN = "\x1b[92m"
    YELLOW = "\x1b[93m"
    BLUE = "\x1b[94m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[96m"
    WHITE = "\x1b[97m"
    GREY = "\x1b[90m"


class Wait(float, Enum):
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
    DONE = 6
    HEADER = 7
    ERROR = 8


map_data = {}


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
        keypress = msvcrt.getwch()
        return keypress


def exit() -> None:
    xprint(text="Exiting…")
    xprint()
    time.sleep(Wait.NORMAL.value)
    os.system("cls" if os.name == "nt" else "clear")
    print(Cursor.SHOW, end="", flush=True)
    sys.exit(0)
