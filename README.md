# JSON to mmCIF Converter and Validator

This script facilitates the conversion of JSON data to mmCIF format, appends JSON data to existing mmCIF files, and validates the resulting mmCIF files using the Gemmi tool and an mmCIF dictionary.

Features:
- Convert JSON data to mmCIF format.
- Append JSON data to existing mmCIF files.
- Validate mmCIF files using the latest mmCIF dictionary.
- Save converted mmCIF files and detailed validation reports.

Requirements:
1. Python 3 or higher
2. Required Libraries: pip install mmcif and pip install gemmi
3. Network access (if downloading the mmCIF dictionary).

Installation:
Clone this repository:
git clone https://github.com/your-username/json-to-mmcif.git
cd json-to-mmcif
Install dependencies:pip install mmcif and pip install gemmi

Usage:
python json_to_mmcif.py -j <input_json_file> -f <input_format> [-c <input_cif_file>] [-d <download_dict>] [-v <validate_option>]

Arguments:
    -j, --input_json_file (required): Path to the input JSON file.
    -f, --input_format (required): Format for processing:
        json: Convert directly from JSON to mmCIF.
        cif: Append JSON data to an existing mmCIF file.
    -c, --input_cif_file (optional): Path to the input mmCIF file (required if using cif format).
    -d, --download_dict (optional): Download the latest mmCIF dictionary for validation. Options:
        yes (default): Download and use the latest dictionary.
        no: Use an existing dictionary file in the mmcif_tools/ directory.
    -v, --validate (optional): Validation options:
        all (default): Convert and validate the mmCIF file.
        only: Validate an existing mmCIF file.

Example Usages:
Convert JSON to mmCIF and validate:
python json_to_mmcif.py -j test_data/data.json -f json -d yes -v all

Append JSON to an existing mmCIF file and validate:
python json_to_mmcif.py -j test_data/data.json -f cif -c test_data/input_mmcif.cif -d yes -v all

Only validate an mmCIF file:
python json_to_mmcif.py -j test_data/data.json -f cif -c test_data/input_mmcif.cif -d no -v only

Output:
    Converted mmCIF File: Saved in the same directory as the input JSON file, named <input_json_file>.cif.
    Validation Report: Saved in the same directory as the input JSON file, named <input_json_file>_val.txt.

Error Handling:
   Provides error messages for missing input files, dictionary download failures, or JSON decoding issues.
   Ensures proper merging of JSON data into mmCIF files without overwriting unrelated data.



# mmCIF Validator

This script if executed as standalone will validates an mmCIF file against the mmCIF dictionary using the Gemmi tool. It ensures the structural data in mmCIF format adheres to the specified dictionary standards. This script is also used along with json_to_mmcif.py for validating the converted/modified cif file.

Features:
- Validate mmCIF files for structural compliance.
- Automatically download the latest mmCIF dictionary if needed.
- Save detailed validation results to a file.

Requirements:
1. Python 3 or higher
2. Gemmi library (Install using 'pip install gemmi')
3. Network access (if downloading the mmCIF dictionary)

Installation:
1. Clone this repository:
   git clone https://github.com/your-username/mmcif-validator.git
   cd mmcif-validator
   Install dependencies: pip install gemmi

Usage:
python mmcif_validator.py -c <path_to_mmCIF_file> -d <download_dictionary_option>

Arguments:
   -c, --input_cif_file (required): Path to the input mmCIF file to validate.
   -d, --download_dict (optional): Download the latest mmCIF dictionary for validation. Options:
        yes (default): Download and use the latest dictionary.
        no: Use an existing dictionary file in the mmcif_tools/ directory.

Example:
Validate an mmCIF file and download the dictionary:
python mmcif_validator.py -c test_data/TOMO_data.cif -d yes

Output:
 A validation report will be saved in the same directory as the input mmCIF file, with the filename <input_file>_val.txt.

Error Handling:
   Ensures input files exist.
   Provides meaningful error messages for missing files, dictionary download issues, or Gemmi command failures.



