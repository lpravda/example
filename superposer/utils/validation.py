import os
import re
from argparse import ArgumentTypeError
from collections import namedtuple

import requests
from superposer.core import resources

pdb_id_re = r"\d{1}\w{3}"

# gracefully taken from: https://www.uniprot.org/help/accession_numbers
uniprot_id_re = r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"

Pivot = namedtuple("Pivot", "pdb_id chain_id")


def path_exist(file_path):
    """Check valid path

    Args:
        file_path (str): Path to file or directory to be checked

    Raises:
        argparse.ArgumentTypeError: If it is invalid
    """
    if not os.path.exists(file_path):
        raise ArgumentTypeError(f"Path '{file_path}' is not a valid file path.")

    if not os.access(file_path, os.W_OK):
        raise ArgumentTypeError(f"Path '{file_path}' is not writable.")

    return file_path


def valid_pivot(pdb_string):
    """Validation of user specified pivot. E.g. 1tqn:A.

    Args:
        pdb_string (pdb_string): User argument in the format pdb_id:chain_id

    Raises:
        ArgumentTypeError: On validation error

    Returns:
        namedtuple: Parsed pivot
    """
    splitted = pdb_string.split(":")

    if len(splitted) != 2:
        raise ArgumentTypeError(
            f"{pdb_string} PDB pivot format is 'PDB-id:label_asym_id'. E.g. '1tqn:A'"
        )

    pdb_id = valid_pdb(splitted[0])
    chain_id = splitted[1]

    return Pivot(pdb_id, chain_id)


def valid_uniprot_id(unp):
    """Check if uniprot can be valid (syntax only)

    Args:
        unp (str): UniProt identifier

    Raises:
        ArgumentTypeError: On validation error.

    Returns:
        str: UniProt identifier
    """
    if not re.fullmatch(uniprot_id_re, unp):
        raise ArgumentTypeError(
            f"{unp} is not a valid UniProt identifier. It should look like: 'P24941'"
        )

    return unp


def valid_pdb(pdb_id):
    """Check pdb entry is a valid pdb identifier (syntax only)

    Args:
        pdb_id (str): PDB identifier

    Raises:
        ArgumentTypeError: On validation error

    Returns:
        str: PDb identifer
    """
    if not re.fullmatch(pdb_id_re, pdb_id):
        raise ArgumentTypeError(
            f"{pdb_id} is not a valid PDB identifier. It should look like: '1tqn'"
        )

    return pdb_id


def positive_float(nmb):
    """Check if number is a positive float

    Args:
        nmb (str): float representation as string

    Raises:
        ArgumentTypeError: on validation error

    Returns:
        float: float number
    """
    try:
        number = float(nmb)
        if number <= 0:
            raise ArgumentTypeError("Value needs to be positive float.")

        return number
    except ValueError:
        raise ArgumentTypeError("Value needs to be positive float.")


def check_uniprot_in_pdb(unp, pdb, chain):
    """Check whether or not a PDB entry's chain contains defined
    UniProt id.

    Args:
        unp (str): Uniprot identifier
        pdb (str): PDB identifier
        chain (str): Chain identifier aka label_asym_id

    Raises:
        ArgumentTypeError: On validation error
    """
    response = requests.get(resources.URL_PDB_MAPPINGS % {"pdb": pdb})

    if response.status_code == 404:
        raise ArgumentTypeError(
            f"PDB-id '{pdb}' does not exist. Perhaps it never did or it is obsolete."
        )

    if response.status_code != 200:
        raise ArgumentTypeError(
            f"Check of PDB id and Uniprot could not be done. Response code: {response.status_code} "
        )

    data = response.json()[pdb]["UniProt"]

    try:
        chain_exist = any(x["chain_id"] == chain for x in data[unp]["mappings"])
        if not chain_exist:
            raise ArgumentTypeError(
                f"Selected chain '{chain}' is either not protein {unp} or is not in PDB-id: {pdb}."
            )

    except KeyError:
        raise ArgumentTypeError(
            f"UniProt-id: {unp} could not be found in the requested PDB-id: {pdb}"
        )
