from src.defs import objects, players, terrain


class TerrainRGB:
    _ROCK_RGB = (0x00, 0x00, 0x00)
    _LAND_RGB = (0x4D, 0x4D, 0x4D)
    _ALT_LAND_RGB = (0x3D, 0x3D, 0x3D)

    passable = {
        terrain.ID.Dirt: (0x52, 0x39, 0x08),
        terrain.ID.Sand: (0xDE, 0xCE, 0x8C),
        terrain.ID.Grass: (0x00, 0x42, 0x00),
        terrain.ID.Snow: (0xB5, 0xC6, 0xC6),
        terrain.ID.Swamp: (0x4A, 0x84, 0x6B),
        terrain.ID.Rough: (0x84, 0x73, 0x31),
        terrain.ID.Subterranean: (0x84, 0x31, 0x00),
        terrain.ID.Lava: (0x4A, 0x4A, 0x4A),
        terrain.ID.Water: (0x08, 0x52, 0x94),
        terrain.ID.Rock: _ROCK_RGB,
        terrain.ID.Highlands: (0x29, 0x73, 0x18),
        terrain.ID.Wasteland: (0xBD, 0x5A, 0x08),
    }

    blocked = {
        terrain.ID.Dirt: (0x39, 0x29, 0x08),
        terrain.ID.Sand: (0xA5, 0x9C, 0x6B),
        terrain.ID.Grass: (0x00, 0x31, 0x00),
        terrain.ID.Snow: (0x8C, 0x9C, 0x9C),
        terrain.ID.Swamp: (0x21, 0x5A, 0x42),
        terrain.ID.Rough: (0x63, 0x52, 0x21),
        terrain.ID.Subterranean: (0x5A, 0x08, 0x00),
        terrain.ID.Lava: (0x29, 0x29, 0x29),
        terrain.ID.Water: (0x00, 0x29, 0x6B),
        terrain.ID.Rock: _ROCK_RGB,
        terrain.ID.Highlands: (0x21, 0x52, 0x10),
        terrain.ID.Wasteland: (0x9C, 0x42, 0x08),
    }

    alt_passable = {
        terrain.ID.Dirt: _LAND_RGB,
        terrain.ID.Sand: _LAND_RGB,
        terrain.ID.Grass: _LAND_RGB,
        terrain.ID.Snow: _LAND_RGB,
        terrain.ID.Swamp: _LAND_RGB,
        terrain.ID.Rough: _LAND_RGB,
        terrain.ID.Subterranean: _LAND_RGB,
        terrain.ID.Lava: _LAND_RGB,
        terrain.ID.Water: (0x4B, 0x56, 0x5E),
        terrain.ID.Rock: _ROCK_RGB,
        terrain.ID.Highlands: _LAND_RGB,
        terrain.ID.Wasteland: _LAND_RGB,
    }

    alt_blocked = {
        terrain.ID.Dirt: _ALT_LAND_RGB,
        terrain.ID.Sand: _ALT_LAND_RGB,
        terrain.ID.Grass: _ALT_LAND_RGB,
        terrain.ID.Snow: _ALT_LAND_RGB,
        terrain.ID.Swamp: _ALT_LAND_RGB,
        terrain.ID.Rough: _ALT_LAND_RGB,
        terrain.ID.Subterranean: _ALT_LAND_RGB,
        terrain.ID.Lava: _ALT_LAND_RGB,
        terrain.ID.Water: (0x3C, 0x45, 0x4D),
        terrain.ID.Rock: _ROCK_RGB,
        terrain.ID.Highlands: _ALT_LAND_RGB,
        terrain.ID.Wasteland: _ALT_LAND_RGB,
    }


