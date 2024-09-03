from enum import Enum
import keyboard
import pygetwindow as gw  # For checking active window
import os
import shutil
import threading
import time

SLEEP_TIME = 0.75
PRINT_OFFSET = 27
DONE = "DONE"

screen_content = []
previous_width = shutil.get_terminal_size().columns
redraw_scheduled = False
is_redrawing = False

class ALIGN(Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"

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
    global screen_content
    os.system('cls' if os.name == 'nt' else 'clear')

def redraw_screen():
    global redraw_scheduled, is_redrawing, screen_content
    redraw_scheduled = False
    is_redrawing = True
    clear_screen()
    for type, number, text in screen_content:
        cprint(type, number, text)
    is_redrawing = False

def start_new_screen():
    global screen_content
    screen_content = []
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

def cprint(type=MSG.NORMAL, number=-1, text="") -> None:
    global screen_content, is_redrawing
    if not is_redrawing:
        screen_content.append((type, number, text))
    if type == MSG.PROMPT:
        ctext = align_text(text=f"{COLOR.YELLOW}[{text}] > {COLOR.RESET}")
    elif type == MSG.ACTION:
        ctext = align_text(text=f"{COLOR.WHITE}{text}{COLOR.RESET}")
    else:
        ctext = align_text(ALIGN.CENTER, text)
    match type:
        case MSG.NORMAL:
            print(ctext)
        case MSG.INFO:
            print(f"{COLOR.CYAN}{ctext}{COLOR.RESET}")
        case MSG.MENU:
            print(align_text(text=f"[{COLOR.YELLOW}{str(number)}{COLOR.WHITE}] {text}{COLOR.RESET}"))
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

def align_text(align=ALIGN.LEFT, text="") -> str:
    terminal_width = shutil.get_terminal_size().columns
    if align == ALIGN.LEFT:
        padding = terminal_width // 2 - PRINT_OFFSET
    else:
        padding = (terminal_width - len(text)) // 2
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
