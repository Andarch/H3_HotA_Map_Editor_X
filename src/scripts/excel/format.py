import data.objects as objects
import data.spells as spells


# Define special case mappings for enum formatting
SPELL_SPECIAL_CASES = {
    "Titans Lightning Bolt": "Titan's Lightning Bolt"
}

ARTIFACT_SPECIAL_CASES = {
    "Admirals Hat": "Admiral's Hat",
    "Lions Shield of Courage": "Lion's Shield of Courage",
    "Ogres Club of Havoc": "Ogre's Club of Havoc",
    "Titans Gladius": "Titan's Gladius",
    "Titans Cuirass": "Titan's Cuirass",
    "Titans Thunder": "Titan's Thunder",
    "Sea Captains Hat": "Sea Captain's Hat",
    "Spellbinders Hat": "Spellbinder's Hat",
    "Wayfarers Boots": "Wayfarer's Boots"
}


def format_enum_list(enum_list, enum_class, special_cases=None):
    """Convert a list of 1s and 0s to readable enum names separated by commas

    Args:
        enum_list: List of 1s and 0s indicating which items are enabled
        enum_class: The enum class to use for name lookup
        special_cases: Dict of special case replacements for formatting
    """
    if special_cases is None:
        special_cases = {}

    names = []
    for index, has_item in enumerate(enum_list):
        if has_item == 1:
            try:
                enum_item = enum_class(index)
                name = enum_item.name.replace('_', ' ')

                # Apply special case formatting if specified
                if name in special_cases:
                    name = special_cases[name]

                names.append(name)
            except ValueError:
                pass

    return ", ".join(names)


def format_special_buildings(special_array, state_filter=None):
    """Convert an array of special building states to readable building names

    Args:
        special_array: List of building states (0=enabled, 1=built, 2=disabled)
        state_filter: If specified, only include buildings with this state value
    """
    if not special_array or not isinstance(special_array, list):
        return ""

    building_names = []

    for building_index, building_state in enumerate(special_array):
        # If state_filter is specified, only include buildings with that state
        # If no filter, include enabled (0) and built (1), skip disabled (2)
        if state_filter is not None:
            if building_state != state_filter:
                continue
        else:
            if building_state not in [0, 1]:
                continue

        try:
            building_enum = objects.Town_Buildings_Special(building_index)
            raw_name = building_enum.name

            # Skip placeholder buildings
            if raw_name.startswith("Special_Building_"):
                continue

            # Format the building name
            formatted_name = raw_name.replace('_', ' ')

            # Extract faction name and format nicely
            if formatted_name.endswith(' Castle'):
                building_name = formatted_name[:-7] + ' (Castle)'
            elif formatted_name.endswith(' Rampart'):
                building_name = formatted_name[:-8] + ' (Rampart)'
            elif formatted_name.endswith(' Tower'):
                building_name = formatted_name[:-6] + ' (Tower)'
            elif formatted_name.endswith(' Inferno'):
                building_name = formatted_name[:-8] + ' (Inferno)'
            elif formatted_name.endswith(' Necropolis'):
                building_name = formatted_name[:-11] + ' (Necropolis)'
            elif formatted_name.endswith(' Dungeon'):
                building_name = formatted_name[:-8] + ' (Dungeon)'
            elif formatted_name.endswith(' Stronghold'):
                building_name = formatted_name[:-11] + ' (Stronghold)'
            elif formatted_name.endswith(' Fortress'):
                building_name = formatted_name[:-9] + ' (Fortress)'
            elif formatted_name.endswith(' Conflux'):
                building_name = formatted_name[:-8] + ' (Conflux)'
            elif formatted_name.endswith(' Cove'):
                building_name = formatted_name[:-5] + ' (Cove)'
            elif formatted_name.endswith(' Factory'):
                building_name = formatted_name[:-8] + ' (Factory)'
            else:
                # No faction suffix or special case, keep as is
                building_name = formatted_name

            building_names.append(building_name)
        except ValueError:
            # Invalid building index, skip
            pass

    return ", ".join(building_names)


def format_number(value, as_text=False):
    """Format a number with commas. If as_text is True, return as string for Excel."""
    if value is None:
        return ""
    s = f"{int(value):,}"
    return s if not as_text else str(s)
