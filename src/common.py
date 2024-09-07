from H3_HotA_MEX import map_data
import ctypes
from enum import Enum
import keyboard
import pygetwindow as gw
import os
import re
import shutil
import threading
import time
from typing import Tuple

class ALIGN(Enum):
    LEFT   = "LEFT"
    CENTER = "CENTER"
    MENU   = "MENU"
    FLUSH  = "FLUSH"

class CLR:
    RESET     = "\033[0m"
    FAINT     = "\033[2m"
    ITALIC    = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK     = "\033[5m"
    INVERTED  = "\033[7m"
    STRIKE    = "\033[9m"
    DEFAULT   = "\033[39m"
    RED       = "\033[91m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    BLUE      = "\033[94m"
    MAGENTA   = "\033[95m"
    CYAN      = "\033[96m"
    WHITE     = "\033[97m"
    GREY      = "\033[90m"

class MSG(Enum):
    NORMAL  = "NORMAL"
    INFO    = "INFO"
    MENU    = "MENU"
    PROMPT  = "PROMPT"
    ACTION  = "ACTION"
    SPECIAL = "SPECIAL"
    HEADER  = "HEADER"
    ERROR   = "ERROR"

class SLEEP:
    TIC    = 0.01
    SHORT  = 0.05
    NORMAL = 0.75
    LONG   = 1.5

TITLE = "H3 HotA Map Editor X"
VERSION = "v0.3.1"
TITLE_VERSION = f"{TITLE} {VERSION}"
PRINT_WIDTH = 75
PRINT_OFFSET = PRINT_WIDTH // 2
DONE = "DONE"

screen_content = []

terminal_width = 0
old_terminal_width = 0

redraw_scheduled = False
is_redrawing = False

old_key_press = ""

def initialize():
    global terminal_width, old_terminal_width
    terminal_width = old_terminal_width = get_terminal_width()
    hide_cursor(True)

    mutex_name = TITLE.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        draw_header()
        xprint(type = MSG.ERROR, text = "Another instance of the editor is already running.")
        return False

    monitor_thread = threading.Thread(target = monitor_terminal_size, daemon = True)
    monitor_thread.start()

    return True

def monitor_terminal_size() -> None:
    global terminal_width, old_terminal_width, redraw_scheduled
    while True:
        terminal_width = get_terminal_width()
        if terminal_width != old_terminal_width:
            old_terminal_width = terminal_width
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

def xprint(type = MSG.NORMAL, text = "", menu_num = -1, align = ALIGN.LEFT, menu_width = 0) -> None:
    global screen_content, is_redrawing
    if not is_redrawing and type != MSG.HEADER:
        screen_content.append((type, text, menu_num, align, menu_width))
    match type:
        case MSG.NORMAL:
            print(align_text(text = text))
        case MSG.INFO:
            print(align_text(text = f"{CLR.CYAN}{text}{CLR.RESET}"))
        case MSG.MENU:
            print(align_text(
                align = ALIGN.MENU,
                text = f"[{CLR.YELLOW}{str(menu_num)}{CLR.RESET}] {CLR.WHITE}{text}{CLR.RESET}",
                menu_width = menu_width
            ))
        case MSG.PROMPT:
            input = prompt_input(align_text(text = f"{CLR.YELLOW}[{text}] > {CLR.WHITE}"))
            return input
        case MSG.ACTION:
            print(align_text(text = f"{CLR.WHITE}{text}{CLR.RESET}"), end = " ", flush = True)
            time.sleep(SLEEP.NORMAL)
        case MSG.SPECIAL:
            print(f"{CLR.GREEN}{text}{CLR.RESET}")
            time.sleep(SLEEP.NORMAL)
        case MSG.HEADER:
            print(align_text(align = ALIGN.CENTER, text = text))
        case MSG.ERROR:
            match align:
                case ALIGN.LEFT:
                    xprint()
                    print(align_text(text = f"{CLR.RED}Error: {text}{CLR.RESET}"))
                case ALIGN.MENU:
                    xprint()
                    print(align_text(
                        align = ALIGN.MENU,
                        text = f"{CLR.RED}Error: {text}{CLR.RESET}",
                        menu_width = menu_width
                    ))
                case ALIGN.FLUSH:
                    print(f"{CLR.RED}Error: {text}{CLR.RESET}")
            time.sleep(SLEEP.LONG)

def align_text(align = ALIGN.LEFT, text = "", menu_width = 0) -> str:
    global terminal_width
    text = str(text)
    stripped_text = strip_ansi_codes(text)
    text_length = len(stripped_text)
    if align == ALIGN.LEFT:
        padding = terminal_width // 2 - PRINT_OFFSET
        return " " * padding + str(text)
    elif align == ALIGN.CENTER:
        padding = terminal_width // 2 - text_length // 2
        return " " * padding + str(text)
    elif align == ALIGN.MENU:
        padding = terminal_width // 2 - menu_width // 2 - 2
        return " " * padding + str(text)

def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)

def determine_menu_width(menu: list) -> int:
    width = 0
    for option in menu:
        option = str(option)
        stripped_option = strip_ansi_codes(option)
        option_length = len(stripped_option)
        if option_length > width:
            width = option_length
    return width

