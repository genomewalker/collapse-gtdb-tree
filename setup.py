from setuptools import setup
import versioneer

requirements = [
    "pandas>=1.4.2",
    "tqdm>=4.62.3",
    "ete3>=3.1.2",
]

setup(
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        "setuptools>=39.1.0",
        "Cython>=0.29.24",
    ],
    name="collapse-gtdb-tree",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A simple tool to collapse the reference GTDB tree at a scpecific rank",
    license="MIT",
    author="Antonio Fernandez-Guerra",
    author_email="antonio@metagenomics.eu",
    url="https://github.com/genomewalker/collapse-gtdb-tree",
    packages=["collapse_gtdb_tree"],
    entry_points={"console_scripts": ["collapseGTDB=collapse_gtdb_tree.__main__:main"]},
    install_requires=requirements,
    keywords="collapse-gtdb-tree,GTDB",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
