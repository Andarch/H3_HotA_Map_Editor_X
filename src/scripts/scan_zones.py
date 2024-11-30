from PIL import Image
import numpy as np
import os
import csv
from ..common import *
import data.objects as objects

def scan_zones(object_data: dict, filename: str) -> bool:
    colors = {
        (255, 0, 0): 'Red',
        (49, 82, 255): 'Blue',
        (156, 115, 82): 'Tan',
        (66, 148, 41): 'Green',
        (255, 132, 0): 'Orange',
        (140, 41, 165): 'Purple',
        (8, 156, 165): 'Teal',
        (198, 123, 140): 'Pink',
    }
    if filename.endswith('.h3m'):
        filename = filename[:-4]

    ground_filename = filename + '_g.png'
    underground_filename = filename + '_u.png'

    zones = {color: [] for color in colors}

    def process_image(image_path, z):
        if not os.path.exists(image_path):
            return
        image = Image.open(image_path).convert('RGBA')
        image_data = np.array(image)
        for y in range(image_data.shape[0]):
            for x in range(image_data.shape[1]):
                pixel = tuple(image_data[y, x][:3])  # Get the RGB values of the pixel
                if pixel in colors:
                    zones[pixel].append((x, y, z))

    # Process ground image
    process_image(ground_filename, 0)

    # Process underground image if it exists
    process_image(underground_filename, 1)

    draw_header()

    xprint(type=Text.ACTION, text=f"Counting objects per zone...")

    zone_counts = {color: {} for color in colors.values()}

    for obj in object_data:
        coords = obj['coords']
        x, y, z = coords
        for color, positions in zones.items():
            if (x, y, z) in positions:
                obj_type = obj['type']
                obj_type_name = objects.ID(obj_type).name
                if obj_type_name not in zone_counts[colors[color]]:
                    zone_counts[colors[color]][obj_type_name] = 0
                zone_counts[colors[color]][obj_type_name] += 1

    # Write the data to a CSV file
    csv_filename = filename + '_zones.csv'
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        header = ['Object Type'] + list(colors.values())
        writer.writerow(header)
        # Write the data
        all_object_types = set()
        for counts in zone_counts.values():
            all_object_types.update(counts.keys())
        for obj_type in sorted(all_object_types):
            row = [obj_type]
            for color in colors.values():
                row.append(zone_counts[color].get(obj_type, 0))
            writer.writerow(row)

    xprint(type=Text.SPECIAL, text=DONE)

    return True
