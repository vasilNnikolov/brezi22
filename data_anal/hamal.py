import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import argparse
import sys
import os
import astroalign as aa
from astropy.visualization import ZScaleInterval
parser = argparse.ArgumentParser()
parser.add_argument("--images", "-i", nargs="+")

base_dir = os.getcwd()

args = parser.parse_args()

image_filenames = args.images
N_images = len(image_filenames)

target_filename = image_filenames[0]
target_image_data = fits.open(target_filename)[0].data.astype(np.uint32)
print(f"Found {N_images} matching the glob, will create a final stacked image stacked_{target_filename}")

images = [fits.open(os.path.join(base_dir, fn))[0].data for fn in image_filenames]

stack = np.min(np.dstack(images), axis=2)
kdf = np.array([2,3,5,6,100])
print(np.median(kdf))
phdu = fits.PrimaryHDU(stack)
phdu.writeto("aaaaaaaaaaaaaaaa.fits")
# transformed_images = []
# tau = [image_filenames[x] for x in [i, i+1, i+2]]
# print(tau)
# for image_name in tau:
#     source_image_data = fits.open(os.path.join(base_dir, image_name))[0].data
#     source_median = np.median(source_image_data)
#     register_image_data, footprint = aa.register(source_image_data, target_image_data, fill_value=source_median)
#     transformed_images.append(register_image_data)

# print(transformed_images)
# final_image_data = np.median(np.dstack(tuple(transformed_images)), axis=2)
# ims_for_mean.append(final_image_data)
# im_for_mean = fits.PrimaryHDU(final_image_data.astype(np.uint16), header=fits.open(target_filename)[0].header)
# im_for_mean.writeto(f"stacked_median_{image_filenames[i]}")

# res_data = np.mean(np.dstack(ims_for_mean), axis=2).astype(np.uint16)
# res = fits.PrimaryHDU(res_data, header=fits.open(target_filename)[0].header)
# res.writeto(f"stacked_average_final_{target_filename}")
