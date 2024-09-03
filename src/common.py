from enum import Enum
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
previous_width = shutil.get_terminal_size().columns
redraw_scheduled = False
is_redrawing = False
previous_key = ""

def hide_cursor(hide: bool) -> None:
    if hide:
        print("\033[?25l", end = "", flush = True)
    else:
        print("\033[?25h", end = "", flush = True)

def is_terminal_focused() -> bool:
    active_window = gw.getActiveWindow()
    if active_window:
        return "h3 hota map editor x" in active_window.title.lower()
    return False

def get_terminal_width() -> int:
    return shutil.get_terminal_size().columns

def clear_screen() -> None:
    global screen_content
    os.system("cls" if os.name == "nt" else "clear")

def align_text(align = ALIGN.LEFT, text = "") -> str:
    terminal_width = shutil.get_terminal_size().columns
    if align == ALIGN.LEFT:
        padding = terminal_width // 2 - PRINT_OFFSET
    else:
        padding = (terminal_width - len(text)) // 2
    return " " * padding + str(text)

def cprint(type = MSG.NORMAL, text = "", menu_item = -1, flush = False) -> None:
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
                print()
                print(align_text(text = f"{CLR.RED}Error: {text}{CLR.RESET}"))
            else:
                print(f"{CLR.RED}Error: {text}{CLR.RESET}")
            time.sleep(SLEEP.LONG)

def redraw_screen() -> None:
    global redraw_scheduled, is_redrawing, screen_content
    redraw_scheduled = False
    is_redrawing = True
    clear_screen()
    for type, text, menu_item, flush in screen_content:
        cprint(type, text, menu_item, flush)
    is_redrawing = False

def start_new_screen() -> None:
    global screen_content
    screen_content = []
    clear_screen()
    # Set up title
    rowA_fill = f"{CLR.GREY}#" * PRINT_WIDTH + CLR.RESET
    rowB_fill = f"{CLR.GREY}#" * ((PRINT_WIDTH - (len(TITLE) + 2)) // 2) + CLR.RESET
    rowB_title = f"{rowB_fill} {CLR.CYAN}{TITLE}{CLR.RESET} {rowB_fill}"
    # Print title
    cprint()
    cprint()
    cprint(text = rowA_fill)
    cprint(text = rowA_fill)
    cprint(text = rowB_title)
    cprint(text = rowA_fill)
    cprint(text = rowA_fill)
    cprint()
    cprint()

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

def key_press(valid_keys: str) -> str:
    global previous_key
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
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
        time.sleep(SLEEP.TIC)

def prompt_input(prompt: str) -> str:
    global previous_key
    print(prompt, end = "", flush = True)
    input_chars = []
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if(event.name == previous_key):
                    continue
                if is_terminal_focused():
                    if event.name == "enter" and len(input_chars) > 0:
                        cprint()
                        cprint()
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
