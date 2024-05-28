import time

SLEEP_TIME = 0.75

class COLOR:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    RESET  = "\033[0m"

def print_cyan(text: str) -> None:
    print(f"{COLOR.CYAN}{text}{COLOR.RESET}")

def print_prompt(prompt: str) -> str:
    user_input = input(f"{COLOR.YELLOW}[{prompt}] > {COLOR.RESET}")
    print()  # This will print a newline character
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