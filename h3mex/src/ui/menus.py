class Menu:
    _H3M = [
        ("1", "General"),
        ("2", "Player Specs"),
        ("3", "Start Heroes"),
        ("4", "Rumors"),
        ("5", "Hero Data"),
        ("6", "Terrain"),
        ("7", "Object Defs"),
        ("8", "Object Data"),
        ("9", "Events"),
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
                ("0", "Exit"),
            ]
        ],
    }

    VIEW = {
        "name": "VIEW",
        "menus": [
            [
                *_H3M,
                None,
                ("S", "Special…"),
            ],
            [("1", "Terrain: Unreachable tile coordinates")],
        ],
    }

    EDIT = {
        "name": "EDIT",
        "menus": [
            [
                ("1", "Towns: Enable spell research, all spells, and all buildings"),
                ("2", "Towns: Add creature bonus events"),
                None,
                ("3", "Heroes: Reset identity details"),
                None,
                ("4", "Monsters: Change level-specific random monsters to any level"),
                ("5", "Monsters: Set monster values"),
                ("6", "Monsters: Set compliant monster values"),
                None,
                ("7", "Treasures: Add treasures"),
            ]
        ],
    }

    EXPORT = {
        "name": "EXPORT",
        "menus": [
            [
                ("1", "Excel: Object data"),
                None,
                ("2", "JSON: All data"),
                ("3", "JSON: Hero data"),
                ("4", "JSON: Terrain data"),
                ("5", "JSON: Town data"),
                None,
                ("6", "PNG: Normal minimap"),
                ("7", "PNG: Extended minimap"),
            ]
        ],
    }
