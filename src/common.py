# region Imports

import ctypes
from enum import Enum
import keyboard
import pygetwindow as gw
import os
import re
import shutil
import sys
import threading
import time
from typing import Union

# endregion

# region Constants

TITLE = "H3 HotA Map Editor X"
VERSION = "v0.3.1"
TITLE_VERSION = f"{TITLE} {VERSION}"
PRINT_WIDTH = 75
PRINT_OFFSET = PRINT_WIDTH // 2
DONE = "DONE"
MAP1 = "Map 1"
MAP2 = "Map 2"

class Align(Enum):
    LEFT   = 1
    CENTER = 2
    MENU   = 3
    FLUSH  = 4

class Color(Enum):
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

class Sleep(Enum):
    TIC    = 0.01
    SHORT  = 0.05
    NORMAL = 0.75
    LONG   = 1.5

class Text(Enum):
    NORMAL  = 1
    INFO    = 2
    MENU    = 3
    PROMPT  = 4
    ACTION  = 5
    SPECIAL = 6
    HEADER  = 7
    ERROR   = 8

class Menu(Enum):
    START = {
        1: "Open",
       -1: "",
        0: "Exit"
    }
    OPEN  = {
        1: "Open 1 map",
        2: "Open 2 maps"
    }
    SAVE_A = {
        1: "Save 1 map",
        2: "Save 2 maps"
    }
    SAVE_B = {
        1: "Save",
        2: "Save as"
    }
    MAIN  = {
        1: "Open",
        2: "Save",
        3: "Display map data",
        4: "Count objects",
        5: "Export .json file",
        6: "Swap layers",
        7: "Modify towns (buildings/spells)",
        8: "Generate minimap",
        9: "Update events (global/town)",
        0: "Exit"
    }

# endregion

# region Global Variables

map_data = {MAP1:{}, MAP2:{}}
screen_content = []
terminal_width = 0
old_terminal_width = 0
redraw_scheduled = False
is_redrawing = False
old_keypress = ""

# endregion

def initialize():
    global terminal_width, old_terminal_width
    terminal_width = old_terminal_width = get_terminal_width()
    hide_cursor(True)

    mutex_name = TITLE.replace(" ", "_")
    ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        draw_header()
        xprint(type=Text.ERROR, text="Another instance of the editor is already running.")
        return False

    monitor_thread1 = threading.Thread(target = monitor_old_keypress, daemon = True)
    monitor_thread1.start()

    monitor_thread2 = threading.Thread(target = monitor_terminal_size, daemon = True)
    monitor_thread2.start()

    return True

def hide_cursor(hide: bool) -> None:
    if hide:
        print("\033[?25l", end = "", flush = True)
    else:
        print("\033[?25h", end = "", flush = True)

def monitor_old_keypress() -> None:
    global old_keypress
    while True:
        if is_terminal_focused():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_UP:
                old_keypress = ""
        else:
            old_keypress = ""
        time.sleep(Sleep.TIC.value)

def monitor_terminal_size() -> None:
    global terminal_width, old_terminal_width, redraw_scheduled
    while True:
        terminal_width = get_terminal_width()
        if terminal_width != old_terminal_width:
            old_terminal_width = terminal_width
            if not redraw_scheduled:
                redraw_scheduled = True
                threading.Timer(0, redraw_screen).start()
        time.sleep(Sleep.SHORT.value)

def get_terminal_width() -> int:
    return shutil.get_terminal_size().columns

def is_terminal_focused() -> bool:
    active_window = gw.getActiveWindow()
    if active_window:
        return TITLE in active_window.title
    return False

