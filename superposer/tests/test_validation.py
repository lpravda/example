"""Set of tests for checking script parameter verification
"""

import pytest
from unittest import mock

from superposer.utils import validation
from argparse import ArgumentTypeError

valid_pdb_ids = ["1tqn", "4hhb"]
invalid_pdb_ids = ["hem", "1tqnn"]

valid_uniprot_id = ["P24941", "Q8N1B3"]
invalid_uniprot_id = ["1tqn", "124941"]

response = {
    "2vta": {
        "UniProt": {
            "P24941": {
                "mappings": [
                    {
                        "chain_id": "A",
                        "struct_asym_id": "A",
                    }
                ]
            }
        }
    }
}


@pytest.mark.parametrize("pdb_id", valid_pdb_ids)
def test_valid_pdb_id(pdb_id):
    result = validation.valid_pdb(pdb_id)

    assert result == pdb_id


@pytest.mark.parametrize("pdb_id", invalid_pdb_ids)
def test_invalid_pdb_id(pdb_id):
    with pytest.raises(ArgumentTypeError):
        result = validation.valid_pdb(pdb_id)


@pytest.mark.parametrize("unp_id", valid_uniprot_id)
def test_valid_unp_id(unp_id):
    result = validation.valid_uniprot_id(unp_id)

    assert result == unp_id


@pytest.mark.parametrize("unp_id", invalid_uniprot_id)
def test_invalid_unp_id(unp_id):
    with pytest.raises(ArgumentTypeError):
        result = validation.valid_uniprot_id(unp_id)


@mock.patch("requests.get")
def test_uniprot_in_pdb_failed(m):
    m.return_value.status_code = 500
    with pytest.raises(ArgumentTypeError):
        validation.check_uniprot_in_pdb("P24941", "2vta", "A")


@mock.patch("requests.get")
def test_uniprot_in_pdb_OK(m):
    m.return_value.status_code = 200
    m.return_value.json.return_value = response

    validation.check_uniprot_in_pdb("P24941", "2vta", "A")
