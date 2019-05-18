import os

import pyexr
import numpy as np

import crop

def split_filename(path, tiles):
    exr = pyexr.open(path)
    root_data = {}

    default = exr.get("default")
    height, width, _ = default.shape

    tiles_x, tiles_y = tiles

    tile_width = width // tiles_x
    tile_height = height // tiles_y

    dirname, basename = os.path.split(path)
    name, extension = os.path.splitext(basename)
    split_name = name.split("-")

    split_id = split_name[0]
    split_rest = "-".join(split_name[1:])

    for tile_y in range(tiles_y):
        for tile_x in range(tiles_x):
            tile_index = tile_y * tiles_x + tile_x
            tiled_filename = f"{split_id}_tile{tile_index}-{split_rest}{extension}"

            tiled_path = os.path.join(dirname, tiled_filename)
            print(tiled_path)

            crop.crop_filename(
                path,
                tiled_path,
                (height, width),
                (tile_height, tile_width),
                (tile_y * tile_height, tile_x * tile_width),
            )
