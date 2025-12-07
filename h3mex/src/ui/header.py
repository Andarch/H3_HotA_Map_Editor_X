import os
from enum import StrEnum

from src.common import App, TextColor, TextType, map_data
from src.ui import ui
from src.ui.xprint import xprint


class Fill(StrEnum):
    Char = "#"
    Color = f"{TextColor.FAINT}{TextColor.GRAY}"


def draw() -> None:
    if not ui.redrawing:
        ui.cache.clear()

    # Clear terminal
    os.system("cls" if os.name == "nt" else "clear")

    # Build header
    text_color = TextColor.GRAY
    mapfile_color = TextColor.BLUE if map_data else TextColor.FAINT + TextColor.BLUE
    mapfile = map_data["filename"] if map_data else "No map loaded"
    header_default = _create_header_line()
    header_appname = _create_header_line(text_color=text_color, text=App.NAME + App.VERSION)
    header_version = _create_header_line(text_color=text_color, text=App.VERSION)
    header_mapfile = _create_header_line(text_color=mapfile_color, text=mapfile)

    # Build subheader
    # filename_color = TextColor.BLUE if map_data else TextColor.FAINT + TextColor.BLUE
    # subtext = map_data["filename"] if map_data else "No map loaded"
    # subheader_border = _create_header_line(fill_color=TextColor.GRAY, FILL="-")
    # header_filename = _create_header_line(fill_color=fill_color, FILL="#", text_color=filename_color, text=subtext)

    # Print header
    # xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_appname)
    xprint(type=TextType.HEADER, text=header_version)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_mapfile)
    xprint(type=TextType.HEADER, text=header_default)

    # Print subheader
    # xprint(type=TextType.HEADER, text="")
    # xprint(type=TextType.HEADER, text=subheader_border)
    # xprint(type=TextType.HEADER, text=header_default)
    # xprint(type=TextType.HEADER, text=header_filename)
    # xprint(type=TextType.HEADER, text=header_default)
    # xprint(type=TextType.HEADER, text=subheader_border)
    # xprint(type=TextType.HEADER, text="")


def _create_header_line(text_color: str = "", text: str = "") -> str:
    # ui_width = ui.MAX_WIDTH if ui.width >= ui.MAX_WIDTH else ui.width
    fill_length = ui.width - (len(text) + 2)
    if text:
        line_left = f"{Fill.Color}{Fill.Char * (fill_length // 2)}{TextColor.RESET}"
        if fill_length % 2 == 0:
            line_right = line_left
        else:
            line_right = f"{Fill.Color}{Fill.Char * ((fill_length // 2) + 1)}{TextColor.RESET}"
        return f"{line_left} {text_color}{text}{TextColor.RESET} {line_right}"
    else:
        return f"{Fill.Color}{Fill.Char * fill_length}{TextColor.RESET}"
    # elif text and not fill:
    #     return f"{text_color}{text}{TextColor.RESET}"
    # else:
    #     raise Exception("Need at least one of 'fill' or 'text' to create header line.")
