from enum import Enum
import ctypes
import keyboard
import pygetwindow as gw
import os
import shutil
import threading
import time

class ALIGN(Enum):
    LEFT   = "LEFT"
    CENTER = "CENTER"

class CLR:
    RESET   = "\033[0m"
    NO_BOLD = "\033[22m"
    DEFAULT = "\033[39m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"

class MSG(Enum):
    NORMAL  = "NORMAL"
    INFO    = "INFO"
    MENU    = "MENU"
    PROMPT  = "PROMPT"
    ACTION  = "ACTION"
    SPECIAL = "SPECIAL"
    ERROR   = "ERROR"

class SLEEP:
    TIC    = 0.01
    SHORT  = 0.05
    NORMAL = 0.75
    LONG   = 1.5

TITLE = "H3 HotA Map Editor X v0.3.1"
PRINT_WIDTH = 75
PRINT_OFFSET = 37
DONE = "DONE"

screen_content = []
previous_width = None
redraw_scheduled = False
is_redrawing = False
previous_key = ""

def initialize():
    global previous_width
    previous_width = get_terminal_width()
    hide_cursor(True)
    mutex_name = "H3_HotA_Map_Editor_X"
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        start_new_screen()
        xprint(type = MSG.ERROR, text = "Another instance of the editor is already running.", flush = False)
        return False
    monitor_thread = threading.Thread(target = monitor_terminal_size, daemon = True)
    monitor_thread.start()
    return True

def monitor_terminal_size() -> None:
    global previous_width, redraw_scheduled
    while True:
        current_width = get_terminal_width()
        if current_width != previous_width:
            previous_width = current_width
            if not redraw_scheduled:
                redraw_scheduled = True
                threading.Timer(0, redraw_screen).start()
        time.sleep(SLEEP.SHORT)

def get_terminal_width() -> int:
    return shutil.get_terminal_size().columns

def hide_cursor(hide: bool) -> None:
    if hide:
        print("\033[?25l", end = "", flush = True)
    else:
        print("\033[?25h", end = "", flush = True)

def xprint(type = MSG.NORMAL, text = "", menu_item = -1, flush = False) -> None:
    global screen_content, is_redrawing
    if not is_redrawing:
        screen_content.append((type, text, menu_item, flush))
    match type:
        case MSG.NORMAL:
            print(align_text(text = text))
        case MSG.INFO:
            print(align_text(text = f"{CLR.CYAN}{text}{CLR.RESET}"))
        case MSG.MENU:
            print(align_text(text = f"[{CLR.YELLOW}{str(menu_item)}{CLR.RESET}] {CLR.WHITE}{text}{CLR.RESET}"))
        case MSG.PROMPT:
            input = prompt_input(align_text(text = f"{CLR.YELLOW}[{text}] > {CLR.WHITE}"))
            return input
        case MSG.ACTION:
            print(align_text(text = f"{CLR.WHITE}{text}{CLR.RESET}"), end = " ", flush = True)
            time.sleep(SLEEP.NORMAL)
        case MSG.SPECIAL:
            print(f"{CLR.GREEN}{text}{CLR.RESET}")
            time.sleep(SLEEP.NORMAL)
        case MSG.ERROR:
            if(not flush):
                xprint()
                print(align_text(text = f"{CLR.RED}Error: {text}{CLR.RESET}"))
            else:
                print(f"{CLR.RED}Error: {text}{CLR.RESET}")
            time.sleep(SLEEP.LONG)

def align_text(align = ALIGN.LEFT, text = "") -> str:
    terminal_width = get_terminal_width()
    if align == ALIGN.LEFT:
        padding = terminal_width // 2 - PRINT_OFFSET
    else:
        padding = (terminal_width - len(text)) // 2
    return " " * padding + str(text)

def start_new_screen() -> None:
    global screen_content
    screen_content = []
    clear_screen()
    # Set up title
    rowA_fill = f"{CLR.GREY}#" * PRINT_WIDTH + CLR.RESET
    rowB_fill = f"{CLR.GREY}#" * ((PRINT_WIDTH - (len(TITLE) + 2)) // 2) + CLR.RESET
    rowB_title = f"{rowB_fill} {CLR.CYAN}{TITLE}{CLR.RESET} {rowB_fill}"
    # Print title
    xprint()
    xprint()
    xprint(text = rowA_fill)
    xprint(text = rowA_fill)
    xprint(text = rowB_title)
    xprint(text = rowA_fill)
    xprint(text = rowA_fill)
    xprint()
    xprint()

def redraw_screen() -> None:
    global redraw_scheduled, is_redrawing, screen_content
    redraw_scheduled = False
    is_redrawing = True
    clear_screen()
    for type, text, menu_item, flush in screen_content:
        xprint(type, text, menu_item, flush)
    is_redrawing = False

def clear_screen() -> None:
    global screen_content
    os.system("cls" if os.name == "nt" else "clear")

def is_terminal_focused() -> bool:
    active_window = gw.getActiveWindow()
    if active_window:
        return "h3 hota map editor x" in active_window.title.lower()
    return False

def detect_key_press(valid_keys: str) -> str:
    global previous_key
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if is_terminal_focused():
                    if(event.name == previous_key):
                        continue
                    if event.name in valid_keys:
                        previous_key = event.name
                        return event.name
                    elif event.name == "esc":
                        previous_key = "esc"
                        return "esc"
            elif event.event_type == keyboard.KEY_UP:
                previous_key = ""
        else:
            previous_key = ""
        time.sleep(SLEEP.TIC)

def prompt_input(prompt: str) -> str:
    global previous_key
    input_chars = []
    print(prompt, end = "", flush = True)
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if is_terminal_focused():
                    if(event.name == previous_key):
                        continue
                    if event.name == "enter" and len(input_chars) > 0:
                        xprint()
                        xprint()
                        break
                    elif event.name == "backspace":
                        if input_chars:
                            input_chars.pop()
                            print("\b \b", end = "", flush = True)
                    elif event.name == "esc":
                        previous_key = "esc"
                        return ""
                    elif not keyboard.is_modifier(event.name) and len(event.name) == 1:
                        input_chars.append(event.name)
                        print(event.name, end = "", flush = True)
            elif event.event_type == keyboard.KEY_UP:
                previous_key = ""
        time.sleep(SLEEP.TIC)
    return "".join(input_chars)
