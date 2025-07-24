from enum import IntEnum

import src.file_io as io


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
    tile = {
        "terrain_type": TerrainType.Dirt,
        "terrain_sprite": 0,
        "river_type": RiverType.Empty,
        "river_sprite": 0,
        "road_type": RoadType.Empty,
        "road_sprite": 0,
        "mirroring": [],
    }

    size = map_specs["map_size"]
    has_underground = map_specs["has_underground"]
    tile_amount = size * size * 2 if has_underground else size * size

    for _ in range(tile_amount):  # 7 bytes per tile:
        tile["terrain_type"] = TerrainType(io.read_int(1))
        tile["terrain_sprite"] = io.read_int(1)
        tile["river_type"] = RiverType(io.read_int(1))
        tile["river_sprite"] = io.read_int(1)
        tile["road_type"] = RoadType(io.read_int(1))
        tile["road_sprite"] = io.read_int(1)
        tile["mirroring"] = io.read_bits(1)
        info.append(tile)
        # info.append(
        #     [
        #         TerrainType(io.read_int(1)),  # Byte 1: Terrain type
        #         io.read_int(1),  # Byte 2: Terrain picture
        #         RiverType(io.read_int(1)),  # Byte 3: River type
        #         io.read_int(1),  # Byte 4: River picture
        #         RoadType(io.read_int(1)),  # Byte 5: Road type
        #         io.read_int(1),  # Byte 6: Road picture
        #         io.read_bits(1),  # Byte 7: Tile mirroring
        #     ]
        # )

    return info


def write_terrain(info: list) -> None:
    for tile in info:
        for i in tile:
            io.write_int(i, 1)
