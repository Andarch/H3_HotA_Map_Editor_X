import shutil
import threading
import time

from src.common import Wait
from src.ui import header
from src.ui.xprint import xprint

MAX_WIDTH = 80

cache = []
redrawing = False
width = 0


def monitor_width():
    monitor_thread1 = threading.Thread(target=_monitor_width, daemon=True)
    monitor_thread1.start()


def _monitor_width() -> None:
    global width, redrawing
    old_width = 0
    while True:
        width = shutil.get_terminal_size().columns
        if width != old_width:
            old_width = width
            if not redrawing:
                redrawing = True
                threading.Timer(0, _redraw).start()
        time.sleep(Wait.SHORT.value)


def _redraw() -> None:
    global redrawing
    header.draw()
    for type, text, align, overwrite, skip_line, menu_num, menu_width, menu in cache:
        xprint(type, text, align, overwrite, skip_line, menu_num, menu_width, menu)
    redrawing = False
