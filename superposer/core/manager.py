import json
import os

import gemmi
from multiprocessing import Pool
import pandas as pd
from superposer.core import data_provider
from superposer.utils import logger


class Manager:
    """Superposer manager orchastrating computation."""

    def __init__(self, pivot, wd, log=None):
        self.pdb_id = pivot.pdb_id
        self.chain_id = pivot.chain_id
        self.wd = wd
        self.pivot_structure = None
        self.rmsds = []

        self.structures = os.path.join(wd, "structures")
        self.superposed = os.path.join(wd, "superposed")
        os.makedirs(self.structures, exist_ok=True)
        os.makedirs(self.superposed, exist_ok=True)

        self.log = log if log else logger.set_up_logger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Object destroyer, releases database connections, cleans data etc."""
        pass

    def _load_pivot(self):
        """Create internal representation for pivot molecule

        Raises:
            RuntimeError: If Pivot structure cannot be loaded
        """
        try:
            self.log.info("Downloading pivot")

            pivot_path = os.path.join(
                self.structures, f"{self.pdb_id}_{self.chain_id}.cif"
            )
            self.chain_id = data_provider.get_auth_chain_id(self.pdb_id, self.chain_id)
            data_provider.download_structure(self.pdb_id, self.chain_id, pivot_path)

            self.log.info("Loading pivot")

            # take chain from first model
            structure = gemmi.read_structure(pivot_path)
            protein = structure[0][self.chain_id]
            self.pivot_structure = protein.get_polymer()

        except Exception as e:
            self.log.error(f"Something went wrong with pivot loading. Reason: {str(e)}")
            raise RuntimeError()

    def process_protein(self, unp, rmsd):
        """Process uniprot protein:
            * Retrieve list of relevant PDB ids
            * Download their structures
            * Align them to pivot
            * Write out superposed form
            * write out statistics

        PDB entries with Calpha RMSD greater than threshold will be
        discarded

        Args:
            unp (str): UniProt id.
            rmsd (flouat): Threshold to for alignment acceptance
        """
        self.threshold = rmsd
        data = data_provider.list_pdbs_for_uniprot(unp)

        self.log.info("Downloading...")
        p = Pool(os.cpu_count())
        result = p.map(self.download_template, data)
        self.log.info("Completed.")

        self._load_pivot()

        # sadly gemmi does not support multiprocessing in python so far
        for chain_id, file_path in result:
            try:
                if not file_path:
                    continue

                self.superpose_structure(file_path, chain_id)
            except Exception as e:
                self.log.error(
                    f"Error occured while processing {file_path}. Reason: {str(e)}"
                )

        # write out some stats
        df = pd.DataFrame(self.rmsds, columns=["RMSD[A]"])
        self.log.info(df.describe())

        json_repr = os.path.join(self.wd, "statistics.json")
        with open(json_repr, "w") as fp:
            json.dump(self.rmsds, fp)

        self.log.info("We are done.")

    def download_template(self, item):
        """Download PDB chain given the pdb id and chain id

        Args:
            item (tuple[str,str]): PDB-id and label_asym_id

        Returns:
            tuple[str,str] = auth_asym_id, file path
        """
        try:
            pdb_id = item[0]
            chain_id = item[1]

            chain_id = data_provider.get_auth_chain_id(pdb_id, chain_id)
            file_path = os.path.join(self.structures, f"{pdb_id}_{chain_id}.cif")

            data_provider.download_structure(pdb_id, chain_id, file_path)
        except:
            return None, None
        return chain_id, file_path

    def write_out_superposed(self, structure, chain, transformation):
        """Write out superposed protein in mmCIF file.

        Args:
            structure (gemmi.Structure): gemmi structure
            chain (str): label_asym_id
            transformation (gemmi.Transformation): gemmi transforamtion
                object.
        """
        file_path = os.path.join(self.superposed, f"{structure.name}_{chain}.cif")

        to_translate = structure[0][chain]

        for residue in to_translate:
            for atom in residue:
                translated = transformation.mat.multiply(atom.pos) + transformation.vec
                atom.pos.x = translated.x
                atom.pos.y = translated.y
                atom.pos.z = translated.z

        structure.make_mmcif_document().write_file(file_path)

    def superpose_structure(self, file_path, chain_id):
        """Superpose PDB structure to pivot.

        Args:
            file_path (str): Path to the PDB entry.
            chain_id (str): Chain identifier to pick from PDB entry
        """
        structure = gemmi.read_structure(file_path)

        model = structure[0]
        target = model[chain_id].get_polymer()
        p_type = gemmi.PolymerType.PeptideL

        superposition = gemmi.calculate_superposition(
            self.pivot_structure, target, p_type, gemmi.SupSelect.CaP
        )

        if superposition.rmsd <= self.threshold:
            self.write_out_superposed(structure, chain_id, superposition.transform)
            self.log.info(
                f"Similarity with {structure.name}({chain_id}) is {superposition.rmsd:.3f}"
            )
        else:
            self.log.info(
                f"Rejected similarity with {structure.name}({chain_id}) {superposition.rmsd:.3f} >= threshold {self.threshold}."
            )

        self.rmsds.append(superposition.rmsd)
