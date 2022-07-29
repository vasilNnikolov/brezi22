import numpy as np
from astropy.io import fits
import argparse
import sys
import os
parser = argparse.ArgumentParser()
parser.add_argument("--images", "-i", nargs="+")
parser.add_argument("--image_dark", "-id")
parser.add_argument("--flat", "-f")
parser.add_argument("--flat_dark", "-fd")


base_dir = os.getcwd()

args = parser.parse_args()

print(f"flats: {args.flats}")
print(f"master dark of flats: {args.dark}")
print(f"output file: {args.output}")
all_flat_filenames = args.flats
for filename in all_flat_filenames:
    print(f"flat {filename}")

print(f"Found {len(all_flat_filenames)} flats")

dstack = np.dstack([fits.open(filename)[0].data for filename in all_flat_filenames])
master_dark_filename = args.dark
master_dark_data = fits.open(master_dark_filename)[0].data
final_flat_data = np.median(dstack, axis=2).astype(np.uint16) - master_dark_data

master_flat_image = fits.PrimaryHDU(final_flat_data) 
master_flat_filename = os.path.join(base_dir, args.output)
master_flat_image.writeto(master_flat_filename)
print(f"Master dark created in {master_flat_filename}")




