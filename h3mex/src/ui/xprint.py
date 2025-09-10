import msvcrt
import re
import time

from src.common import (
    Align,
    Color,
    Cursor,
    Keypress,
    MsgType,
    Wait,
    map_data,
)
from src.ui import header, ui
from src.ui.menus import Menu
from src.utilities import exit


def xprint(
    type: int = MsgType.NORMAL,
    text: str = "",
    align: int = Align.LEFT,
    overwrite: int = 0,
    skip_line: bool = False,
    menu_num: int = -1,
    menu_width: int = 0,
    menu: tuple[str, list] = None,
) -> None | str:
    if menu:
        return _menu_prompt(menu[0], menu[1])
    if not ui.redrawing and type != MsgType.HEADER:
        ui.cache.append((type, text, align, overwrite, skip_line, menu_num, menu_width, menu))
    if overwrite > 0:
        _overwrite(overwrite)
    match type:
        case MsgType.NORMAL:
            print(_align_text(align=align, text=f"{Color.WHITE}{text}{Color.RESET}"))
        case MsgType.INFO:
            print(_align_text(text=f"{Color.CYAN}{text}{Color.RESET}"))
        case MsgType.MENU:
            menu_num_formatted = f"[{Color.YELLOW}{str(menu_num)}{Color.RESET}]"
            text_formatted = f"{Color.WHITE}{text}{Color.RESET}"
            print(_align_text(align=Align.MENU, text=f"{menu_num_formatted} {text_formatted}", menu_width=menu_width))
        case MsgType.PROMPT:
            xprint()
            input = _string_prompt(_align_text(text=f"{Color.YELLOW}[{text}] > {Color.WHITE}"))
            return input
        case MsgType.ACTION:
            print(
                _align_text(text=f"{Color.WHITE}{text}{Color.RESET}"),
                end=" ",
                flush=True,
            )
            time.sleep(Wait.NORMAL.value)
        case MsgType.DONE:
            print(f"{Color.GREEN}{"DONE"}{Color.RESET}")
            time.sleep(Wait.NORMAL.value)
        case MsgType.HEADER:
            print(_align_text(align=Align.CENTER, text=text))
        case MsgType.ERROR:
            match align:
                case Align.LEFT:
                    if skip_line:
                        xprint()
                    print(_align_text(text=f"{Color.RED}Error: {text}{Color.RESET}"))
                case Align.FLUSH:
                    print(f"{Color.RED}Error: {text}{Color.RESET}")
            time.sleep(Wait.LONG.value)
    return None


def _overwrite(overwrite: int) -> None:
    time.sleep(Wait.SHORT.value)
    for _ in range(overwrite):
        print(Cursor.RESET_PREVIOUS, end="")


def _align_text(align=Align.LEFT, text="", menu_width=0) -> str:
    cleaned_text = _clean(str(text))
    text_length = len(cleaned_text)
    if align == Align.LEFT:
        padding = (ui.width // 2) - (ui.MAX_WIDTH // 2)
        return " " * padding + str(text)
    elif align == Align.CENTER:
        padding = ui.width // 2 - text_length // 2
        return " " * padding + str(text)
    elif align == Align.MENU:
        padding = ui.width // 2 - menu_width // 2
        return " " * padding + str(text)


def _menu_prompt(name: str, items: list) -> str:
    header.draw()
    width = 0
    for item in items:
        if item is None:
            continue
        text = _clean(item[1])
        w = len(text)
        if w > width:
            width = w
    valid_keys = [] if items == Menu.MAIN["menus"][0] else [Keypress.ESC]
    xprint(text=f"{name}", align=Align.CENTER)
    xprint()
    for item in items:
        if item:
            valid_keys.append(item[0])
            xprint(type=MsgType.MENU, text=item[1], menu_num=item[0], menu_width=width)
        else:
            xprint()
    xprint()
    while True:
        keypress = msvcrt.getwch()
        if keypress.upper() in valid_keys:
            return keypress.upper()


def _string_prompt(prompt: str) -> str:
    print(prompt, end="", flush=True)
    print(Cursor.SHOW, end="", flush=True)
    chars = []
    while True:
        keypress = msvcrt.getwch()
        match keypress:
            case Keypress.ENTER:
                if chars:
                    print(Cursor.HIDE, end="", flush=True)
                    xprint()
                    xprint()
                    return "".join(chars)
                continue
            case Keypress.BACKSPACE:
                if chars:
                    chars.pop()
                    print("\b \b", end="", flush=True)
                continue
            case Keypress.ESC:
                print(Cursor.HIDE, end="", flush=True)
                if map_data:
                    return ""
                else:
                    print("\r\x1b[K", end="", flush=True)
                    exit()
            case _:
                chars.append(keypress)
                print(keypress, end="", flush=True)


def _clean(text: str) -> str:
    # Remove ANSI escape codes
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    text = ansi_escape.sub("", text)
    # Remove control characters except space (preserve visible spaces)
    invisible = re.compile(r"[\x00-\x1F\x7F]")
    return invisible.sub("", text)
