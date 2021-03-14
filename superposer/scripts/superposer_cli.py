#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
from superposer.utils import validation, logger
from superposer.core.manager import Manager

log = logger.set_up_logger("superposer")


def create_parser():
    """
    Sets up parse the command line options.

    Returns:
         argparse.Namespace parser
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        type=validation.path_exist,
        help="Path to the output directory.",
    )
    parser.add_argument(
        "-u",
        "--uniprot-id",
        required=True,
        type=validation.valid_uniprot_id,
        help="Uniprot ID to be extracted.",
    )
    parser.add_argument(
        "-r",
        "--rmsd-threshold",
        required=False,
        type=validation.positive_float,
        default=3.0,
        help="Threshold for acceptance of superposition result [Å].",
    )
    parser.add_argument(
        "-t",
        "--threads",
        required=False,
        type=validation.positive_int,
        default=os.cpu_count() - 1,
        help="Number of threads to be used.",
    )
    parser.add_argument(
        "-p",
        "--pdb-pivot",
        required=True,
        type=validation.valid_pivot,
        help="PDB id and label_asym_id to be used as pivot for superimposition. Format 'PDB-id/chain_id'.",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    pdb = args.pdb_pivot.pdb_id
    chain = args.pdb_pivot.chain_id

    logger.log_settings(log, args)

    validation.check_uniprot_in_pdb(args.uniprot_id, pdb, chain)

    with Manager(args.pdb_pivot, args.output_dir) as m:
        m.process_protein(args.uniprot_id, args.rmsd_threshold, args.threads)


if __name__ == "__main__":
    main()