class ObjectRGB:
    _QUEST_RGB = (0xFF, 0xFF, 0x00)
    _GARRISON_RGB = (0x9C, 0x9A, 0x8B)
    _INTERACTIVE_RGB = (0xFF, 0x00, 0xFF)

    player = {
        players.ID.Red: (0xFF, 0x00, 0x00),
        players.ID.Blue: (0x31, 0x52, 0xFF),
        players.ID.Tan: (0x9C, 0x73, 0x52),
        players.ID.Green: (0x42, 0x94, 0x29),
        players.ID.Orange: (0xFF, 0x84, 0x00),
        players.ID.Purple: (0x8C, 0x29, 0xA5),
        players.ID.Teal: (0x08, 0x9C, 0xA5),
        players.ID.Pink: (0xC6, 0x7B, 0x8C),
        players.ID.Neutral: (0x84, 0x84, 0x84),
    }

    border = {
        objects.SubID.Border.Light_Blue: (0x00, 0xB7, 0xFF),
        objects.SubID.Border.Green: (0x06, 0xC6, 0x2F),
        objects.SubID.Border.Red: (0xCE, 0x19, 0x1A),
        objects.SubID.Border.Dark_Blue: (0x14, 0x14, 0xFE),
        objects.SubID.Border.Brown: (0xC8, 0x82, 0x46),
        objects.SubID.Border.Purple: (0xA8, 0x43, 0xE0),
        objects.SubID.Border.White: (0xF7, 0xF7, 0xF7),
        objects.SubID.Border.Black: (0x12, 0x12, 0x12),
        objects.SubID.Border.Quest_Gate: _QUEST_RGB,
    }

    quest = {objects.ID.Quest_Guard: _QUEST_RGB}

    garrison = {
        objects.ID.Garrison: _GARRISON_RGB,
        objects.ID.Garrison_Vertical: _GARRISON_RGB,
    }

    monolith_portal = {
        objects.SubID.MonolithPortal.OneWay.Small_Blue: (0x1E, 0x40, 0xCF),
        objects.SubID.MonolithPortal.OneWay.Small_Pink: (0xF7, 0x38, 0xA6),
        objects.SubID.MonolithPortal.OneWay.Small_Orange: (0xFF, 0x8C, 0x1A),
        objects.SubID.MonolithPortal.OneWay.Small_Yellow: (0xFF, 0xF7, 0x1A),
        objects.SubID.MonolithPortal.OneWay.Big_Purple: (0x8E, 0x44, 0xAD),
        objects.SubID.MonolithPortal.OneWay.Big_Orange: (0xFF, 0xB3, 0x47),
        objects.SubID.MonolithPortal.OneWay.Big_Red: (0xE7, 0x2B, 0x2B),
        objects.SubID.MonolithPortal.OneWay.Big_Cyan: (0x1A, 0xE6, 0xE6),
        objects.SubID.MonolithPortal.OneWay.Small_Turquoise: (0x1A, 0xC6, 0xB7),
        objects.SubID.MonolithPortal.OneWay.Small_Violet: (0x7C, 0x3C, 0xBD),
        objects.SubID.MonolithPortal.OneWay.Small_Chartreuse: (0x7D, 0xFF, 0x1A),
        objects.SubID.MonolithPortal.OneWay.Small_White: (0xF7, 0xF7, 0xF7),
        objects.SubID.MonolithPortal.TwoWay.Small_Green: (0x1A, 0xB5, 0x3B),
        objects.SubID.MonolithPortal.TwoWay.Small_Brown: (0x8B, 0x5C, 0x2B),
        objects.SubID.MonolithPortal.TwoWay.Small_Violet: (0xB0, 0x5D, 0xE6),
        objects.SubID.MonolithPortal.TwoWay.Small_Orange: (0xFF, 0x6F, 0x00),
        objects.SubID.MonolithPortal.TwoWay.Big_Green: (0x3B, 0xE6, 0x1A),
        objects.SubID.MonolithPortal.TwoWay.Big_Yellow: (0xFF, 0xE6, 0x1A),
        objects.SubID.MonolithPortal.TwoWay.Big_Red: (0xD9, 0x2B, 0x2B),
        objects.SubID.MonolithPortal.TwoWay.Big_Cyan: (0x1A, 0xB5, 0xE6),
        objects.SubID.MonolithPortal.TwoWay.Water_White: (0xFF, 0xFF, 0xFF),
        objects.SubID.MonolithPortal.TwoWay.Small_Pink: (0xFF, 0x69, 0xB4),
        objects.SubID.MonolithPortal.TwoWay.Small_Turquoise: (0x40, 0xE0, 0xD0),
        objects.SubID.MonolithPortal.TwoWay.Small_Yellow: (0xFF, 0xFF, 0x99),
        objects.SubID.MonolithPortal.TwoWay.Small_Black: (0x22, 0x22, 0x22),
        objects.SubID.MonolithPortal.TwoWay.Big_Chartreuse: (0x7F, 0xFF, 0x00),
        objects.SubID.MonolithPortal.TwoWay.Big_Turquoise: (0x00, 0xFF, 0xFF),
        objects.SubID.MonolithPortal.TwoWay.Big_Violet: (0xEE, 0x82, 0xEE),
        objects.SubID.MonolithPortal.TwoWay.Big_Orange: (0xFF, 0xA5, 0x00),
        objects.SubID.MonolithPortal.TwoWay.Small_Blue: (0x00, 0x7F, 0xFF),
        objects.SubID.MonolithPortal.TwoWay.Small_Red: (0xFF, 0x45, 0x00),
        objects.SubID.MonolithPortal.TwoWay.Big_Pink: (0xFF, 0xC0, 0xCB),
        objects.SubID.MonolithPortal.TwoWay.Big_Blue: (0x00, 0x00, 0xFF),
        objects.SubID.MonolithPortal.TwoWay.Water_Red: (0xB2, 0x22, 0x22),
        objects.SubID.MonolithPortal.TwoWay.Water_Blue: (0x41, 0x69, 0xE1),
        objects.SubID.MonolithPortal.TwoWay.Water_Chartreuse: (0xAD, 0xFF, 0x2F),
        objects.SubID.MonolithPortal.TwoWay.Water_Yellow: (0xFF, 0xFA, 0xCD),
    }


