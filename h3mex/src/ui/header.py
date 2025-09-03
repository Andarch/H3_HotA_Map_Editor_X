import os

from src.common import App, Color, MsgType, map_data
from src.ui import ui
from src.ui.xprint import xprint


def draw() -> None:
    if not ui.redrawing:
        ui.cache.clear()

    # Clear terminal
    os.system("cls" if os.name == "nt" else "clear")

    # Build header
    header_default = _create_header_line(color=(Color.FAINT + Color.GREY), symbol="#")
    header_appname = _create_header_line(color=(Color.FAINT + Color.GREY), symbol="#", text=App.NAME)
    header_version = _create_header_line(color=(Color.FAINT + Color.GREY), symbol="#", text=App.VERSION)

    # Build subheader
    subheader_filled = _create_header_line(color=(Color.FAINT + Color.WHITE), symbol="-")
    subtext1 = map_data["general"]["map_name"] if map_data else "No map"
    subtext1_color = Color.MAGENTA if map_data else Color.FAINT + Color.MAGENTA
    subheader_line1 = f"{subtext1_color}{subtext1}{Color.RESET}"
    subtext2 = map_data["filename"] if map_data else "loaded"
    subheader_line2 = f"{Color.FAINT + Color.MAGENTA}{subtext2}{Color.RESET}"

    # Print header
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_appname)
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_version)
    xprint(type=MsgType.HEADER, text=header_default)
    xprint(type=MsgType.HEADER, text=header_default)

    # Print subheader
    xprint(type=MsgType.HEADER, text="")
    xprint(type=MsgType.HEADER, text=subheader_filled)
    xprint(type=MsgType.HEADER, text=subheader_line1)
    xprint(type=MsgType.HEADER, text=subheader_line2)
    xprint(type=MsgType.HEADER, text=subheader_filled)
    xprint(type=MsgType.HEADER, text="")


def _create_header_line(color: str, symbol: str, text: str = "") -> str:
    width = ui.MAX_WIDTH if ui.width >= ui.MAX_WIDTH else ui.width
    if text == "":
        return color + (symbol * width) + Color.RESET
    else:
        fill_length = width - (len(text) + 2)
        line_left = color + (symbol * (fill_length // 2)) + Color.RESET
        if fill_length % 2 == 0:
            line_right = line_left
        else:
            line_right = color + (symbol * ((fill_length // 2) + 1)) + Color.RESET
        return f"{line_left} {Color.CYAN}{text}{Color.RESET} {line_right}"
