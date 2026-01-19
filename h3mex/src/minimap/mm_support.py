from enum import IntEnum

from src.defs import objects


class MMAction(IntEnum):
    VIEW = 1
    EXPORT = 2


class MMType(IntEnum):
    STANDARD = 1
    EXTENDED = 2


class ObjectMask(IntEnum):
    ROWS = 6
    COLUMNS = 8


BLOCKED_TERRAIN_ID_OFFSET = 20


class MMTerrainID(IntEnum):
    # normal
    DIRT = 0
    SAND = 1
    GRASS = 2
    SNOW = 3
    SWAMP = 4
    ROUGH = 5
    SUBTERRANEAN = 6
    LAVA = 7
    WATER = 8
    ROCK = 9
    HIGHLANDS = 10
    WASTELAND = 11

    # blocked
    BDIRT = 20
    BSAND = 21
    BGRASS = 22
    BSNOW = 23
    BSWAMP = 24
    BROUGH = 25
    BSUBTERRANEAN = 26
    BLAVA = 27
    BWATER = 28
    BROCK = 29
    BHIGHLANDS = 30
    BWASTELAND = 31


KM_ID_OFFSET = 1000
MP1_ID_OFFSET = 3000
MP2_ID_OFFSET = 3500


class MMObjectID(IntEnum):
    RED = 0
    BLUE = 1
    TAN = 2
    GREEN = 3
    ORANGE = 4
    PURPLE = 5
    TEAL = 6
    PINK = 7
    NEUTRAL = 255

    KM_LIGHTBLUE = 1000
    KM_GREEN = 1001
    KM_RED = 1002
    KM_DARKBLUE = 1003
    KM_BROWN = 1004
    KM_PURPLE = 1005
    KM_WHITE = 1006
    KM_BLACK = 1007

    GARRISON = 1999
    QUEST = 2000

    M1_BLUE = 3000
    M1_PINK = 3001
    M1_ORANGE = 3002
    M1_YELLOW = 3003
    P1_PURPLE = 3004
    P1_ORANGE = 3005
    P1_RED = 3006
    P1_CYAN = 3007
    M1_TURQUOISE = 3008
    M1_VIOLET = 3009
    M1_CHARTREUSE = 3010
    M1_WHITE = 3011

    M2_GREEN = 3500
    M2_BROWN = 3501
    M2_VIOLET = 3502
    M2_ORANGE = 3503
    P2_GREEN = 3504
    P2_YELLOW = 3505
    P2_RED = 3506
    P2_CYAN = 3507
    S2_WHITE = 3508
    M2_PINK = 3509
    M2_TURQUOISE = 3510
    M2_YELLOW = 3511
    M2_BLACK = 3512
    P2_CHARTREUSE = 3513
    P2_TURQUOISE = 3514
    P2_VIOLET = 3515
    P2_ORANGE = 3516
    M2_BLUE = 3517
    M2_RED = 3518
    P2_PINK = 3519
    P2_BLUE = 3520
    S2_RED = 3521
    S2_BLUE = 3522
    S2_CHARTREUSE = 3523
    S2_YELLOW = 3524

    REDWOOD = 4000
    PILLAR = 4001

    ALL_OTHERS = 10000


MM_TERRAIN_COLORS = {
    # Terrain
    MMTerrainID.DIRT: (0x52, 0x39, 0x08),
    MMTerrainID.SAND: (0xDE, 0xCE, 0x8C),
    MMTerrainID.GRASS: (0x00, 0x42, 0x00),
    MMTerrainID.SNOW: (0xB5, 0xC6, 0xC6),
    MMTerrainID.SWAMP: (0x4A, 0x84, 0x6B),
    MMTerrainID.ROUGH: (0x84, 0x73, 0x31),
    MMTerrainID.SUBTERRANEAN: (0x84, 0x31, 0x00),
    MMTerrainID.LAVA: (0x4A, 0x4A, 0x4A),
    MMTerrainID.WATER: (0x08, 0x52, 0x94),
    MMTerrainID.ROCK: (0x00, 0x00, 0x00),
    MMTerrainID.HIGHLANDS: (0x29, 0x73, 0x18),
    MMTerrainID.WASTELAND: (0xBD, 0x5A, 0x08),
    # Blocked Terrain
    MMTerrainID.BDIRT: (0x39, 0x29, 0x08),
    MMTerrainID.BSAND: (0xA5, 0x9C, 0x6B),
    MMTerrainID.BGRASS: (0x00, 0x31, 0x00),
    MMTerrainID.BSNOW: (0x8C, 0x9C, 0x9C),
    MMTerrainID.BSWAMP: (0x21, 0x5A, 0x42),
    MMTerrainID.BROUGH: (0x63, 0x52, 0x21),
    MMTerrainID.BSUBTERRANEAN: (0x5A, 0x08, 0x00),
    MMTerrainID.BLAVA: (0x29, 0x29, 0x29),
    MMTerrainID.BWATER: (0x00, 0x29, 0x6B),
    MMTerrainID.BROCK: (0x00, 0x00, 0x00),
    MMTerrainID.BHIGHLANDS: (0x21, 0x52, 0x10),
    MMTerrainID.BWASTELAND: (0x9C, 0x42, 0x08),
}

