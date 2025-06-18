from enum import IntEnum

import src.file_io as io

# The general information of a map is stored as follows:
#
# - Map format           | 4 bytes int
# - HotA version         | 4 bytes int
# - unknown data         | 1 byte ???
# - is_arena             | 1 byte bool
# - unknown data         | 8 bytes ???
# - allowed difficulties | 1 byte (bits)
# - has_hero             | 1 byte bool
# - map_size             | 4 bytes int
# - is_two_level         | 1 byte bool
# - name length          | 4 bytes int
# - name                 | X bytes str
# - description length   | 4 bytes int
# - description          | X bytes str
# - difficulty           | 1 byte int
# - level_cap            | 1 byte int

class MapFormat(IntEnum):
    RoE  = 14
    AB   = 21
    SoD  = 28
    CHR  = 29
    HotA = 32
    WoG  = 51

class MapSize(IntEnum):
    S  =  36
    M  =  72
    L  = 108
    XL = 144
    H  = 180
    XH = 216
    G  = 252

class Difficulty(IntEnum):
    Easy       = 0
    Normal     = 1
    Hard       = 2
    Expert     = 3
    Impossible = 4

def parse_general() -> dict:
    info = {
        "map_format"               : 0,
        "hota_version"             : 0,
        "hota_versionMajor"        : 0,
        "hota_versionMinor"        : 0,
        "hota_versionPatch"        : 0,
        "hota_versionLocked"       : 0,
        "is_mirror"                : b'',
        "terrain_type_count"       : b'',
        "name"                     : "",
        "description"              : "",
        "map_size"                 : 0,
        "has_hero"                 : False,
        "is_two_level"             : False,
        "is_arena"                 : False,
        "difficulty"               : 0,
        "allowed_difficulties"     : [],
        "level_cap"                : 0,
        "can_hire_defeated_heroes" : 0,
    }

    info["map_format"] = MapFormat(io.read_int(4))

    if info["map_format"] != MapFormat.HotA:
        raise NotImplementedError(f"unsupported map format: {info['map_format']}")

    info["hota_version"] = io.read_int(4)

    if info["hota_version"] < 8:
        raise NotImplementedError(f"unsupported hota version: {info['hota_version']}")

    info["hota_versionMajor"] = io.read_int(4)
    info["hota_versionMinor"] = io.read_int(4)
    info["hota_versionPatch"] = io.read_int(4)

    info["is_mirror"]                = bool(      io.read_int(1))
    info["is_arena"]                 = bool(      io.read_int(1))
    info["terrain_type_count"]       =            io.read_int(4)
    info["town_type_count"]          =            io.read_int(4)
    info["allowed_difficulties"]     =            io.read_bits(1)
    info["can_hire_defeated_heroes"] = bool(      io.read_int(1))
    info["hota_versionLocked"]       = bool(      io.read_int(1))
    info["has_hero"]                 = bool(      io.read_int(1))
    info["map_size"]                 = MapSize(   io.read_int(4))
    info["is_two_level"]             = bool(      io.read_int(1))
    info["name"]                     =            io.read_str(io.read_int(4))
    info["description"]              =            io.read_str(io.read_int(4))
    info["difficulty"]               = Difficulty(io.read_int(1))
    info["level_cap"]                =            io.read_int(1)

    return info

def write_general(info: dict) -> None:
    io.write_int(    info["map_format"], 4)
    io.write_int(    info["hota_version"], 4)

    io.write_int(    info["is_mirror"], 1)
    io.write_int(    info["is_arena"], 1)
    io.write_int(    info["terrain_type_count"], 4)
    io.write_int(    info["town_type_count"], 4)
    io.write_bits(   info["allowed_difficulties"])
    io.write_int(    info["can_hire_defeated_heroes"], 1)
    io.write_int(    info["has_hero"], 1)
    io.write_int(    info["map_size"], 4)
    io.write_int(    info["is_two_level"], 1)
    io.write_int(len(info["name"]), 4)
    io.write_str(    info["name"])
    io.write_int(len(info["description"]), 4)
    io.write_str(    info["description"])
    io.write_int(    info["difficulty"], 1)
    io.write_int(    info["level_cap"], 1)
