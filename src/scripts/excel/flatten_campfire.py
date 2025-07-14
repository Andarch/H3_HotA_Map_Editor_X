from .format import format_number
import data.objects as objects

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
    """
    Flattens campfire objects for Excel export.
    Adds 'Coords', 'Subtype', 'Mode', and 'Resources' columns.
    """
    rows = []
    for obj in campfires:
        row = {}
        row["Coords"] = obj.get("coords", "")
        row["Zone"] = obj.get("zone", "")
        row["Subtype"] = obj.get("subtype", "")
        resources = obj.get("resources", {})
        mode = obj.get("mode", b"")
        items = list(resources.items())
        if mode == DEFAULT_SETTING:
            row["Mode"] = "Custom"
            # Show customized values
            res_strs = []
            for res, val in items:
                res_id = res.value if hasattr(res, "value") else int(res)
                res_strs.append(f"+{format_number(val, as_text=True)} {RESOURCE_NAMES.get(res_id, str(res_id))}")
            row["Resources"] = "\n".join(res_strs) if res_strs else ""
        else:
            row["Mode"] = "Default"
            row["Resources"] = ""
        rows.append(row)
    return rows
