from enum import IntEnum


class ID(IntEnum):
    Dirt = 0
    Sand = 1
    Grass = 2
    Snow = 3
    Swamp = 4
    Rough = 5
    Subterranean = 6
    Lava = 7
    Water = 8
    Rock = 9
    Highlands = 10
    Wasteland = 11


class River(IntEnum):
    Empty = 0
    Clear = 1
    Icy = 2
    Muddy = 3
    Lava = 4


class Road(IntEnum):
    Empty = 0
    Dirt = 1
    Gravel = 2
    Cobblestone = 3
