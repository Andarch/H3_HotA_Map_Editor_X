import shutil
import threading
import time

from src.common import Wait
from src.ui import header
from src.ui.xprint import xprint


def _set_width() -> None:
    global width
    while True:
        width = MAX_WIDTH if terminal_width >= MAX_WIDTH else terminal_width
        time.sleep(Wait.TIC.value)


MAX_WIDTH = 165

terminal_width = shutil.get_terminal_size().columns
old_terminal_width = terminal_width
monitor_thread1 = threading.Thread(target=_set_width, daemon=True)
monitor_thread1.start()

cache = []
redrawing = False


def monitor_terminal_width():
    monitor_thread2 = threading.Thread(target=_monitor_terminal_width, daemon=True)
    monitor_thread2.start()


def _monitor_terminal_width() -> None:
    global width, redrawing, terminal_width, old_terminal_width
    while True:
        terminal_width = shutil.get_terminal_size().columns
        if terminal_width != old_terminal_width:
            old_terminal_width = terminal_width
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
