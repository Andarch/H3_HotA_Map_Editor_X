from core.h3m import artifacts, objects
from src.common import MsgType, map_data, wait_for_keypress, xprint


def fix_empty_contents() -> None:
    xprint(type=MsgType.ACTION, text="Fixing empty contents in objects…")

    target_ids = {
        objects.ID.Sea_Chest,
        objects.ID.Shipwreck_Survivor,
        objects.ID.Treasure_Chest,
        objects.ID.Warriors_Tomb,
    }
    empty_markers = {
        artifacts.ID.Empty_1_Byte,
        artifacts.ID.Empty_2_Bytes,
        artifacts.ID.Empty_Unknown,
        artifacts.ID.Empty_4_Bytes,
    }

    def enum_name_by_value(enum_cls, value: int) -> str:
        try:
            return enum_cls(value).name
        except ValueError:
            return f"0x{value:08X}"

    count = 0
    for obj in map_data["object_data"]:
        oid = obj.get("id")
        if oid in target_ids:
            contents = obj.get("contents")
            if contents in empty_markers:
                obj["artifact"] = contents
                count += 1
                xprint(
                    type=MsgType.INFO,
                    text=f"{obj.get('type')} at {obj.get('coords')} contains {enum_name_by_value(artifacts.ID, contents)}",
                )
    xprint()
    xprint(type=MsgType.INFO, text=f"Updated {count} objects.")

    wait_for_keypress()
