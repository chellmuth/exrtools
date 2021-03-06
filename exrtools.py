import os
import sys

import click
import pyexr

import crop as crop_mod
import split as split_mod

def check_has_channel(exr, channel):
    channels = dump_channels(exr)
    return channel in channels

def dump_channels(exr):
    return [channel for channel in exr.channels]

def filter_exrs_missing_channel(root_path, channel):
    missing = []

    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if filename.endswith(".exr"):
                full_path = os.path.join(root, filename)
                exr = pyexr.open(full_path)
                if not check_has_channel(exr, channel):
                    missing.append(full_path)

    return missing

@click.group()
def cli():
    pass

@cli.command()
@click.argument("filename")
@click.option("--from-shape", nargs=2, type=int, required=True)
@click.option("--to-shape", nargs=2, type=int, required=True)
@click.option("--offset", nargs=2, type=int, required=True)
def crop(filename, from_shape, to_shape, offset):
    crop_mod.crop_filename(filename, filename, from_shape, to_shape, offset)

@cli.command()
@click.argument("filename")
@click.option("--tiles", nargs=2, type=int, required=True)
def split(filename, tiles):
    split_mod.split_filename(filename, tiles)

@cli.command()
@click.argument("filename")
def stats(filename):
    exr = pyexr.open(filename)
    print(exr.get().shape)

@cli.command()
@click.argument("filename")
def channels(filename):
    exr = pyexr.open(filename)
    print(dump_channels(exr))

@cli.command()
@click.argument("root")
@click.argument("channel")
def missing(root, channel):
    missing_exrs = filter_exrs_missing_channel(root, channel)
    print(missing)

@cli.command()
@click.argument("exr_filename", type=click.Path(exists=True))
@click.argument("out_filename", type=click.Path())
@click.option("--channels", "-c", multiple=True, required=True)
def filter(exr_filename, out_filename, channels):
    exr = pyexr.open(exr_filename)
    channel_data = {
        channel: exr.get(channel)
        for channel in channels
    }

    if len(channel_data) == 1:
        channel_data["default"] = channel_data.pop(channels[0])

    pyexr.write(out_filename, channel_data)

if __name__ == "__main__":
    cli()
