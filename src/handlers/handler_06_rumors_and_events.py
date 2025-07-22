import src.file_io as io
from .common import *

def parse_rumors() -> list:
    info = []
    rumor_count = io.read_int(4)

    for _ in range(rumor_count):
        rumor = {}
        rumor["name"] = io.read_str(io.read_int(4))
        rumor["text"] = io.read_str(io.read_int(4))
        info.append(rumor)

    return info

def write_rumors(info: list) -> None:
    io.write_int(len(info), 4)

    for rumor in info:
        io.write_int(len(rumor["name"]), 4)
        io.write_str(    rumor["name"])
        io.write_int(len(rumor["text"]), 4)
        io.write_str(    rumor["text"])

def parse_events(is_town: bool = False) -> list:
    info = []
    event_count = io.read_int(4)

    for _ in range(event_count):
        event = {}
        event["isTown"]  = is_town
        event["name"]    = io.read_str(io.read_int(4))
        event["message"] = io.read_str(io.read_int(4))

        event["resources"] = []
        for _ in range(7):
            event["resources"].append(io.read_int(4))

        event["apply_to"]              =      io.read_bits(1)
        event["apply_human"]           = bool(io.read_int(1))
        event["apply_ai"]              = bool(io.read_int(1))
        event["first_occurence"]       =      io.read_int(2)
        event["subsequent_occurences"] =      io.read_int(2)
        event["trash_bytes"]           =      io.read_raw(16)
        event["allowed_difficulties"] =      io.read_int(4)

        if is_town:
            event["hota_town_event_1"]    =      io.read_int(4)
            event["hota_town_event_2"]    =      io.read_int(4)
            event["hota_special"]         =      io.read_bits(6)
            event["apply_neutral_towns"]  = bool(io.read_int(1))
            event["buildings"]            =      io.read_bits(6)

            event["creatures"] = []
            for _ in range(7):
                event["creatures"].append(io.read_int(2))

            event["end_trash"] = io.read_raw(4)

        info.append(event)

    return info

def write_events(info: list, is_town: bool = False) -> None:
    io.write_int(len(info), 4)

    for event in info:
        io.write_int(len(event["name"]), 4)
        io.write_str(    event["name"])
        io.write_int(len(event["message"]), 4)
        io.write_str(    event["message"])

        for resource in event["resources"]:
            io.write_int(resource, 4)

        io.write_bits(event["apply_to"])
        io.write_int( event["apply_human"], 1)
        io.write_int( event["apply_ai"], 1)
        io.write_int( event["first_occurence"], 2)
        io.write_int( event["subsequent_occurences"], 2)
        io.write_raw( event["trash_bytes"])
        io.write_int( event["allowed_difficulties"], 4)

        if is_town:
            io.write_int( event["hota_level_7b"], 4)
            io.write_int( event["hota_amount"], 4)
            io.write_bits(event["hota_special"])
            io.write_int( event["apply_neutral_towns"], 1)
            io.write_bits(event["buildings"])

            for creature in event["creatures"]:
                io.write_int(creature, 2)

            io.write_raw(event["end_trash"])