class ObjectGroup:
    IGNORED_STANDARD = {
        objects.ID.Hero,
        objects.ID.Prison,
        objects.ID.Random_Hero,
        objects.ID.Hero_Placeholder,
    }

    IGNORED_EX_BASE2 = {
        objects.ID.Treasure_Chest,
        objects.ID.Scholar,
        objects.ID.Campfire,
        objects.ID.Flotsam,
        objects.ID.Sea_Chest,
        objects.ID.Shipwreck_Survivor,
        objects.ID.Ocean_Bottle,
        objects.ID.Grail,
        objects.ID.Monster,
        objects.ID.Event,
        objects.ID.Artifact,
        objects.ID.Pandoras_Box,
        objects.ID.Spell_Scroll,
        objects.ID.HotA_Collectible,
        objects.ID.Random_Artifact,
        objects.ID.Random_Treasure_Artifact,
        objects.ID.Random_Minor_Artifact,
        objects.ID.Random_Major_Artifact,
        objects.ID.Random_Relic,
        objects.ID.Random_Monster,
        objects.ID.Random_Monster_1,
        objects.ID.Random_Monster_2,
        objects.ID.Random_Monster_3,
        objects.ID.Random_Monster_4,
        objects.ID.Random_Monster_5,
        objects.ID.Random_Monster_6,
        objects.ID.Random_Monster_7,
        objects.ID.Random_Resource,
        objects.ID.Resource,
        objects.ID.Boat,
    }

    BARRIERS = {
        objects.ID.Border_Gate,
        objects.ID.Border_Guard,
        objects.ID.Garrison,
        objects.ID.Garrison_Vertical,
        objects.ID.Quest_Guard,
    }

    TWO_WAY_LAND_PORTALS = {
        objects.SubID.MonolithPortal.TwoWay.Small_Green,
        objects.SubID.MonolithPortal.TwoWay.Small_Brown,
        objects.SubID.MonolithPortal.TwoWay.Small_Violet,
        objects.SubID.MonolithPortal.TwoWay.Small_Orange,
        objects.SubID.MonolithPortal.TwoWay.Big_Green,
        objects.SubID.MonolithPortal.TwoWay.Big_Yellow,
        objects.SubID.MonolithPortal.TwoWay.Big_Red,
        objects.SubID.MonolithPortal.TwoWay.Big_Cyan,
        objects.SubID.MonolithPortal.TwoWay.Small_Pink,
        objects.SubID.MonolithPortal.TwoWay.Small_Turquoise,
        objects.SubID.MonolithPortal.TwoWay.Small_Yellow,
        objects.SubID.MonolithPortal.TwoWay.Small_Black,
        objects.SubID.MonolithPortal.TwoWay.Big_Chartreuse,
        objects.SubID.MonolithPortal.TwoWay.Big_Turquoise,
        objects.SubID.MonolithPortal.TwoWay.Big_Violet,
        objects.SubID.MonolithPortal.TwoWay.Big_Orange,
        objects.SubID.MonolithPortal.TwoWay.Small_Blue,
        objects.SubID.MonolithPortal.TwoWay.Small_Red,
        objects.SubID.MonolithPortal.TwoWay.Big_Pink,
        objects.SubID.MonolithPortal.TwoWay.Big_Blue,
    }

    TWO_WAY_SEA_PORTALS = {
        objects.SubID.MonolithPortal.TwoWay.Water_White,
        objects.SubID.MonolithPortal.TwoWay.Water_Red,
        objects.SubID.MonolithPortal.TwoWay.Water_Blue,
        objects.SubID.MonolithPortal.TwoWay.Water_Chartreuse,
        objects.SubID.MonolithPortal.TwoWay.Water_Yellow,
    }

    MONSTERS = {
        objects.ID.Monster,
        objects.ID.Random_Monster,
        objects.ID.Random_Monster_1,
        objects.ID.Random_Monster_2,
        objects.ID.Random_Monster_3,
        objects.ID.Random_Monster_4,
        objects.ID.Random_Monster_5,
        objects.ID.Random_Monster_6,
        objects.ID.Random_Monster_7,
    }

    RESOURCES = {objects.ID.Resource, objects.ID.Random_Resource}
