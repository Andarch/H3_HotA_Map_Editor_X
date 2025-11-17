from src.defs.terrain import ID, River, Road

from . import io


def parse_terrain(general: dict) -> list:
    info = []

    size = general["map_size"]
    has_underground = general["has_underground"]
    tile_amount = size * size * 2 if has_underground else size * size

    for _ in range(tile_amount):
        tile = {
            "terrain_type": ID(io.read_int(1)),
            "terrain_sprite": io.read_int(1),
            "river_type": River(io.read_int(1)),
            "river_sprite": io.read_int(1),
            "road_type": Road(io.read_int(1)),
            "road_sprite": io.read_int(1),
            "mirroring": io.read_bits(1),
        }
        info.append(tile)

    return info


def write_terrain(info: list) -> None:
    for tile in info:
        io.write_int(tile["terrain_type"], 1)
        io.write_int(tile["terrain_sprite"], 1)
        io.write_int(tile["river_type"], 1)
        io.write_int(tile["river_sprite"], 1)
        io.write_int(tile["road_type"], 1)
        io.write_int(tile["road_sprite"], 1)
        io.write_bits(tile["mirroring"])
