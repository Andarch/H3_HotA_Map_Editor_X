import data.objects as objects


def format_building_list(building_list):
    """Convert a list of 1s and 0s to readable building names separated by commas"""
    building_names = []
    for building_index, has_building in enumerate(building_list):
        if has_building == 1:
            try:
                building_enum = objects.Town_Buildings(building_index)
                building_name = building_enum.name.replace('_', ' ')
                building_names.append(building_name)
            except ValueError:
                pass

    return ", ".join(building_names)
