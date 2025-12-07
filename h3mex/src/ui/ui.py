import shutil
import threading
import time

from src.common import Wait
from src.ui import header
from src.ui.xprint import xprint

MAX_WIDTH = 165

# _terminal_width = shutil.get_terminal_size().columns
width = MAX_WIDTH if shutil.get_terminal_size().columns >= MAX_WIDTH else shutil.get_terminal_size().columns

cache = []
redrawing = False


def monitor_terminal_width():
    monitor_thread1 = threading.Thread(target=_monitor_terminal_width, daemon=True)
    monitor_thread1.start()


def _monitor_terminal_width() -> None:
    global width, redrawing
    old_terminal_cols = 0
    while True:
        terminal_cols = shutil.get_terminal_size().columns
        if terminal_cols != old_terminal_cols:
            old_terminal_cols = terminal_cols
            if not redrawing:
                redrawing = True
                threading.Timer(0, _redraw).start()
        width = MAX_WIDTH if terminal_cols >= MAX_WIDTH else terminal_cols
        time.sleep(Wait.SHORT.value)


def _redraw() -> None:
    global redrawing
    header.draw()
    for type, text, align, overwrite, skip_line, menu_num, menu_width, menu in cache:
        xprint(type, text, align, overwrite, skip_line, menu_num, menu_width, menu)
    redrawing = False
