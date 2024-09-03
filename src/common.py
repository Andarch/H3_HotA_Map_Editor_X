from enum import Enum
import keyboard
import pygetwindow as gw  # For checking active window
import os
import shutil
import time

SLEEP_TIME = 0.75
SELECT = "Select an option:"
DONE = "DONE"

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

def is_terminal_focused() -> bool:
    active_window = gw.getActiveWindow()
    if active_window:
        return 'h3 hota map editor x' in active_window.title.lower()
    return False

def show_cursor(show: bool) -> None:
    if show:
        print("\033[?25h", end="", flush=True)
    else:
        print("\033[?25l", end="", flush=True)

def print_header():
    os.system('cls')
    cprint()
    cprint()
    cprint(text="###################################")
    cprint(text="##                               ##")
    cprint(text="##  H3 HotA Map Editor X v0.3.1  ##")
    cprint(text="##                               ##")
    cprint(text="###################################")
    cprint()
    cprint()

def cprint(type=MSG.NORMAL, number=-1, text="", offset=0):
    if type == MSG.MENU:
        ctext = menu_text(
            f"[{COLOR.YELLOW}{str(number)}{COLOR.WHITE}] {text}{COLOR.RESET}",
            offset
        )
    elif type == MSG.PROMPT:
        ctext = center_text(f"{COLOR.YELLOW}[{text}] > {COLOR.RESET}")
    else:
        ctext = center_text(text)
    match type:
        case MSG.NORMAL:
            print(ctext)
        case MSG.INFO:
            print(f"{COLOR.CYAN}{ctext}{COLOR.RESET}")
        case MSG.MENU:
            print(ctext)
        case MSG.PROMPT:
            user_input = robust_input(ctext)
            print()
            return user_input
        case MSG.ACTION:
            print(f"{COLOR.WHITE}{text}{COLOR.RESET}", end=" ", flush=True)
            time.sleep(SLEEP_TIME)
        case MSG.SPECIAL:
            print(f"{COLOR.GREEN}{text}{COLOR.RESET}")
            time.sleep(SLEEP_TIME)
            print()
        case MSG.ERROR:
            print(f"\n{COLOR.RED}Error: {text}{COLOR.RESET}")
            time.sleep(SLEEP_TIME)
            print()

def center_text(text: str) -> str:
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    return ' ' * padding + text

def menu_text(text: str, offset: int) -> str:
    terminal_width = shutil.get_terminal_size().columns
    padding = terminal_width // 2 - offset
    return ' ' * padding + text

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
    print(prompt, end='', flush=True)
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
