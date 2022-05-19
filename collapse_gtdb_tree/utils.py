import argparse
import sys
import gzip
import os
import logging
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull
from collapse_gtdb_tree import __version__
import time


log = logging.getLogger("my_logger")
log.setLevel(logging.INFO)
timestr = time.strftime("%Y%m%d-%H%M%S")


def is_debug():
    return logging.getLogger("my_logger").getEffectiveLevel() == logging.DEBUG


filters = ["breadth", "depth", "depth_evenness", "breadth_expected_ratio"]

# From https://stackoverflow.com/a/59617044/15704171
def convert_list_to_str(lst):
    n = len(lst)
    if not n:
        return ""
    if n == 1:
        return lst[0]
    return ", ".join(lst[:-1]) + f" or {lst[-1]}"


def get_compression_type(filename):
    """
    Attempts to guess the compression (if any) on a file using the first few bytes.
    http://stackoverflow.com/questions/13044562
    """
    magic_dict = {
        "gz": (b"\x1f", b"\x8b", b"\x08"),
        "bz2": (b"\x42", b"\x5a", b"\x68"),
        "zip": (b"\x50", b"\x4b", b"\x03", b"\x04"),
    }
    max_len = max(len(x) for x in magic_dict)

    unknown_file = open(filename, "rb")
    file_start = unknown_file.read(max_len)
    unknown_file.close()
    compression_type = "plain"
    for file_type, magic_bytes in magic_dict.items():
        if file_start.startswith(magic_bytes):
            compression_type = file_type
    if compression_type == "bz2":
        sys.exit("Error: cannot use bzip2 format - use gzip instead")
        sys.exit("Error: cannot use zip format - use gzip instead")
    return compression_type


def get_open_func(filename):
    if get_compression_type(filename) == "gz":
        return gzip.open
    else:  # plain text
        return open


# From: https://stackoverflow.com/a/11541450
def is_valid_file(parser, arg, var):
    if not os.path.exists(arg):
        parser.error("argument %s: The file %s does not exist!" % (var, arg))
    else:
        return arg


def get_ranks(parser, ranks, var):
    valid_ranks = ["all", "phylum", "class", "order", "family", "genus"]
    ranks = ranks.split(",")
    # check if ranks are valid
    for rank in ranks:
        if rank not in valid_ranks:
            parser.error(
                f"argument {var}: Invalid value {rank}.\Rank has to be one of {convert_list_to_str(valid_ranks)}"
            )
        if rank == "all":
            ranks = valid_ranks[1:]
    return ranks


defaults = {
    "rank": "all",
}

help_msg = {
    "tree": f"GTDB tree file",
    "taxonomy": f"GTDB taxonomy file",
    "rank": f"Select taxonomic rank to collapse",
    "debug": f"Print debug messages",
    "version": f"Print program version",
}


def get_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description="A simple tool to collapse a GTDB tree to a certain taxonomic rank",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--tree",
        type=lambda x: is_valid_file(parser, x, "--tree"),
        help=help_msg["tree"],
        required=True,
    )
    parser.add_argument(
        "-T",
        "--taxonomy",
        type=lambda x: is_valid_file(parser, x, "--taxonomy"),
        help=help_msg["taxonomy"],
        required=True,
    )
    # this is an argument to comma separated list of ranks for which to collapse
    parser.add_argument(
        "-r",
        "--rank",
        type=lambda x: get_ranks(parser, x, "--rank"),
        default=defaults["rank"],
        help=help_msg["rank"],
    )
    parser.add_argument(
        "--debug", dest="debug", action="store_true", help=help_msg["debug"]
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help=help_msg["version"],
    )
    args = parser.parse_args(None if sys.argv[1:] else ["-h"])
    return args


@contextmanager
def suppress_stdout():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)
