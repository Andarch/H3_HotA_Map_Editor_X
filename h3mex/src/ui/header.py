import os

from src.common import App, TextColor, TextType, map_data
from src.ui import ui
from src.ui.xprint import xprint


def draw() -> None:
    if not ui.redrawing:
        ui.cache.clear()

    # Clear terminal
    os.system("cls" if os.name == "nt" else "clear")

    # Build header
    header_default = _create_header_line(color=(TextColor.FAINT + TextColor.GREY), symbol="#")
    header_appname = _create_header_line(color=(TextColor.FAINT + TextColor.GREY), symbol="#", text=App.NAME)
    header_version = _create_header_line(color=(TextColor.FAINT + TextColor.GREY), symbol="#", text=App.VERSION)

    # Build subheader
    subheader_filled = _create_header_line(color=(TextColor.FAINT + TextColor.WHITE), symbol="-")
    subtext1 = map_data["general"]["map_name"] if map_data else "No map"
    subtext1_color = TextColor.MAGENTA if map_data else TextColor.FAINT + TextColor.MAGENTA
    subheader_line1 = f"{subtext1_color}{subtext1}{TextColor.RESET}"
    subtext2 = map_data["filename"] if map_data else "loaded"
    subheader_line2 = f"{TextColor.FAINT + TextColor.MAGENTA}{subtext2}{TextColor.RESET}"

    # Print header
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_appname)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_version)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_default)

    # Print subheader
    xprint(type=TextType.HEADER, text="")
    xprint(type=TextType.HEADER, text=subheader_filled)
    xprint(type=TextType.HEADER, text=subheader_line1)
    xprint(type=TextType.HEADER, text=subheader_line2)
    xprint(type=TextType.HEADER, text=subheader_filled)
    xprint(type=TextType.HEADER, text="")


def _create_header_line(color: str, symbol: str, text: str = "") -> str:
    width = ui.MAX_WIDTH if ui.width >= ui.MAX_WIDTH else ui.width
    if text == "":
        return color + (symbol * width) + TextColor.RESET
    else:
        fill_length = width - (len(text) + 2)
        line_left = color + (symbol * (fill_length // 2)) + TextColor.RESET
        if fill_length % 2 == 0:
            line_right = line_left
        else:
            line_right = color + (symbol * ((fill_length // 2) + 1)) + TextColor.RESET
        return f"{line_left} {TextColor.BOLD}{TextColor.CYAN}{text}{TextColor.RESET} {line_right}"
