# json_to_mmcif

json_to_mmcif(file_format, json_path, cif_path=None)

Convert or append/modify an mmCIF file using data from a JSON file.

Parameters:

   file_format : {'json', 'cif'}
        Specify the operation mode. Choose 'json' to create a new mmCIF file from a JSON file. Choose 'cif' to append or modify an existing mmCIF file with data from a JSON file.
        
   json_path : str
        The file path to the JSON file containing structured data for conversion or modification.
        
   cif_path : str, optional
        The file path to an existing mmCIF file to which JSON data will be appended. Required only if 'file_format' is set to 'cif'.

Output:
 A new or modified mmCIF file (filename same as JSON) will be generated as a result of the specified operation.

Description:

The 'json_to_mmcif.py' script provides two primary functionalities:

- JSON to mmCIF Conversion: Converts a JSON file into the macromolecular Crystallographic Information File (mmCIF) format, creating a new mmCIF file based on JSON data.
  
- Appending or modifying Data to an Existing mmCIF File: If you have an existing mmCIF file, you can append new data from a JSON file, thereby extending or modifying the values of items in the mmCIF file based on the JSON data.

Usage Examples:

To convert a JSON file to a new mmCIF file:
python json_to_mmcif.py -f json -j input_data.json

To append/modify an existing mmCIF file by a JSON file:
python json_to_mmcif.py -f cif -j input_data.json -c input_cif.cif




