import numpy as np
from astropy.io import fits
import argparse
import sys
import os
parser = argparse.ArgumentParser()
parser.add_argument("--images", "-i", nargs="+")
parser.add_argument("--image_dark", "-id")
parser.add_argument("--master_flat", "-f")

base_dir = os.getcwd()

args = parser.parse_args()

raw_image_filenames = args.images
print(f"Found {len(raw_image_filenames)} raw images, which will be transformed to clean_<image_name>.fit")
image_dark_data = fits.open(os.path.join(base_dir, args.image_dark))[0].data.astype(np.int32)
master_flat_data = fits.open(os.path.join(base_dir, args.master_flat))[0].data

master_flat_normalised_data = master_flat_data / np.median(master_flat_data)
# remove hot and cold pixels from flat

def remove_outliers(px_value): 
    if px_value < 0.1: 
        return 1.0
    return px_value

vectorized_outlier_remover = np.vectorize(remove_outliers)

master_flat_normalised_data = vectorized_outlier_remover(master_flat_normalised_data)
print(f"master flat min {np.min(master_flat_normalised_data)}, max {np.max(master_flat_normalised_data)}")
print("removed outliers from flat")

for index, filename in enumerate(raw_image_filenames): 
    raw_image = fits.open(os.path.join(base_dir, filename))[0]

    clean_image_data = (raw_image.data.astype(np.int32) - image_dark_data) / master_flat_normalised_data
    clean_image_data = clean_image_data.astype(np.int32)
    # set pixels where dark was brighter than image to 0
    clean_image_data[clean_image_data < 0] = 0
    clean_image_data[clean_image_data >= 2**16 - 1] = 2**16 - 1 
    print(f"clean image data min {np.min(clean_image_data)} max {np.max(clean_image_data)}")

    clean_image = fits.PrimaryHDU(clean_image_data.astype(np.uint16), header=raw_image.header)   

    clean_image.writeto(f"clean_{filename}")
    print(f"Progress: {100*index/len(raw_image_filenames):.2f}")
