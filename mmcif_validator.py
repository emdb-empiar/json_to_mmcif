#!/usr/bin/env python3
import os
import sys
import argparse
import urllib.request
from gemmi import cif

# URL and filename for the latest PDBx/mmCIF dictionary (v5.0 as of 2025)
DICT_URL = "https://mmcif.wwpdb.org/dictionaries/ascii/mmcif_pdbx_v50.dic"
DICT_FILE = "mmcif_pdbx_v50.dic"

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Validate an mmCIF file using Gemmi and the PDBx/mmCIF dictionary.")
    parser.add_argument("-c", "--cif", dest="cif_path", required=True,
                        help="Path to the input mmCIF file to validate")
    args = parser.parse_args()
    cif_path = args.cif_path

    # Ensure the input file exists
    if not os.path.isfile(cif_path):
        print(f"Error: file '{cif_path}' not found.")
        sys.exit(1)

    # Download the mmCIF dictionary if not already present
    if not os.path.isfile(DICT_FILE):
        try:
            print(f"Downloading mmCIF dictionary from {DICT_URL}...")
            urllib.request.urlretrieve(DICT_URL, DICT_FILE)
        except Exception as err:
            print(f"Error: failed to download dictionary ({err}).")
            sys.exit(1)

    # Load the dictionary and the mmCIF data file using Gemmi
    try:
        dict_doc = cif.read(DICT_FILE)       # Parse the dictionary CIF file into a Document
    except Exception as err:
        print(f"Error: failed to read dictionary file ({err}).")
        sys.exit(1)
    try:
        data_doc = cif.read(cif_path)        # Parse the input mmCIF file into a Document
    except Exception as err:
        print(f"Error: failed to read mmCIF file ({err}).")
        sys.exit(1)

    # Set up the Gemmi Ddl validator with output logger to stdout
    validator = cif.Ddl(logger=sys.stdout)
    validator.read_ddl(dict_doc)

    # Validate the mmCIF Document against the dictionary
    is_valid = validator.validate_cif(data_doc)

    # Print summary result
    if is_valid:
        print("Validation succeeded.")
    else:
        print("Validation failed.")
        # Detailed errors have already been printed to stdout by Gemmi's logger

if __name__ == "__main__":
    main()