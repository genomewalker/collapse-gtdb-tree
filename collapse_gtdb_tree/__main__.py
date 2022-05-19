"""
 Copyright (c) 2022 Antonio Fernandez-Guerra

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """


import logging
from collapse_gtdb_tree.utils import (
    get_arguments,
)
import pandas as pd
from ete3 import Tree
import os
from pathlib import Path

log = logging.getLogger("my_logger")


def create_collapsed_tree_files(file, ranks):
    """
    Create collapsed tree files
    """
    # get file name from path
    file_name = Path(file).resolve().stem.split(".")[0]
    files = {}
    for rank in ranks:
        files[rank] = f"{file_name}_{rank}.tree"
    return files


def collapse_gtdb_tree_by_rank(tree, taxonomy, ranks, files):
    for rank in ranks:
        t = tree.copy()
        df = taxonomy[["genome_id", rank]]
        df = df.groupby([rank]).agg(lambda x: x.iloc[0]).reset_index()
        ids = df.set_index(
            "genome_id",
        ).to_dict()[rank]
        t.prune(list(ids.keys()))
        logging.info(f"Pruned tree for {rank} [leaves: {len(t.get_leaves()):,}]")
        # rename leaves
        for leaf in t.iter_leaves():
            leaf.name = ids[leaf.name]
        t.write(outfile=str(files[rank]), quoted_node_names=True, format=1)


def main():

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s ::: %(asctime)s ::: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args = get_arguments()
    logging.getLogger("my_logger").setLevel(
        logging.DEBUG if args.debug else logging.INFO
    )

    # Read taxonomy file
    logging.info(f"Reading taxonomy file {os.path.basename(args.taxonomy)}")
    taxonomy_file = pd.read_csv(
        args.taxonomy, sep="\t", names=["genome_id", "tax_string"]
    )
    ranks = ["domain", "phylum", "class", "order", "family", "genus", "species"]

    taxonomy_file[ranks] = taxonomy_file.tax_string.str.split(
        ";",
        expand=True,
    )
    logging.info(f"Read tree file {os.path.basename(args.tree)}")
    tree = Tree(args.tree, quoted_node_names=True, format=1)
    logging.info(f"Read tree with {len(tree.get_leaves()):,} leaves")
    tips = [x.name for x in tree.iter_leaves()]
    taxonomy_file = taxonomy_file[taxonomy_file["genome_id"].isin(tips)]

    files = create_collapsed_tree_files(args.tree, args.rank)
    # get list of ids by ranks
    collapse_gtdb_tree_by_rank(
        tree=tree, taxonomy=taxonomy_file, ranks=args.rank, files=files
    )


if __name__ == "__main__":
    main()
