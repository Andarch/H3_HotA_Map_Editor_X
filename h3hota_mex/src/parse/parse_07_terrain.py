from enum import IntEnum

from .. import file_io as io


class Tile(IntEnum):
    TerrainType = 0
    TerrainPicture = 1
    RiverType = 2
    RiverPicture = 3
    RoadType = 4
    RoadPicture = 5
    Mirroring = 6


class TerrainType(IntEnum):
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


class RiverType(IntEnum):
    Empty = 0
    Clear = 1
    Icy = 2
    Muddy = 3
    Lava = 4


class RoadType(IntEnum):
    Empty = 0
    Dirt = 1
    Gravel = 2
    Cobblestone = 3


def parse_terrain(map_specs: dict) -> list:
    info = []

    size = map_specs["map_size"]
    has_underground = map_specs["has_underground"]
    tile_amount = size * size * 2 if has_underground else size * size

    for _ in range(tile_amount):  # 7 bytes per tile:
        tile = {
            "terrain_type_int": io.read_int(1),
            "terrain_sprite": io.read_int(1),
            "river_type_int": io.read_int(1),
            "river_sprite": io.read_int(1),
            "road_type_int": io.read_int(1),
            "road_sprite": io.read_int(1),
            "mirroring": io.read_bits(1),
        }
        tile["terrain_type"] = TerrainType(tile["terrain_type_int"])
        tile["river_type"] = RiverType(tile["river_type_int"])
        tile["road_type"] = RoadType(tile["road_type_int"])
        info.append(tile)

    return info


def write_terrain(info: list) -> None:
    for tile in info:
        io.write_int(tile["terrain_type_int"], 1)
        io.write_int(tile["terrain_sprite"], 1)
        io.write_int(tile["river_type_int"], 1)
        io.write_int(tile["river_sprite"], 1)
        io.write_int(tile["road_type_int"], 1)
        io.write_int(tile["road_sprite"], 1)
        io.write_bits(tile["mirroring"])
