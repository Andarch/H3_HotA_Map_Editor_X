from enum import Enum


class Menu(Enum):
    MAIN = {
        1: "View…",
        2: "Edit…",
        -1: "",
        3: "Save",
        4: "Save as…",
        -2: "",
        5: "Export…",
        -3: "",
        6: "Load…",
        7: "Reload",
        -4: "",
        0: "Exit",
    }

    DATA = {
        1: "Map Specs",
        2: "Player Specs",
        3: "Start Heroes",
        4: "Rumors",
        5: "Hero Data",
        6: "Terrain",
        7: "Object Defs",
        8: "Object Data",
        9: "Events",
    }

    VIEW = {
        1: "Map data",
        -1: "",
        2: "Terrain: List unreachable tiles",
    }

    EDIT = {
        1: "Towns: Enable spell research, spells, and buildings",
        2: "Towns: Create events",
        -1: "",
        3: "Heroes: Reset identity details",
        -2: "",
        4: "Change random monster 1-7 to any level",
        5: "Set compliant monster values",
    }

    EXPORT = {
        1: "Excel: Object data",
        -1: "",
        2: "JSON: All data",
        3: "JSON: Hero data",
        4: "JSON: Terrain data",
        5: "JSON: Town data",
        -2: "",
        6: "PNG: Normal minimap",
        7: "PNG: Extended minimap",
    }
