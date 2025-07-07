import data.heroes as heroes
import os


def get_portrait_path(portrait_id, hero_data=None):
    # Handle default portrait case
    if portrait_id is None or portrait_id == 255:  # Default portrait
        if hero_data and "default_name" in hero_data:
            default_name = hero_data["default_name"]
            if default_name:
                # Use the default name to find the portrait
                filename = f"{default_name}.bmp"

                # Get the full path to the portrait file
                script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                portrait_path = os.path.join(script_dir, "portraits", filename)

                # Only return path if file exists
                if os.path.exists(portrait_path):
                    return portrait_path
        return ""

    try:
        # Get the portrait enum name
        portrait_enum = heroes.Portrait(portrait_id)
        portrait_name = portrait_enum.name

        # Handle special cases
        if portrait_name.endswith('_campaign'):
            # Remove '_campaign' and add ' (campaign)'
            base_name = portrait_name[:-9]  # Remove '_campaign'
            filename = f"{base_name} (campaign).bmp"
        elif portrait_name.startswith('Tarnum_'):
            # Convert Tarnum_Barbarian to Tarnum (Barbarian)
            class_name = portrait_name[7:]  # Remove 'Tarnum_'
            filename = f"Tarnum ({class_name}).bmp"
        else:
            # Standard conversion: replace underscores with spaces
            filename = portrait_name.replace('_', ' ') + '.bmp'

        # Get the full path to the portrait file
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        portrait_path = os.path.join(script_dir, "portraits", filename)

        # Only return path if file exists
        if os.path.exists(portrait_path):
            return portrait_path
        else:
            return ""
    except (ValueError, AttributeError):
        # Invalid portrait ID or other error
        return ""