MM_TERRAIN_COLORS_ALT = {
    # Terrain
    MMTerrainID.DIRT: (0x4D, 0x4D, 0x4D),
    MMTerrainID.SAND: (0x4D, 0x4D, 0x4D),
    MMTerrainID.GRASS: (0x4D, 0x4D, 0x4D),
    MMTerrainID.SNOW: (0x4D, 0x4D, 0x4D),
    MMTerrainID.SWAMP: (0x4D, 0x4D, 0x4D),
    MMTerrainID.ROUGH: (0x4D, 0x4D, 0x4D),
    MMTerrainID.SUBTERRANEAN: (0x4D, 0x4D, 0x4D),
    MMTerrainID.LAVA: (0x4D, 0x4D, 0x4D),
    MMTerrainID.WATER: (0x4B, 0x56, 0x5E),
    MMTerrainID.ROCK: (0x00, 0x00, 0x00),
    MMTerrainID.HIGHLANDS: (0x4D, 0x4D, 0x4D),
    MMTerrainID.WASTELAND: (0x4D, 0x4D, 0x4D),
    # Blocked Terrain
    MMTerrainID.BDIRT: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BSAND: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BGRASS: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BSNOW: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BSWAMP: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BROUGH: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BSUBTERRANEAN: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BLAVA: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BWATER: (0x3C, 0x45, 0x4D),
    MMTerrainID.BROCK: (0x00, 0x00, 0x00),
    MMTerrainID.BHIGHLANDS: (0x3D, 0x3D, 0x3D),
    MMTerrainID.BWASTELAND: (0x3D, 0x3D, 0x3D),
}

