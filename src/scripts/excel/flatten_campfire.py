from .format import format_number
from . import sort

RESOURCE_NAMES = {
    0: "Wood",
    1: "Mercury",
    2: "Ore",
    3: "Sulfur",
    4: "Crystal",
    5: "Gems",
    6: "Gold",
}

RESOURCE_IDS = [0, 1, 2, 3, 4, 5, 6]

DEFAULT_SETTING = b'\x00\x00\x00\x00\xff\xff\xff\xff'

def flatten_campfire(campfires):
    rows = []
    for obj in campfires:
        row = {}
        row["coords"] = obj.get("coords", "")
        row["zone_type"] = obj.get("zone_type", "")
        row["zone_color"] = obj.get("zone_color", "")
        row["subtype"] = obj.get("subtype", "")
        resources = obj.get("resources", {})
        mode = obj.get("mode", b"")
        items = list(resources.items())
        if mode == DEFAULT_SETTING:
            row["mode"] = "Custom"
            # Show customized values
            res_strs = []
            for res, val in items:
                res_id = res.value if hasattr(res, "value") else int(res)
                res_strs.append(f"+{format_number(val, as_text=True)} {RESOURCE_NAMES.get(res_id, str(res_id))}")
            row["resources"] = "\n".join(res_strs) if res_strs else ""
        else:
            row["mode"] = "Default"
            row["resources"] = ""
        rows.append(row)

    rows = sort.sort_by_zone(rows)
    return rows
