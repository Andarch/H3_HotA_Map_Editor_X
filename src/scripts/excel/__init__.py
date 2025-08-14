"""Excel export helpers package.

This initializer exposes commonly used submodules and functions so callers can
do `from src.scripts import excel` and then access `excel.format` and
`excel.flatten_*` helpers directly.
"""

# Re-export submodules used by flatteners and exporters
from . import format, sort  # noqa: F401
from .flatten_ancient_lamp import flatten_ancient_lamp  # noqa: F401
from .flatten_artifacts import flatten_artifacts  # noqa: F401
from .flatten_campfire import flatten_campfire  # noqa: F401
from .flatten_creature_banks import flatten_creature_banks  # noqa: F401
from .flatten_events import flatten_events  # noqa: F401
from .flatten_flotsam_jetsam import flatten_flotsam_jetsam  # noqa: F401
from .flatten_garrisons import flatten_garrisons  # noqa: F401
from .flatten_grave import flatten_grave  # noqa: F401

# Re-export flatten functions for convenient access
from .flatten_heroes import flatten_heroes  # noqa: F401
from .flatten_monsters import flatten_monsters  # noqa: F401
from .flatten_resources import flatten_resources  # noqa: F401
from .flatten_scholar import flatten_scholar  # noqa: F401
from .flatten_sea_barrel import flatten_sea_barrel  # noqa: F401
from .flatten_sea_chest import flatten_sea_chest  # noqa: F401
from .flatten_shipwreck_survivor import flatten_shipwreck_survivor  # noqa: F401
from .flatten_spells import flatten_spells  # noqa: F401
from .flatten_town_events import flatten_town_events  # noqa: F401
from .flatten_towns import flatten_towns  # noqa: F401
from .flatten_treasure_chest import flatten_treasure_chest  # noqa: F401
from .flatten_vial_of_mana import flatten_vial_of_mana  # noqa: F401

__all__ = [
    # submodules
    "format",
    "sort",
    # flatteners
    "flatten_heroes",
    "flatten_towns",
    "flatten_monsters",
    "flatten_spells",
    "flatten_artifacts",
    "flatten_resources",
    "flatten_campfire",
    "flatten_scholar",
    "flatten_treasure_chest",
    "flatten_sea_chest",
    "flatten_shipwreck_survivor",
    "flatten_flotsam_jetsam",
    "flatten_sea_barrel",
    "flatten_vial_of_mana",
    "flatten_ancient_lamp",
    "flatten_grave",
    "flatten_creature_banks",
    "flatten_garrisons",
    "flatten_town_events",
    "flatten_events",
]
