from enum import Enum

class Menu(Enum):
    START = {
        1: "Load 1 map",
        2: "Load 2 maps",
       -1: "",
       -2: "",
        0: "Exit"
    }
    MAP_IO = {
        1: "Load",
        2: "Save"
    }
    LOAD  = {
        1: "Load 1 map",
        2: "Load 2 maps"
    }
    SAVE_A = {
        1: "Save 1 map",
        2: "Save 2 maps"
    }
    SAVE_B = {
        1: "Save",
        2: "Save as"
    }
    MAIN  = {
        1: "Load / Save",
       -1: "",
        2: "!!Display map data",
        3: "!!Count objects",
        4: "Reset heroes",
        5: "Export .json file",
       -2: "",
        6: "!!Swap layers",
        7: "Modify towns (buildings/spells)",
        8: "Generate minimap",
        9: "!!Update events (global/town)",
       -3: "",
       -4: "",
        0: "Exit"
    }
    PRINT = {
        1: "General",
        2: "Players/Teams",
        3: "Win/Loss Conditions",
        4: "Heroes",
        5: "Disabled Skills/Spells",
        6: "Terrain",
        7: "Object Defs",
        8: "Object Data",
        9: "Events & Rumors",
        0: "Null Bytes"
    }
    JSON  = {
        1: "All data",
        2: "Hero data",
        3: "Terrain data"
    }
    MINIMAP  = {
        1: "Normal",
        2: "Passability only"
    }
