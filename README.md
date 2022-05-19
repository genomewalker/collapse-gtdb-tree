
# collapseGTDB: a tool to collapse a GTDB tree to a certain rank


[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/genomewalker/collapse-gtdb-tree?include_prereleases&label=version)](https://github.com/genomewalker/collapse-gtdb-tree/releases) [![collapse-gtdb-tree](https://github.com/genomewalker/collapse-gtdb-tree/workflows/collapseGTDB_ci/badge.svg)](https://github.com/genomewalker/collapse-gtdb-tree/actions) [![PyPI](https://img.shields.io/pypi/v/collapse-gtdb-tree)](https://pypi.org/project/collapse-gtdb-tree/) [![Conda](https://img.shields.io/conda/v/genomewalker/collapse-gtdb-tree)](https://anaconda.org/genomewalker/collapse-gtdb-tree)

A simple tool to collapse a GTDB to a certain rank.

# Installation

We recommend having [**conda**](https://docs.conda.io/en/latest/) installed to manage the virtual environments

### Using pip

First, we create a conda virtual environment with:

```bash
wget https://raw.githubusercontent.com/genomewalker/collapse-gtdb-tree/master/environment.yml
conda env create -f environment.yml
```

Then we proceed to install using pip:

```bash
pip install collapse-gtdb-tree
```

### Using conda

```bash
conda install -c conda-forge -c bioconda -c genomewalker collapse-gtdb-tree
```

### Install from source to use the development version

Using pip

```bash
pip install git+ssh://git@github.com/genomewalker/collapse-gtdb-tree.git
```

By cloning in a dedicated conda environment

```bash
git clone git@github.com:genomewalker/collapse-gtdb-tree.git
cd collapse-gtdb-tree
conda env create -f environment.yml
conda activate collapse-gtdb-tree
pip install -e .
```


# Usage

collapseGTDB needs the GTDB tree and taxonomy files available from [here](https://gtdb.ecogenomic.org/downloads). Then one can specify one of the following ranks to collapse the tree: `phylum`, `class`, `order`, `family`, `genus` or `all` to run all of them at once. 

For a complete list of options:

```
$ collapseGTDB --help
usage: collapseGTDB [-h] -t TREE -T TAXONOMY [-r RANK] [--debug] [--version]

A simple tool to collapse a GTDB tree to a certain taxonomic rank

optional arguments:
  -h, --help            show this help message and exit
  -t TREE, --tree TREE  GTDB tree file (default: None)
  -T TAXONOMY, --taxonomy TAXONOMY
                        GTDB taxonomy file (default: None)
  -r RANK, --rank RANK  Select taxonomic rank to collapse (default: all)
  --debug               Print debug messages (default: False)
  --version             Print program version
```

One would run `collapseGTDB` as:

```bash
collapseGTDB -t bac120_r86.2.tree -T /Users/ufo/Downloads/test-carlota/bac120_taxonomy_r86.2.tsv -r all
```

This will produce the following files:

```bash
├── bac120_r86_class.tree
├── bac120_r86_family.tree
├── bac120_r86_genus.tree
├── bac120_r86_order.tree
└── bac120_r86_phylum.tree
```



