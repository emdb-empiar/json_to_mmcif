"""
mmcif_validator.py

Description: This script can validate an mmCIF file using the latest mmCIF dictionary.

"""
__author__ = 'Amudha Kumari Duraisamy'
__email__ = 'emdbhelp@ebi.ac.uk'
__date__ = '2024-11-20'

import os
import argparse
import urllib.request
import gemmi

def parse_arguments():
    """
    Parses command-line arguments for mmCIF file validation.

    Example usage:
        python mmcif_validator.py -c test_data/TOMO_data.cif -d no

    Requirements:
        - Gemmi: A Python package for working with mmCIF files.
        To install:
            pip install gemmi

    Returns:
        argparse.Namespace: Parsed arguments with input CIF file, dictionary file, and output file paths.
    """
    parser = argparse.ArgumentParser(description="Validate a mmCIF file against a mmCIF dictionary.")
    parser.add_argument("-c", "--input_cif_file", required=True, help="Path to the input mmCIF file to validate.")
    parser.add_argument("-d", "--download_dict", choices=["yes", "no"], default="yes",
                        help="Download the latest mmCIF dictionary for validation (default: yes)")
    return parser.parse_args()

def mmcif_validation(cif_file, download_dict, output_file):
    """
    Validates an mmCIF file using the Gemmi Python API and saves the output to a file.

    Parameters:
        cif_file (str): Path to the mmCIF file.
        download_dict (str): Whether to download the dictionary file.
        output_file (str): Path to save the validation output.

    Returns:
        tuple: (bool, str)
            - bool: True if validation succeeded, False otherwise.
            - str: Message detailing validation results or errors.
    """
    dic_dir = "mmcif_tools"
    os.makedirs(dic_dir, exist_ok=True)
    dic_file = os.path.join(dic_dir, "mmcif_pdbx_v50.dic")

    if download_dict == "yes":
        urllib.request.urlretrieve("https://mmcif.wwpdb.org/dictionaries/ascii/mmcif_pdbx_v50.dic", dic_file)

    try:
        if not os.path.isfile(cif_file):
            return False, f"Error: Input CIF file '{cif_file}' does not exist."
        if not os.path.isfile(dic_file):
            return False, f"Error: Dictionary file '{dic_file}' does not exist."

        doc = gemmi.cif.read_file(cif_file)
        block = doc.sole_block()

        d = gemmi.cif.Dic()
        d.read_file(dic_file)

        validator = gemmi.cif.Validator(d)
        issues = validator.validate_block(block)

        if not issues:
            success_msg = f"Validation succeeded. No issues found. Results saved to {output_file}"
            with open(output_file, "w") as f:
                f.write(success_msg + "\n")
            print(success_msg)
            return True, success_msg
        else:
            with open(output_file, "w") as f:
                for issue in issues:
                    f.write(str(issue) + '\n')
            error_msg = f"Validation found issues. See {output_file} for details."
            print(error_msg)
            return False, error_msg

    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"

def validate_and_print(input_cif_file, download_dict, output_val_file):
    """
    A callable function for validation with direct input of arguments.

    Parameters:
        input_cif_file (str): Path to the input mmCIF file.
        cif_dict (str): Path to the mmCIF dictionary file.
        output_val_file (str): Path to save the validation output.
    """
    success, message = mmcif_validation(input_cif_file, download_dict, output_val_file)
    if not success:
        print(message)

def main():
    """
    Parses arguments, performs validation, and outputs results.
    """
    args = parse_arguments()
    output_val_file = args.input_cif_file.split(".")[0] + '_val.txt'
    validate_and_print(args.input_cif_file, args.download_dict, output_val_file)

if __name__ == "__main__":
    main()
