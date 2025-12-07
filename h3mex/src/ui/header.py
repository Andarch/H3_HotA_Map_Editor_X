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

    os.system("cls" if os.name == "nt" else "clear")

    text_color = TextColor.GRAY
    mapfile_color = TextColor.FAINT + TextColor.CYAN if map_data else TextColor.FAINT + TextColor.RED
    mapfile = map_data["filename"] if map_data else "No map loaded"

    header_default = _create_header_line()
    header_appname = _create_header_line(text_color=text_color, text=f"{App.NAME} {App.VERSION}")
    header_mapfile = _create_header_line(text_color=mapfile_color, text=mapfile)

    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_appname)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text=header_mapfile)
    xprint(type=TextType.HEADER, text=header_default)
    xprint(type=TextType.HEADER, text="")


def _create_header_line(text_color: str = "", text: str = "") -> str:
    if text:
        fill_length = ui.width - (len(text) + 2)
        line_left = f"{Fill.Color}{Fill.Char * (fill_length // 2)}{TextColor.RESET}"
        if fill_length % 2 == 0:
            line_right = line_left
        else:
            line_right = f"{Fill.Color}{Fill.Char * ((fill_length // 2) + 1)}{TextColor.RESET}"
        return f"{line_left} {text_color}{text}{TextColor.RESET} {line_right}"
    else:
        return f"{Fill.Color}{Fill.Char * ui.width}{TextColor.RESET}"
