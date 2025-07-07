import data.spells as spells


def format_spell_list(spell_list):
    """Convert a list of 1s and 0s to readable spell names separated by commas"""
    spell_names = []
    for spell_index, has_spell in enumerate(spell_list):
        if has_spell == 1:
            try:
                spell_enum = spells.ID(spell_index)
                spell_name = spell_enum.name.replace('_', ' ')

                # Special case for Titan's Lightning Bolt
                if spell_name == "Titans Lightning Bolt":
                    spell_name = "Titan's Lightning Bolt"

                spell_names.append(spell_name)
            except ValueError:
                pass

    return ", ".join(spell_names)
