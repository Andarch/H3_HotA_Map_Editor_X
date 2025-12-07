import msvcrt
import os
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from src.common import TextAlign, TextColor, TextType
from src.ui.xprint import xprint


def is_file_writable(filepath: str) -> bool:
    try:
        if os.path.exists(filepath):
            with open(filepath, "r+b"):
                pass
        return True
    except (IOError, OSError, PermissionError):
        xprint(type=TextType.ERROR, text="File is open in another program.")
        return False


def wait_for_keypress(suffix: str = " to return to the menu", blank_lines: int = 2) -> int:
    for _ in range(blank_lines):
        xprint()
    xprint(text=f"{TextColor.YELLOW + TextColor.FAINT}[Press any key{suffix}]{TextColor.RESET}", align=TextAlign.CENTER)
    while True:
        keypress = msvcrt.getwch()
        return keypress


def display_image(buffer: BytesIO) -> None:
    if os.environ.get("TERM_PROGRAM") != "vscode":
        xprint(type=TextType.INDENT)
        img2sixel = str(Path(os.getcwd()).parent / "h3mex" / "res" / "bin" / "img2sixel.exe")
        subprocess.run([img2sixel, "-I"], input=buffer.getvalue(), stdout=sys.stdout.buffer, check=True)
        sys.stdout.write("\r\n")
        sys.stdout.flush()
    else:
        xprint(type=TextType.ERROR, text="Image display is not supported in the VS Code terminal.")
