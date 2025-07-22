import math

import src.file_io as io


def parse_flags() -> dict:
    info = {
        "allow_plague": 0,
        "combo_artifact_count": 0,
        "combo_artifacts": [],
        "combat_round_limit": 0,
        "unhandled_bytes": b"",
        "artifacts": [],
        "spells": [],
        "skills": [],
    }

    info["allow_plague"] = bool(io.read_int(4))

    info["combo_artifact_count"] = io.read_int(4)
    combo_artifact_bytes = math.ceil(info["combo_artifact_count"] / 8)
    info["combo_artifacts"] = io.read_bits(combo_artifact_bytes)

    info["combat_round_limit"] = io.read_int(4)
    info["unhandled_bytes"] = io.read_raw(8)

    info["artifact_count"] = io.read_int(4)
    artifact_bytes = math.ceil(info["artifact_count"] / 8)
    info["artifacts"] = io.read_bits(artifact_bytes)

    info["spells"] = io.read_bits(9)
    info["skills"] = io.read_bits(4)

    return info


def write_flags(info: dict) -> None:
    io.write_int(info["allow_plague"], 4)
    io.write_int(info["combo_artifact_count"], 4)
    io.write_bits(info["combo_artifacts"])
    io.write_int(info["combat_round_limit"], 4)
    io.write_raw(info["unhandled_bytes"])
    io.write_int(info["artifact_count"], 4)
    io.write_bits(info["artifacts"])
    io.write_bits(info["spells"])
    io.write_bits(info["skills"])
