from enum import Enum

class Menu(Enum):
    # START = {
    #     1: "Load 1 map",
    #     2: "Load 2 maps",
    #    -1: "",
    #    -2: "",
    #     0: "Exit"
    # }

    MAIN  = {
        1: "INFO",
        2: "EDIT",
       -1: "",
        3: "EXPORT JSON",
        4: "EXPORT MINIMAP",
       -2: "",
        5: "QUICK RELOAD",
        6: "QUICK SAVE",
        7: "LOAD",
        8: "SAVE",
       -3: "",
        0: "EXIT"
    }

    INFO = {
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

    EDIT  = {
        1: "Modify towns (buildings/spells)",
        2: "Reset heroes",
        3: "!!Swap layers",
        4: "!!Update events (global/town)"
    }

    # MAP_IO = {
    #     1: "Load",
    #     2: "Save"
    # }

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

    JSON  = {
        1: "All data",
        2: "Hero data",
        3: "Terrain data"
    }

    MINIMAP  = {
        1: "Normal",
        2: "Passability only"
    }
