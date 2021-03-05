"""Web resources consumed by the app.
"""

URL_BEST_STRUCTURE = "https://www.ebi.ac.uk/pdbe/graph-api/mappings/best_structures/%(unp)s"
"""Retrieves list of PDB structures given UniProt identifier.
"""

URL_MOLECULES_IN_ENTRY = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/%(pdb)s"
"""
"""

URL_CHAIN_STRUCTURE_DOWNLOAD = "https://www.ebi.ac.uk/pdbe/model-server/v1/%(pdb)s/atoms?auth_asym_id=%(chain)s&copy_all_categories=false"
"""ModelServer query to retrieve selected chain only
"""


URL_PDB_MAPPINGS = "https://www.ebi.ac.uk/pdbe/api/mappings/%(pdb)s"
"""Chains mapping within a PDB entry
"""