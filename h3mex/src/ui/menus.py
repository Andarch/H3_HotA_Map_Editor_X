import msvcrt

from src.common import Cursor, Keypress, TextAlign, TextColor, TextType

from . import header
from .xprint import _clean_text, xprint


class GenericMenu:
    def display(menu: tuple[str, list]) -> str:
        def _read_keypress() -> str:
            keypress = msvcrt.getwch()
            if keypress in ["\x00", "\xe0"]:
                extended_key = msvcrt.getwch()
                if extended_key == "P":
                    return Keypress.DOWN
                if extended_key == "H":
                    return Keypress.UP
            return keypress

        header.draw()
        name = menu[0]
        items = menu[1]
        width = 0
        for item in items:
            text = _clean_text(item)
            w = len(text)
            if w > width:
                width = w
        xprint(text=f"{name}", align=TextAlign.CENTER)
        xprint()
        selected_index = 0
        while True:
            for i, item in enumerate(items):
                if i == selected_index:
                    xprint(type=TextType.GENERIC_MENU, text=f"{TextColor.INVERTED}{item}", menu_width=width)
                else:
                    xprint(type=TextType.GENERIC_MENU, text=item, menu_width=width)
            xprint()
            keypress = _read_keypress()
            if keypress == Keypress.DOWN:
                selected_index = (selected_index + 1) % len(items)
                for _ in range(len(items) + 1):
                    print(Cursor.RESET, end="")
            elif keypress == Keypress.UP:
                selected_index = (selected_index - 1) % len(items)
                for _ in range(len(items) + 1):
                    print(Cursor.RESET, end="")
            elif keypress == Keypress.ENTER:
                return int(selected_index)
            elif keypress == Keypress.ESC:
                return keypress


class NumberedMenu:
    def display(menu: tuple[str, list]) -> str:
        header.draw()
        name = menu[0]
        items = menu[1]
        width = 0
        for item in items:
            if item is None:
                continue
            text = _clean_text(item[1])
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
                xprint(type=TextType.NUMBERED_MENU, text=item[1], menu_num=item[0], menu_width=width)
            else:
                xprint()
        xprint()
        while True:
            keypress = msvcrt.getwch()
            if keypress.upper() in valid_keys:
                return keypress.upper()

    _H3M = [
        ("1", "General"),
        ("2", "Player Specs"),
        ("3", "Start Heroes"),
        ("4", "Ban Flags"),
        ("5", "Rumors"),
        ("6", "Hero Data"),
        ("7", "Terrain"),
        ("8", "Object Defs"),
        ("9", "Object Data"),
        ("0", "Town Events"),
        ("E", "Global Events"),
    ]

    _MINIMAP = [
        ("1", "Standard minimap"),
        None,
        ("2", "Extended minimap…"),
        ("3", "Extended minimap with zone types…"),
        ("4", "Extended minimap with zone owners…"),
    ]

    MAIN = {
        "name": "MAIN MENU",
        "menus": [
            [
                ("1", "View…"),
                ("2", "Edit…"),
                None,
                ("3", "Save"),
                ("4", "Save as…"),
                None,
                ("5", "Export…"),
                None,
                ("6", "Load…"),
                ("7", "Reload"),
                None,
                None,
                ("ESC", "Exit"),
            ]
        ],
    }

    VIEW = {
        "name": "VIEW",
        "menus": [
            [
                *_H3M,
                None,
                ("M", "Minimap…"),
                None,
                ("S", "Special…"),
            ],
            [
                ("1", "Terrain: Unreachable tile coordinates"),
                None,
                ("2", "Zones: Invalid objects"),
            ],
        ],
    }

    EDIT = {
        "name": "EDIT",
        "menus": [
            [
                ("1", "Replace objects"),
                ("2", "Remove objects"),
                None,
                ("3", "Towns…"),
                ("4", "Heroes…"),
                ("5", "Monsters…"),
                ("6", "Treasures…"),
                None,
                ("M", "Show more…"),
            ],
            [
                ("1", "Event Objects: Add explorer bonuses"),
                ("2", "Event Objects: Delete explorer bonuses"),
                ("3", "Event Objects: Modify AI main hero boost"),
                None,
                ("4", "Pandora's Boxes: Modify contents"),
                None,
                ("5", "Seers' Huts: Modify seers' huts"),
                None,
                ("6", "Garrisons: Copy garrison guards"),
                ("7", "Garrisons: Fill empty garrisons with guards"),
                None,
                ("8", "Abandoned Mines: Modify abandoned mines"),
                None,
                ("M", "Show more…"),
            ],
            [
                ("1", "Towns: Enable all spells/research and all buildings"),
                ("2", "Towns: Add creature bonus events"),
                ("3", "Towns: Add fourth-town events"),
                ("4", "Towns: Add mega-town events"),
                ("5", "Towns: Add humans to AI-only events"),
                ("6", "Towns: Copy events from source town to target towns"),
                ("7", "Towns: Copy buildings from source town to target towns"),
            ],
            [
                ("1", "Heroes: Reset identity details"),
                ("2", "Heroes: Move heroes from towns to map"),
                ("3", "Heroes: Swap hero indexes"),
            ],
            [
                ("1", "Monsters: Change non-level-specific random monsters to level 1-7"),
                ("2", "Monsters: Set monster quantities"),
                ("3", "Monsters: Set compliant monster values"),
                ("4", "Monsters: Set monster flee values"),
                ("5", "Monsters: Make compliant monsters not grow"),
                ("6", "Monsters: Make non-compliant monsters grow"),
                ("7", "Monsters: Increase creature stashes"),
            ],
            [
                ("1", "Treasures: Add treasures"),
                ("2", "Treasures: Fix empty contents"),
                ("3", "Treasures: Add scholars"),
                ("4", "Treasures: Remove sea treasures"),
                ("5", "Treasures: Modify treasure rewards"),
            ],
        ],
    }

    EXPORT = {
        "name": "EXPORT",
        "menus": [
            [
                ("1", "PNG: Standard minimap"),
                ("2", "PNG: Extended minimap"),
                None,
                ("3", "JSON…"),
            ],
            [*_H3M],
        ],
    }

    VIEW_MINIMAP = {
        "name": "VIEW MINIMAP",
        "menus": [[*_MINIMAP]],
    }

    EXPORT_MINIMAP = {
        "name": "EXPORT MINIMAP",
        "menus": [[*_MINIMAP]],
    }
