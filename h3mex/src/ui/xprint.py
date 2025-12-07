import msvcrt
import re
import time

from src.common import Cursor, Keypress, TextAlign, TextColor, TextType, Wait
from src.ui import header, ui


def xprint(
    type: int = TextType.NORMAL,
    text: str = "",
    align: int = TextAlign.LEFT,
    overwrite: int = 0,
    skip_line: bool = False,
    menu_num: str = "",
    menu_width: int = 0,
    menu: tuple[str, list] = None,
) -> None | str:
    if menu:
        return _menu_prompt(menu[0], menu[1])

    if not ui.redrawing and type != TextType.HEADER:
        ui.cache.append((type, text, align, overwrite, skip_line, menu_num, menu_width, menu))

    if overwrite > 0:
        _overwrite(overwrite)

    match type:
        case TextType.NORMAL:
            print(_align_text(align=align, text=f"{TextColor.WHITE}{text}{TextColor.RESET}"))

        case TextType.INFO:
            print(_align_text(text=f"{TextColor.CYAN}{text}{TextColor.RESET}"))

        case TextType.MENU:
            spacing = 3 - len(menu_num)
            menu_num_formatted = f"{' ' * spacing}[{TextColor.YELLOW}{menu_num}{TextColor.RESET}]"
            text_formatted = f"{TextColor.WHITE}{text}{TextColor.RESET}"
            print(
                _align_text(align=TextAlign.MENU, text=f"{menu_num_formatted} {text_formatted}", menu_width=menu_width)
            )

        case TextType.PROMPT:
            xprint()
            input = _string_prompt(_align_text(text=f"{TextColor.YELLOW}[{text}] > {TextColor.WHITE}"))
            return input

        case TextType.ACTION:
            print(
                _align_text(text=f"{TextColor.WHITE}{text}{TextColor.RESET}"),
                end=" ",
                flush=True,
            )
            time.sleep(Wait.NORMAL.value)

        case TextType.DONE:
            print(f"{TextColor.GREEN}{"DONE"}{TextColor.RESET}")
            time.sleep(Wait.NORMAL.value)

        case TextType.HEADER:
            print(_align_text(align=TextAlign.CENTER, text=text))

        case TextType.ERROR:
            match align:
                case TextAlign.LEFT:
                    if skip_line:
                        xprint()
                    print(_align_text(text=f"{TextColor.RED}Error: {text}{TextColor.RESET}"))
                case TextAlign.FLUSH:
                    print(f"{TextColor.RED}Error: {text}{TextColor.RESET}")
            time.sleep(Wait.LONG.value)

        case TextType.INDENT:
            print(
                _align_text(text=text),
                end="",
                flush=True,
            )

    return None


def _overwrite(overwrite: int) -> None:
    time.sleep(Wait.SHORT.value)
    for _ in range(overwrite):
        print(Cursor.RESET_PREVIOUS, end="")


def _align_text(align=TextAlign.LEFT, text="", menu_width=0) -> str:
    cleaned_text = _clean(str(text))
    text_length = len(cleaned_text)
    if align == TextAlign.LEFT:
        padding = (ui.terminal_width - ui.MAX_PRINT_WIDTH) // 2
        return " " * padding + str(text)
    elif align == TextAlign.CENTER:
        padding = (ui.terminal_width - text_length) // 2
        return " " * padding + str(text)
    elif align == TextAlign.MENU:
        padding = (ui.terminal_width - menu_width) // 2
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
    width += 8
    valid_keys = [] if name == "MAIN MENU" else [Keypress.ESC]
    xprint(text=f"{name}", align=TextAlign.CENTER)
    xprint()
    for item in items:
        if item:
            valid_keys.append(item[0]) if item[0] != "ESC" else valid_keys.append(Keypress.ESC)
            xprint(type=TextType.MENU, text=item[1], menu_num=item[0], menu_width=width)
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
                return ""
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
