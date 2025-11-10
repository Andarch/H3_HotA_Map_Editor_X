import msvcrt
import os
import sys
import time

from src.common import Color, Cursor, MsgType, Wait
from src.ui import header
from src.ui.xprint import xprint


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


def quit() -> None:
    header.draw()
    xprint(text="Exiting…")
    xprint()
    time.sleep(Wait.NORMAL.value)
    os.system("cls" if os.name == "nt" else "clear")
    print(Cursor.SHOW, end="", flush=True)
    sys.exit(0)
