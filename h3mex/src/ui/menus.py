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
        ("9", "Global Events"),
        ("0", "Town Events"),
    ]

    _MINIMAP = [
        ("1", "Standard minimap"),
        None,
        ("2", "Custom minimap…"),
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
                ("1", "Replace objects…"),
                None,
                ("2", "Remove objects"),
                None,
                ("3", "Towns…"),
                None,
                ("4", "Heroes…"),
                None,
                ("5", "Monsters: Change level-specific random monsters to any level"),
                ("6", "Monsters: Set monster values"),
                ("7", "Monsters: Set compliant monster values"),
                None,
                ("8", "Treasures: Add treasures"),
                ("9", "Treasures: Fix empty contents"),
                ("0", "Treasures: Add scholars"),
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
                ("M", "Show more…"),
            ],
            [
                ("1", "Towns: Enable all spells/research and all buildings"),
                ("2", "Towns: Add creature bonus events"),
                ("3", "Towns: Add humans to AI-only events"),
                ("4", "Towns: Copy events from source town to target towns"),
                ("5", "Towns: Copy buildings from source town to target towns"),
            ],
            [
                ("1", "Heroes: Reset identity details"),
                ("2", "Heroes: Move heroes from towns to map"),
                ("3", "Heroes: Swap hero indexes"),
            ],
        ],
    }

    EXPORT = {
        "name": "EXPORT",
        "menus": [
            [
                ("1", "JSON: All data"),
                ("2", "JSON: Hero data"),
                ("3", "JSON: Terrain data"),
                ("4", "JSON: Town data"),
                None,
                ("5", "PNG: Normal minimap…"),
                ("6", "PNG: Extended minimap…"),
            ]
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
