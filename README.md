# Superposer

This is an example Python application demonstrating basic use case of superposing all proteins from PDB given the uniprot id, threshold and pivot. Documentation of the process and individual components is [here](https://lpravda.github.io/example/)

## Installation instructions

`superposer` is best to be run in conda environment. The official documentaion has installation instructions for a variety of platforms. For linux/mac OS this is most easily done using the with commands similar to:

```
conda create -n test-env python=3.7
conda activate test-env
```

Once you have the environment installed and activated, install the application either from repository:

```
pip install git+https://github.com/lpravda/example.git
```

or clone the repository and install it from source

```
pip install -e .
```

## Dependencies

There are three dependencies for this application. All are installed automatically, however gemmi is installed from conda much faster than from pip (see below):

* [gemmi](https://gemmi.readthedocs.io/)
* [pandas](https://pandas.pydata.org/)
* [requests](https://requests.readthedocs.io/en/master/)

Gemmi can be conveniently installed from conda-forge channel:
```
conda install -c conda-forge "gemmi>=0.4.5"
```

The version specified needs to be 0.4.5 or greater as there is a [bug](https://github.com/project-gemmi/gemmi/issues/86) in the previous version of gemmi, that prevents the program from working.

## Binary

After installation an executable is made available. Typical use case would look like:

```bash
superposer --help
superposer -o output_dir -u P24941 -p 2vta:A -r 3.0
```

The binary then downloads all the relevant chains, superpose them to the pivot, writes out the superposed coordinates and prints out some basic statistics on RMSD using `pandas` package.

### Parameters - `superposer`

| Parameter   | Type     | Required  | Description |
| :-----------|:--------:| :--------:| :-----------|
| -o, --output-dir       | string   | **Yes**   | Path to the output directory |
| -u, --uniprot-id       | string   | **Yes**   | Uniprot identifier to define PDB chains to be aligned. |
| -p, --pdb-pivot        | string   | **Yes**   | Pivot to be used for alignment in format pdb_id:chain_id e.g. '2vta:A' |
| -r, --rmsd-threshold   | float    | No        | RMSD threshold to accept alignment (Default: 3.0). |
| -t, --threads          | int      | No        | Number of threads to be used. |

## Unit tests

There are a few basic unit tests that can be run using pytest. Install pytest and run tests to inspect them

```
pip install pytest
pytest
```

## Documentation

There is an option to automatically generate documentation from source code using Sphinx package. You can install relevant packages (from the root directory):

```
pip install -e ".[docs]"
```

and generate documentation yourself

```
cd doc
make html
```

and open it from `superposer/doc/build/index.html`.