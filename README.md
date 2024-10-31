# json_to_mmcif
Converting JSON to mmCIF, as well as adding to and modifying an mmCIF file using a JSON file.

Conversion to mmCIF metadata file:
The standalone Python script (json_to_mmcif.py) provides two functionalities: it either converts a JSON file into the mmCIF format, or it appends data from a JSON file to an already existing mmCIF file. This flexibility allows for both the creation of new mmCIF files from JSON data and the extension or modification of existing mmCIF files by incorporating additional data.

Key Features:
1. JSON to mmCIF conversion: The script reads structured data from a JSON file and generates a new mmCIF file formatted according to the standard used in macromolecular data storage.
2. Appending Data to an existing mmCIF file: If you already have an mmCIF file, the script allows you to append new data from a JSON file to this existing file, preserving the original data while augmenting it with new entries.
   
Usage:
To use the script, you need to specify whether you are converting a JSON file to a new mmCIF file or appending data to an existing mmCIF file with -f parameter stating either ‘json’ or ‘cif’ respectively. Need to mention the input JSON file path with -j parameter and -c parameter is used when appending or modifying the existing file stating the mmCIF file path. 
Example command for converting JSON to mmCIF:
python json_to_mmcif.py -f json -j input_data.json

Or example command for adding JSON to an existing mmCIF information:
Python json_to_mmcif.py -f cif -j input_data.json -c input_cif.cif
