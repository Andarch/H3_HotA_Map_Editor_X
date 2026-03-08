from src.common import TextType, map_data
from src.file import file
from src.ui import header
from src.ui.xprint import xprint
from src.utilities import wait_for_keypress


def copy_hota_events_from_other_map():
    other_filename = file.choose_map()
    if not other_filename:
        return

    other_map_data = file.load(other_filename)

    header.draw()

    if not other_map_data["ban_flags"]["has_hota_events"]:
        xprint(type=TextType.ERROR, text="Source map has no HotA events to copy.")
        xprint()
        wait_for_keypress()
        return

    xprint(type=TextType.ACTION, text="Copying HotA events from another map…")

    map_data["ban_flags"]["has_hota_events"] = True
    map_data["ban_flags"]["hota_events"] = other_map_data["ban_flags"]["hota_events"]

    xprint(type=TextType.DONE)
    xprint()
    wait_for_keypress()
