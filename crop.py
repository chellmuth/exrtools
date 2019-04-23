import sys

from shutil import copyfile

import pyexr
import numpy as np

def crop_filename(filename, from_shape, to_shape, offset, keep_orig=False):
    exr = pyexr.open(filename)
    root_data = {}

    default = exr.get("default")
    assert default.shape[:2] == from_shape

    for channel, data in exr.get_all().items():
        new_data = np.empty((to_shape[0], to_shape[1], data.shape[2]))

        for y in range(new_data.shape[0]):
            for x in range(new_data.shape[1]):
                new_data[y][x] = data[y + offset[0]][x + offset[1]]
                new_data[y][x] = data[y + offset[0]][x + offset[1]]
                new_data[y][x] = data[y + offset[0]][x + offset[1]]

        root_data[channel] = new_data

    if keep_orig:
        copyfile(filename, filename + ".orig")

    pyexr.write(filename, root_data)
