import os

import pyexr
import numpy as np

import crop

def split_filename(filename, tiles):
    exr = pyexr.open(filename)
    root_data = {}

    default = exr.get("default")
    height, width, _ = default.shape

    tiles_x, tiles_y = tiles

    tile_width = width // tiles_x
    tile_height = height // tiles_y

    name, extension = os.path.splitext(filename)

    for tile_y in range(tiles_y):
        for tile_x in range(tiles_x):
            tile_index = tile_y * tiles_x + tile_x
            tiled_filename = f"{name}-tile{tile_index}{extension}"

            crop.crop_filename(
                filename,
                tiled_filename,
                (height, width),
                (tile_height, tile_width),
                (tile_y * tile_height, tile_x * tile_width),
            )
