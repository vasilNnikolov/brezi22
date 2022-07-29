import numpy as np
from astropy.io import fits
import argparse
import sys
import os
parser = argparse.ArgumentParser()
parser.add_argument("--name")

base_dir = os.getcwd()

args = parser.parse_args()

print(fits.open(os.path.join(base_dir, args.name))[0].header)

