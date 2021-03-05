import logging

import requests
from superposer.core import resources
from superposer.utils.logger import set_up_logger

logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = set_up_logger()


def get_auth_chain_id(pdb_id, chain_id):
    auth_asym_id = ""

    url = resources.URL_MOLECULES_IN_ENTRY % {"pdb": pdb_id}
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Could not retrieve chain mapping for {pdb_id}")

    data = response.json()

    for x in data[pdb_id]:
        try:
            index = x["in_struct_asyms"].index(chain_id)
            auth_asym_id = x["in_chains"][index]
            break
        except ValueError:
            # it is OK if chain is not found in an entry
            pass

    if not auth_asym_id:
        raise ValueError(f'label_asym_id {chain_id} could not be found in {pdb_id} PDB entry.')

    return auth_asym_id


def list_pdbs_for_uniprot(unp):
    """Retireve a list of PDB entries where the uniprot can be found.

    Args:
        unp (str): Uniprot identifier

    Raises:
        Exception: If list of PDB entries could not be obtained.

    Returns:
        dict[str,list[str]]: Data structure with pdb-id:label_asym_id
        mappings.
    """
    result = {}
    url = resources.URL_BEST_STRUCTURE % {"unp": unp}
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Could not retrieve list of PDB entries for {unp}")

    data = response.json()
    result = [(x["pdb_id"], x["chain_id"]) for x in data[unp]]

    logger.info(
        f"There are {len(data[unp])} chains to be downloaded and processed."
    )

    return result


def download_structure(pdb_id, chain_id, file_path):
    """Download PDB structure.

    Args:
        pdb_id (str): PDB identifier.
        chain_id (str): label_asym_id identifier.
        file_path (str): Path where the structure should be saved.

    Raises:
        ValueError: If an entry could not be downloaded
    """
    url = resources.URL_CHAIN_STRUCTURE_DOWNLOAD % {"pdb": pdb_id, "chain": chain_id}
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Could not download structure for entry: {pdb_id}")

    with open(file_path, "wb") as fp:
        fp.write(response.content)
