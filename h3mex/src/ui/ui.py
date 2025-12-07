import os
import shutil
import threading
import time

from src.common import Cursor, Wait
from src.ui import header
from src.ui.xprint import xprint


def initialize():
    global MAX_PRINT_WIDTH, print_width, terminal_width, cache, redrawing

    MAX_PRINT_WIDTH = 165

    terminal_width = shutil.get_terminal_size().columns
    print_width = MAX_PRINT_WIDTH if terminal_width >= MAX_PRINT_WIDTH else terminal_width
    cache = []
    redrawing = False

    print(Cursor.HIDE, end="", flush=True)
    thread = threading.Thread(target=_set_width, daemon=True)
    thread.start()


def uninitialize():
    os.system("cls" if os.name == "nt" else "clear")
    print(Cursor.SHOW, end="", flush=True)


def _set_width() -> None:
    global print_width, terminal_width, cache, redrawing

    _old_terminal_width = terminal_width

    while True:
        terminal_width = shutil.get_terminal_size().columns
        print_width = MAX_PRINT_WIDTH if terminal_width >= MAX_PRINT_WIDTH else terminal_width
        if terminal_width != _old_terminal_width:
            _old_terminal_width = terminal_width
            if not redrawing:
                redrawing = True
                threading.Timer(0, _redraw).start()
        time.sleep(Wait.TIC.value)


def _redraw() -> None:
    global redrawing

    header.draw()
    for type, text, align, overwrite, skip_line, menu_num, menu_width, menu in cache:
        xprint(type, text, align, overwrite, skip_line, menu_num, menu_width, menu)

    redrawing = False
