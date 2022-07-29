import numpy as np
from astropy.io import fits
import argparse
import sys
import os
parser = argparse.ArgumentParser()
parser.add_argument("--darks", "-d", nargs="+")
parser.add_argument("--output", "-o")

base_dir = os.getcwd()

args = parser.parse_args()

print(f"darks: {args.darks}")
print(f"output file: {args.output}")
all_dark_filenames = args.darks 
for filename in all_dark_filenames:
    print(f"dark {filename}")

print(f"Found {len(all_dark_filenames)} darks")

dstack = np.dstack([fits.open(filename)[0].data for filename in all_dark_filenames])
print(dstack.dtype)
final_dark_data = np.median(dstack, axis=2).astype(np.uint16)
print(final_dark_data.dtype)


master_dark_image = fits.PrimaryHDU(final_dark_data) 
master_dark_filename = os.path.join(base_dir, args.output)
master_dark_image.writeto(master_dark_filename)
print(f"Master dark created in {master_dark_filename}")




