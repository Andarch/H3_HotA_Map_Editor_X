import keyboard
import time
import shutil
from enum import Enum

SLEEP_TIME = 0.75

class COLOR:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    RESET  = "\033[0m"

class CPTYPE(Enum):
    NORMAL = 1
    INFO = 2
    INPUT  = 3
    ACTION = 4
    SPECIAL  = 5
    ERROR = 6

def print_cyan(text: str) -> None:
    print(f"{COLOR.CYAN}{text}{COLOR.RESET}")

def print_menu_option(number: str, text: str) -> None:
    print(f"   {COLOR.YELLOW}{number}{COLOR.WHITE} – {text}{COLOR.RESET}")

def print_string_prompt(prompt: str) -> str:
    user_input = input(f"{COLOR.YELLOW}[{prompt}] > {COLOR.RESET}")
    print()
    return user_input

def print_action(text: str) -> None:
    print(f"{COLOR.WHITE}{text}{COLOR.RESET}", end=" ", flush=True)
    time.sleep(SLEEP_TIME)

def print_done() -> None:
    print(f"{COLOR.GREEN}DONE{COLOR.RESET}")
    time.sleep(SLEEP_TIME)
    print()

def print_error(error: str) -> None:
    print(f"{COLOR.RED}{error}{COLOR.RESET}")
    time.sleep(SLEEP_TIME)
    print()

def key_prompt(valid_keys: str) -> str:
    while True:
        for key in valid_keys:
            if keyboard.is_pressed(key):
                return key
        time.sleep(0.01)

def cprint(text = ""):
    print(center_text(text))

def center_text(text):
    # Get the terminal size
    terminal_width = shutil.get_terminal_size().columns
    # Calculate the padding needed to center the text
    padding = (terminal_width - len(text)) // 2
    # Return the centered text
    return ' ' * padding + text