def draw_header(new_screen: bool = True) -> None:
    global screen_content, terminal_width
    if new_screen:
        screen_content = []
    clear_screen()

    # Set up header
    fill1_symbol = "#"
    fill1_color = Color.GREY.value + Color.FAINT.value
    title_color = Color.CYAN.value
    headerA_colors = (fill1_color, title_color)
    fill1_row = create_filled_row(fill1_symbol, headerA_colors)
    title_row = create_filled_row(fill1_symbol, headerA_colors, TITLE)
    version_row = create_filled_row(fill1_symbol, headerA_colors, VERSION)

    map1_data = map_data["Map 1"]
    map2_data = map_data["Map 2"]
    headerB_color1 = Color.MAGENTA.value
    headerB_color2 = Color.GREY.value
    fill2_symbol = "-"
    fill2_color = headerB_color2
    headerB_colors = (fill2_color, fill2_color)
    fill2_row = create_filled_row(fill2_symbol, headerB_colors)
    if map1_data:
        if map2_data:
            map1_row1 = f"Map 1: {map1_data["filename"]} | Map 2: {map2_data["filename"]}"
        else:
            map1_row1 = f"{headerB_color1}{map1_data['general']['name']}{Color.RESET.value}"
            map1_row2 = f"{Color.FAINT.value}{headerB_color1}{{{map1_data['filename']}}}{Color.RESET.value}"
    else:
        map1_row1 = f"{headerB_color1}Press a{Color.RESET.value}"
        map1_row2 = f"{headerB_color1}key{Color.RESET.value}"

    # Print header
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=title_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=version_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text=fill1_row)
    xprint(type=Text.HEADER, text="")
    xprint(type=Text.HEADER, text=fill2_row)
    xprint(type=Text.HEADER, text=map1_row1)
    xprint(type=Text.HEADER, text=map1_row2)
    xprint(type=Text.HEADER, text=fill2_row)
    xprint(type=Text.HEADER, text="")

def redraw_screen() -> None:
    global redraw_scheduled, is_redrawing, screen_content
    redraw_scheduled = False
    is_redrawing = True
    draw_header(False)
    for type, text, align, menu_num, menu_width in screen_content:
        xprint(type, text, align, menu_num, menu_width)
    is_redrawing = False

def clear_screen() -> None:
    global screen_content
    os.system("cls" if os.name == "nt" else "clear")

