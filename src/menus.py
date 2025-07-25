from enum import Enum


class Menu(Enum):
    MAIN = {
        1: "INFO",
        2: "EDIT",
        -1: "",
        3: "EXPORT EXCEL",
        4: "EXPORT JSON",
        5: "EXPORT MINIMAP",
        -2: "",
        6: "QUICK RELOAD",
        7: "QUICK SAVE",
        8: "LOAD",
        9: "SAVE",
        -3: "",
        0: "EXIT",
    }

    INFO = {
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

    EDIT = {
        1: "Modify towns (buildings/spells)",
        2: "Reset heroes",
        -1: "",
        3: "List unreachable tiles",
        4: "Change random monster 1-7 to any level",
        5: "Set compliant monster values",
    }

    LOAD = {1: "Load 1 map", 2: "Load 2 maps"}
    SAVE_A = {1: "Save 1 map", 2: "Save 2 maps"}
    SAVE_B = {1: "Save", 2: "Save as"}

    JSON = {1: "All data", 2: "Hero data", 3: "Terrain data"}

    MINIMAP = {1: "Normal", 2: "All layers"}
