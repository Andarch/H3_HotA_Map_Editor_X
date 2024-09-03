from enum import Enum
import keyboard
import pygetwindow as gw  # For checking active window
import os
import shutil
import threading
import time

SLEEP_TIME = 0.75
SELECT = "Select an option:"
DONE = "DONE"

screen_content = []
previous_width = shutil.get_terminal_size().columns
redraw_scheduled = False
is_redrawing = False

class COLOR:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    RESET  = "\033[0m"

class MSG(Enum):
    NORMAL = "NORMAL"
    INFO = "INFO"
    MENU  = "MENU"
    PROMPT = "PROMPT"
    ACTION = "ACTION"
    SPECIAL  = "SPECIAL"
    ERROR = "ERROR"

def hide_cursor(hide: bool) -> None:
    if hide:
        print("\033[?25l", end="", flush=True)
    else:
        print("\033[?25h", end="", flush=True)

def is_terminal_focused() -> bool:
    active_window = gw.getActiveWindow()
    if active_window:
        return 'h3 hota map editor x' in active_window.title.lower()
    return False

def get_terminal_width():
    return shutil.get_terminal_size().columns

def monitor_terminal_size():
    global previous_width, redraw_scheduled
    while True:
        current_width = get_terminal_width()
        if current_width != previous_width:
            previous_width = current_width
            if not redraw_scheduled:
                redraw_scheduled = True
                threading.Timer(0, redraw_screen).start()
        time.sleep(0.05)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def redraw_screen():
    global redraw_scheduled, is_redrawing
    redraw_scheduled = False
    is_redrawing = True
    clear_screen()
    for type, number, text, offset in screen_content:
        cprint(type, number, text, offset)
    is_redrawing = False

def redraw_header():
    clear_screen()
    cprint()
    cprint()
    cprint(text="#####################################################")
    cprint(text="##                                                 ##")
    cprint(text="##           H3 HotA Map Editor X v0.3.1           ##")
    cprint(text="##                                                 ##")
    cprint(text="#####################################################")
    cprint()
    cprint()

def cprint(type=MSG.NORMAL, number=-1, text="", offset=0):
    global screen_content, is_redrawing
    if not is_redrawing:
        screen_content.append((type, number, text, offset))
    if type == MSG.PROMPT:
        ctext = left_text(f"{COLOR.YELLOW}[{text}] > {COLOR.RESET}", offset)
    elif type == MSG.ACTION:
        ctext = left_text(f"{COLOR.WHITE}{text}{COLOR.RESET}", offset)
    else:
        ctext = center_text(text)
    match type:
        case MSG.NORMAL:
            print(ctext)
        case MSG.INFO:
            print(f"{COLOR.CYAN}{ctext}{COLOR.RESET}")
        case MSG.MENU:
            print(left_text(f"[{COLOR.YELLOW}{str(number)}{COLOR.WHITE}] {text}{COLOR.RESET}",
            offset))
        case MSG.PROMPT:
            user_input = robust_input(ctext)
            return user_input
        case MSG.ACTION:
            print(ctext)
            time.sleep(SLEEP_TIME)
        case MSG.SPECIAL:
            print(f"{COLOR.GREEN}{text}{COLOR.RESET}")
            time.sleep(SLEEP_TIME)
            print()
        case MSG.ERROR:
            print(f"\n{COLOR.RED}Error: {text}{COLOR.RESET}")
            time.sleep(SLEEP_TIME)

def center_text(text: str) -> str:
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    return ' ' * padding + text

def left_text(text: str, offset: int) -> str:
    terminal_width = shutil.get_terminal_size().columns
    padding = terminal_width // 2 - offset
    return ' ' * padding + text

# def align_text(text: str, align: str) -> str:

def key_press(valid_keys: str) -> str:
    time.sleep(0.1)
    while True:
        if is_terminal_focused():
            for key in valid_keys:
                if keyboard.is_pressed(key):
                    while keyboard.is_pressed(key):
                        time.sleep(0.01)
                    return key
        time.sleep(0.01)

def robust_input(prompt):
    print(prompt, end="", flush=True)
    input_chars = []
    time.sleep(0.1)
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if is_terminal_focused():
                    if event.name == 'enter':
                        break
                    elif event.name == 'backspace':
                        if input_chars:
                            input_chars.pop()
                            print('\b \b', end='', flush=True)
                    elif not keyboard.is_modifier(event.name) and len(event.name) == 1:
                        input_chars.append(event.name)
                        print(event.name, end='', flush=True)
        time.sleep(0.01)
    return ''.join(input_chars)
