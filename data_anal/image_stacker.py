import numpy as np
from astropy.io import fits
import argparse
import sys
import os
import astroalign as aa
parser = argparse.ArgumentParser()
parser.add_argument("--images", "-i", nargs="+")

base_dir = os.getcwd()

args = parser.parse_args()

image_filenames = args.images
N_images = len(image_filenames)

target_filename = image_filenames[0]
target_image_data = fits.open(target_filename)[0].data.astype(np.uint32)
print(f"Found {N_images} matching the glob, will create a final stacked image stacked_{target_filename}")

for index, image_name in enumerate(image_filenames[1:]):
    source_image_data = fits.open(os.path.join(base_dir, image_name))[0].data
    source_median = np.median(source_image_data)
    register_image_data, footprint = aa.register(source_image_data, target_image_data, fill_value=source_median)
    target_image_data = target_image_data + register_image_data
    print(f"Progress: {100*index/(N_images - 1):.2f}")

final_image_data = target_image_data / N_images
final_image_data = final_image_data.astype(np.uint16)
final_image = fits.PrimaryHDU(final_image_data, header=fits.open(target_filename)[0].header)
final_image.writeto(f"stacked_{target_filename}")
