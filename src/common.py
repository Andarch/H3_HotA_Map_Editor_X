import keyboard
import time
import shutil
from enum import Enum

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

class CP(Enum):
    NORMAL = "NORMAL"
    INFO = "INFO"
    MENU  = "MENU"
    PROMPT = "PROMPT"
    ACTION = "ACTION"
    SPECIAL  = "SPECIAL"
    ERROR = "ERROR"

def cprint(type=CP.NORMAL, number=-1, text="", offset=0):
    if type != CP.MENU:
        ctext = center_text(text)
    else:
        ctext = menu_text(f"[{COLOR.YELLOW}{str(number)}{COLOR.WHITE}] {text}{COLOR.RESET}", offset)
    match type:
        case CP.NORMAL:
            print(ctext)
        case CP.INFO:
            print(f"{COLOR.CYAN}{ctext}{COLOR.RESET}")
        case CP.MENU:
            print(ctext)
        case CP.PROMPT:
            user_input = input(f"{COLOR.YELLOW}[{text}] > {COLOR.RESET}")
            print()
            return user_input
        case CP.ACTION:
            print(f"{COLOR.WHITE}{text}{COLOR.RESET}", end=" ", flush=True)
            time.sleep(SLEEP_TIME)
        case CP.SPECIAL:
            print(f"{COLOR.GREEN}{text}{COLOR.RESET}")
            time.sleep(SLEEP_TIME)
            print()
        case CP.ERROR:
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
    while True:
        for key in valid_keys:
            if keyboard.is_pressed(key):
                return key
        time.sleep(0.01)