def create_filled_row(symbol: str, colors=(Color.DEFAULT.value, Color.DEFAULT.value), text="") -> str:
    global terminal_width
    if not text:
        if terminal_width >= PRINT_WIDTH:
            filler_row = f"{colors[0]}{symbol}" * PRINT_WIDTH + Color.RESET.value
        else:
            filler_row = f"{colors[0]}{symbol}" * terminal_width + Color.RESET.value
        return filler_row
    else:
        text_length = len(text)
        if terminal_width >= PRINT_WIDTH:
            fill_length = PRINT_WIDTH - (text_length + 2)
        else:
            fill_length = terminal_width - (text_length + 2)
        row_left = f"{colors[0]}{symbol}" * (fill_length // 2) + Color.RESET.value
        row_right = f"{colors[0]}{symbol}" * (fill_length // 2) + Color.RESET.value
        if fill_length % 2 != 0:
            row_right += f"{colors[0]}{symbol}" + Color.RESET.value
        text_row = f"{row_left} {colors[1]}{text}{Color.RESET.value} {row_right}"
        return text_row

def xprint(type=Text.NORMAL, text="", align=Align.LEFT, menu_num=-1, menu_width=0, menu={}) -> Union[None, Union[int, str]]:
    def main() -> Union[None, Union[int, str]]:
        global screen_content, is_redrawing
        if menu: return menu_prompt(menu)
        if not is_redrawing and type != Text.HEADER:
            screen_content.append((type, text, align, menu_num, menu_width))
        match type:
            case Text.NORMAL:
                print(align_text(text=text))
            case Text.INFO:
                print(align_text(text=f"{Color.CYAN.value}{text}{Color.RESET.value}"))
            case Text.MENU:
                print(align_text(
                    align=Align.MENU,
                    text=f"[{Color.YELLOW.value}{str(menu_num)}{Color.RESET.value}] {Color.WHITE.value}{text}{Color.RESET.value}",
                    menu_width=menu_width
                ))
            case Text.PROMPT:
                xprint()
                input = string_prompt(align_text(text=f"{Color.YELLOW.value}[{text}] > {Color.WHITE.value}"))
                return input
            case Text.ACTION:
                print(align_text(text=f"{Color.WHITE.value}{text}{Color.RESET.value}"), end = " ", flush = True)
                time.sleep(Sleep.NORMAL.value)
            case Text.SPECIAL:
                print(f"{Color.GREEN.value}{text}{Color.RESET.value}")
                time.sleep(Sleep.NORMAL.value)
            case Text.HEADER:
                print(align_text(align=Align.CENTER, text=text))
            case Text.ERROR:
                match align:
                    case Align.LEFT:
                        xprint()
                        print(align_text(text=f"{Color.RED.value}Error: {text}{Color.RESET.value}"))
                    case Align.FLUSH:
                        print(f"{Color.RED.value}Error: {text}{Color.RESET.value}")
                time.sleep(Sleep.LONG.value)
        return None

    def align_text(align=Align.LEFT, text="", menu_width=0) -> str:
        global terminal_width
        stripped_text = strip_ansi_codes(str(text))
        text_length = len(stripped_text)
        if align == Align.LEFT:
            padding = terminal_width // 2 - PRINT_OFFSET
            return " " * padding + str(text)
        elif align == Align.CENTER:
            padding = terminal_width // 2 - text_length // 2
            return " " * padding + str(text)
        elif align == Align.MENU:
            padding = terminal_width // 2 - menu_width // 2 - 2
            return " " * padding + str(text)

    def strip_ansi_codes(text: str) -> str:
        ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", text)

    def menu_prompt(menu: dict) -> str:
        def main() -> str:
            draw_header()
            menu_width = get_menu_width(menu)
            # menu_num = 0
            valid_keys = ""
            for key, text in menu.items():
                if text:
                    # menu_num += 1
                    # if(menu_num == 10):
                    #     menu_num = 0
                    valid_keys += str(key)
                    xprint(
                        type=Text.MENU,
                        text=text,
                        menu_num=key,
                        menu_width=menu_width
                    )
                else:
                    xprint()

            input = detect_key_press(valid_keys)
            if input != "esc": input = int(input)
            return input

        def get_menu_width(menu: dict) -> int:
            width = 0
            for _, text in menu.items():
                stripped_text = strip_ansi_codes(text)
                text_length = len(stripped_text)
                if text_length > width:
                    width = text_length
            return width

        def detect_key_press(valid_keys: str) -> str:
            global old_keypress
            while True:
                if is_terminal_focused():
                    event = keyboard.read_event()
                    if event.event_type == keyboard.KEY_DOWN:
                        if is_terminal_focused():
                            if(event.name == old_keypress):
                                continue
                            if event.name in valid_keys:
                                old_keypress = event.name
                                return event.name
                            elif event.name == "esc":
                                old_keypress = "esc"
                                return "esc"
                    elif event.event_type == keyboard.KEY_UP:
                        old_keypress = ""
                else:
                    old_keypress = ""
                time.sleep(Sleep.TIC.value)
        return main()

    def string_prompt(prompt: str) -> str:
        global old_keypress
        input_chars = []
        print(prompt, end = "", flush = True)
        while True:
            if is_terminal_focused():
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if is_terminal_focused():
                        if(event.name == old_keypress):
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
                            old_keypress = "esc"
                            return ""
                        elif not keyboard.is_modifier(event.name) and len(event.name) == 1:
                            input_chars.append(event.name)
                            print(event.name, end = "", flush = True)
                elif event.event_type == keyboard.KEY_UP:
                    old_keypress = ""
            time.sleep(Sleep.TIC.value)
        return "".join(input_chars)
    return main()

def exit() -> None:
    xprint()
    xprint(text="Exiting...")
    time.sleep(Sleep.NORMAL.value)
    xprint(text=Color.RESET.value)
    sys.exit(0)