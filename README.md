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

There are two dependencies for the application both of which are installed automatically:

* [gemmi](https://gemmi.readthedocs.io/)
* [requests](https://requests.readthedocs.io/en/master/)

Gemmi can be conveniently installed also using anaconda from conda-forge channel:
```
conda install -c conda-forge gemmi
```

However, there is a [bug](https://github.com/project-gemmi/gemmi/issues/86) in the presently released version of gemmi, that prevents the program from working. This has been fixed in the master branch of the repository, but the installation from repository is much slower than from conda mirror.

## Binary

After installation an executable is made available. Typical use case would look like:

```bash
superposer --help
superposer -o output_dir -u P24941 -p 2vta:A -r 3.0
```

### Parameters - `superposer`

| Parameter   | Type     | Required  | Description |
| :-----------|:--------:| :--------:| :-----------|
| -o, --output-dir       | string   | **Yes**   | Path to the output directory |
| -u, --uniprot-id       | string   | **Yes**   | Uniprot identifier to define PDB chains to be aligned. |
| -p, --pdb-pivot        | string   | **Yes**   | Pivot to be used for alignment in format pdb_id:chain_id e.g. '2vta:A' |
| -r, --rmsd-threshold   | float    | No        | RMSD threshold to accept alignment (Default: 3.0). |

## Unit tests

There are a few basic unit tests that can be run using pytest. Install pytest and run tests to inspect them

```
pip install pytest
pytest
```

## Documentation

There is an option to automatically generate documentation from source code using Sphinx package. You can install relevant packages (from the root directory):

```
pip install -e "[docs]"
```

and generate documentation yourself

```
cd doc
make html
```

and open it from `superposer/doc/build/index.html`.