MM_OBJECT_COLORS = {
    MMObjectID.RED: (0xFF, 0x00, 0x00),
    MMObjectID.BLUE: (0x31, 0x52, 0xFF),
    MMObjectID.TAN: (0x9C, 0x73, 0x52),
    MMObjectID.GREEN: (0x42, 0x94, 0x29),
    MMObjectID.ORANGE: (0xFF, 0x84, 0x00),
    MMObjectID.PURPLE: (0x8C, 0x29, 0xA5),
    MMObjectID.TEAL: (0x08, 0x9C, 0xA5),
    MMObjectID.PINK: (0xC6, 0x7B, 0x8C),
    MMObjectID.NEUTRAL: (0x84, 0x84, 0x84),
    MMObjectID.KM_LIGHTBLUE: (0x00, 0xB7, 0xFF),
    MMObjectID.KM_GREEN: (0x06, 0xC6, 0x2F),
    MMObjectID.KM_RED: (0xCE, 0x19, 0x1A),
    MMObjectID.KM_DARKBLUE: (0x14, 0x14, 0xFE),
    MMObjectID.KM_BROWN: (0xC8, 0x82, 0x46),
    MMObjectID.KM_PURPLE: (0xA8, 0x43, 0xE0),
    MMObjectID.KM_WHITE: (0xF7, 0xF7, 0xF7),
    MMObjectID.KM_BLACK: (0x12, 0x12, 0x12),
    MMObjectID.GARRISON: (0x9C, 0x9A, 0x8B),
    MMObjectID.QUEST: (0xFF, 0xFF, 0x00),
    MMObjectID.M1_BLUE: (0x1E, 0x40, 0xCF),
    MMObjectID.M1_PINK: (0xF7, 0x38, 0xA6),
    MMObjectID.M1_ORANGE: (0xFF, 0x8C, 0x1A),
    MMObjectID.M1_YELLOW: (0xFF, 0xF7, 0x1A),
    MMObjectID.P1_PURPLE: (0x8E, 0x44, 0xAD),
    MMObjectID.P1_ORANGE: (0xFF, 0xB3, 0x47),
    MMObjectID.P1_RED: (0xE7, 0x2B, 0x2B),
    MMObjectID.P1_CYAN: (0x1A, 0xE6, 0xE6),
    MMObjectID.M1_TURQUOISE: (0x1A, 0xC6, 0xB7),
    MMObjectID.M1_VIOLET: (0x7C, 0x3C, 0xBD),
    MMObjectID.M1_CHARTREUSE: (0x7D, 0xFF, 0x1A),
    MMObjectID.M1_WHITE: (0xF7, 0xF7, 0xF7),
    MMObjectID.M2_GREEN: (0x1A, 0xB5, 0x3B),
    MMObjectID.M2_BROWN: (0x8B, 0x5C, 0x2B),
    MMObjectID.M2_VIOLET: (0xB0, 0x5D, 0xE6),
    MMObjectID.M2_ORANGE: (0xFF, 0x6F, 0x00),
    MMObjectID.P2_GREEN: (0x3B, 0xE6, 0x1A),
    MMObjectID.P2_YELLOW: (0xFF, 0xE6, 0x1A),
    MMObjectID.P2_RED: (0xD9, 0x2B, 0x2B),
    MMObjectID.P2_CYAN: (0x1A, 0xB5, 0xE6),
    MMObjectID.S2_WHITE: (0xFF, 0xFF, 0xFF),
    MMObjectID.M2_PINK: (0xFF, 0x69, 0xB4),
    MMObjectID.M2_TURQUOISE: (0x40, 0xE0, 0xD0),
    MMObjectID.M2_YELLOW: (0xFF, 0xFF, 0x99),
    MMObjectID.M2_BLACK: (0x22, 0x22, 0x22),
    MMObjectID.P2_CHARTREUSE: (0x7F, 0xFF, 0x00),
    MMObjectID.P2_TURQUOISE: (0x00, 0xFF, 0xFF),
    MMObjectID.P2_VIOLET: (0xEE, 0x82, 0xEE),
    MMObjectID.P2_ORANGE: (0xFF, 0xA5, 0x00),
    MMObjectID.M2_BLUE: (0x00, 0x7F, 0xFF),
    MMObjectID.M2_RED: (0xFF, 0x45, 0x00),
    MMObjectID.P2_PINK: (0xFF, 0xC0, 0xCB),
    MMObjectID.P2_BLUE: (0x00, 0x00, 0xFF),
    MMObjectID.S2_RED: (0xB2, 0x22, 0x22),
    MMObjectID.S2_BLUE: (0x41, 0x69, 0xE1),
    MMObjectID.S2_CHARTREUSE: (0xAD, 0xFF, 0x2F),
    MMObjectID.S2_YELLOW: (0xFF, 0xFA, 0xCD),
    MMObjectID.REDWOOD: (0xFF, 0x00, 0x00),
    MMObjectID.PILLAR: (0xFF, 0xFF, 0x00),
    MMObjectID.ALL_OTHERS: (0xFF, 0xFF, 0xFF),
}

MM_STANDARD_IGNORED_OBJECTS = {
    objects.ID.Hero,
    objects.ID.Prison,
    objects.ID.Random_Hero,
    objects.ID.Hero_Placeholder,
}

MM_BASE2_IGNORED_OBJECTS = {
    objects.ID.Treasure_Chest,
    objects.ID.Scholar,
    objects.ID.Campfire,
    objects.ID.Flotsam,
    objects.ID.Sea_Chest,
    objects.ID.Shipwreck_Survivor,
    objects.ID.Ocean_Bottle,
    objects.ID.Grail,
    objects.ID.Monster,
    objects.ID.Event_Object,
    objects.ID.Artifact,
    objects.ID.Pandoras_Box,
    objects.ID.Spell_Scroll,
    objects.ID.HotA_Pickup,
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
