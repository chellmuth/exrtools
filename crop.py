import sys

from shutil import copyfile

import pyexr
import numpy as np

def crop_filename(
    source_filename, destination_filename,
    from_shape, to_shape, offset,
    keep_orig=False
):
    exr = pyexr.open(source_filename)
    root_data = {}

    default = exr.get("default")
    assert default.shape[:2] == from_shape

    for channel, data in exr.get_all().items():
        channel_data = data[
            offset[0]:offset[0]+to_shape[0],
            offset[1]:offset[1]+to_shape[1],
            :
        ]

        root_data[channel] = channel_data

    pyexr.write(destination_filename, root_data)