def draw_header(new_screen: bool = True) -> None:
    global screen_content, terminal_width
    if new_screen:
        screen_content = []
    clear_screen()

    # Set up header
    fill_symbol = "#"
    fill_color = CLR.GREY + CLR.FAINT
    title_color = CLR.CYAN
    header_colors = (fill_color, title_color)
    filler_row = create_filled_row(fill_symbol, header_colors)
    title_row = create_filled_row(fill_symbol, header_colors, TITLE)
    version_row = create_filled_row(fill_symbol, header_colors, VERSION)
    map1_data = map_data["Map 1"]
    map2_data = map_data["Map 2"]
    mapname_color1 = CLR.MAGENTA
    mapname_color2 = mapname_color1 + CLR.FAINT
    if map1_data:
        if map2_data:
            maps_loaded_row1 = f"Map 1: {map1_data["filename"]} | Map 2: {map2_data["filename"]}"
        else:
            maps_loaded_row1 = mapname_color1 + map1_data["general"]["name"] + CLR.RESET
            maps_loaded_row2 = mapname_color2 + map1_data["filename"] + CLR.RESET
    else:
        maps_loaded_row1 = mapname_color1 + "No map opened" + CLR.RESET
        maps_loaded_row2 = mapname_color2 + "Press 1 to open a map" + CLR.RESET

    # Print header
    xprint(type = MSG.HEADER, text = "")
    xprint(type = MSG.HEADER, text = "")
    xprint(type = MSG.HEADER, text = filler_row)
    xprint(type = MSG.HEADER, text = filler_row)
    xprint(type = MSG.HEADER, text = title_row)
    xprint(type = MSG.HEADER, text = filler_row)
    xprint(type = MSG.HEADER, text = version_row)
    xprint(type = MSG.HEADER, text = filler_row)
    xprint(type = MSG.HEADER, text = filler_row)
    xprint(type = MSG.HEADER, text = "")
    xprint(type = MSG.HEADER, text = "")
    xprint(type = MSG.HEADER, text = maps_loaded_row1)
    xprint(type = MSG.HEADER, text = maps_loaded_row2)
    xprint(type = MSG.HEADER, text = "")
    xprint(type = MSG.HEADER, text = "")

def redraw_screen() -> None:
    global redraw_scheduled, is_redrawing, screen_content
    redraw_scheduled = False
    is_redrawing = True
    draw_header(False)
    for type, text, menu_num, align, menu_width in screen_content:
        xprint(type, text, menu_num, align, menu_width)
    is_redrawing = False

def clear_screen() -> None:
    global screen_content
    os.system("cls" if os.name == "nt" else "clear")

def create_filled_row(symbol: str, colors = (CLR.DEFAULT, CLR.DEFAULT), text = "") -> str:
    global terminal_width
    if not text:
        if terminal_width >= PRINT_WIDTH:
            filler_row = f"{colors[0]}{symbol}" * PRINT_WIDTH + CLR.RESET
        else:
            filler_row = f"{colors[0]}{symbol}" * terminal_width + CLR.RESET
        return filler_row
    else:
        text_length = len(text)
        if terminal_width >= PRINT_WIDTH:
            fill_length = PRINT_WIDTH - (text_length + 2)
        else:
            fill_length = terminal_width - (text_length + 2)
        row_left = f"{colors[0]}{symbol}" * (fill_length // 2) + CLR.RESET
        row_right = f"{colors[0]}{symbol}" * (fill_length // 2) + CLR.RESET
        if fill_length % 2 != 0:
            row_right += f"{colors[0]}{symbol}" + CLR.RESET
        text_row = f"{row_left} {colors[1]}{text}{CLR.RESET} {row_right}"
        return text_row

def menu_prompt(menu: list) -> Tuple[str, int]:
    def main() -> str:
        draw_header()
        menu_width = determine_menu_width(menu)
        menu_num = 0
        valid_keys = ""
        for _, text in enumerate(menu):
            if text:
                menu_num += 1
                if(menu_num == 10):
                    menu_num = 0
                valid_keys += str(menu_num)
                xprint(
                    type = MSG.MENU,
                    menu_num = menu_num,
                    text = text,
                    menu_width = menu_width
                )
            else:
                xprint()
        input = detect_key_press(valid_keys)
        return input, menu_width
    def detect_key_press(valid_keys: str) -> str:
        global old_key_press
        while True:
            if is_terminal_focused():
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if is_terminal_focused():
                        if(event.name == old_key_press):
                            continue
                        if event.name in valid_keys:
                            old_key_press = event.name
                            return event.name
                        elif event.name == "esc":
                            old_key_press = "esc"
                            return "esc"
                elif event.event_type == keyboard.KEY_UP:
                    old_key_press = ""
            else:
                old_key_press = ""
            time.sleep(SLEEP.TIC)
    return main()

def is_terminal_focused() -> bool:
    active_window = gw.getActiveWindow()
    if active_window:
        return "H3 HotA Map Editor X" in active_window.title
    return False

def prompt_input(prompt: str) -> str:
    global old_key_press
    input_chars = []
    print(prompt, end = "", flush = True)
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if is_terminal_focused():
                    if(event.name == old_key_press):
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
                        old_key_press = "esc"
                        return ""
                    elif not keyboard.is_modifier(event.name) and len(event.name) == 1:
                        input_chars.append(event.name)
                        print(event.name, end = "", flush = True)
            elif event.event_type == keyboard.KEY_UP:
                old_key_press = ""
        time.sleep(SLEEP.TIC)
    return "".join(input_chars)
