"""
json_to_mmcif.py

Description: This script convert or append/modify an mmCIF file using data from a given JSON file.
Can validate mmCIF files using the latest mmCIF dictionary, either after conversion or as a standalone
validation tool for any input mmCIF file.

"""
__author__ = 'Amudha Kumari Duraisamy'
__email__ = 'emdbhelp@ebi.ac.uk'
__date__ = '2024-10-15'

import json
import argparse
import urllib.request
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxWriter import PdbxWriter
from mmcif_validator import validate_and_print

def parse_arguments():
    """Example usage (if no input cif file): python json_to_mmcif.py -f json -j test_data/TOMO_data.json -d no -v all
    or if there is an input cif file:
    python json_to_mmcif.py -f cif -j test_data/SPA_data.json -c test_data/input_mmcif.cif -v only"""
    parser = argparse.ArgumentParser(description="JSON to mmCIF")
    parser.add_argument("-j", "--input_json_file", required=True, help="input JSON file to convert or add to mmCIF")
    parser.add_argument("-c", "--input_cif_file", help="input mmCIF file to add the JSON information to")
    parser.add_argument("-f", "--input_format", choices=["json", "cif"], required=True,
                        help="json for converting directly from JSON, cif for adding the JSON file to the existing CIF file")
    parser.add_argument("-d", "--download_dict", choices=["yes", "no"], default="yes",
                        help="Download the latest mmCIF dictionary for validation (default: yes)")
    parser.add_argument("-v", "--validate", default="all", choices=["all", "only"],
                        help="Convert and validate (with option all) or Only validate the mmCIF file (with option only)(default: all)")
    return parser.parse_args()


def json_to_dict(input_json_file):
    """Convert a JSON file to a Python dictionary"""
    try:
        with open(input_json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{input_json_file}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: File '{input_json_file}' is not a valid JSON file.")
        return {}
    return data


def mmcif_to_json(input_cif_file):
    """Converts an mmCIF file to a JSON format."""
    json_data_dict = {}
    with open(input_cif_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('_'):
                key, value = line.split(maxsplit=1)
                if '.' in key:
                    category, sub_key = key[1:].split('.', 1)
                    if category not in json_data_dict:
                        json_data_dict[category] = {}
                    json_data_dict[category][sub_key] = value
    return json_data_dict


def write_mmcif_file(data_list, input_json_file):
    """Writes CIF data to a new file."""
    mmcif_filename = input_json_file.split(".")[0] + '.cif'
    with open(mmcif_filename, "w") as cfile:
        pdbx_writer = PdbxWriter(cfile)
        pdbx_writer.write(data_list)
    return True


def add_container(data_list, container_id):
    """Adds a container with the specified container_id to the data_list."""
    container = DataContainer(container_id)
    data_list.append(container)
    return container


def add_category(container, category_id, items):
    """Adds a category with the specified category_id and items to the container."""
    category = DataCategory(category_id)
    for item in items:
        category.appendAttribute(item)
    container.append(category)


def insert_data(container, category_id, data_list):
    """ Insert or update data in the given category within the DataContainer."""
    # Check if the category exists in the container
    category = container.getObj(category_id)

    if category is None:
        category = DataCategory(category_id)
        container.append(category)

    for idx, value_list in enumerate(data_list):
        if not isinstance(value_list, list):
            value_list = [value_list]

        # Get or generate attribute name
        attr_name = (list(container.getObj(category_id).getAttributeList())[idx]
                     if idx < len(container.getObj(category_id).getAttributeList())
                     else f"attribute_{idx}")

        if not category.hasAttribute(attr_name):
            category.appendAttribute(attr_name)

        # Ensure there is at least one row
        if category.getRowCount() == 0:
            category.append([None] * len(category.getAttributeList()))

        # Update the value of the attribute
        category.setValue(str(value_list[0]), attr_name, 0)


def convert_input_file(input_json_file, input_cif_file, input_format):
    container_dict = {}
    if input_format == "json":
        container_dict = json_to_dict(input_json_file)

    if input_format == "cif":
        container_dict = json_to_dict(input_json_file)
        cif_dict = mmcif_to_json(input_cif_file)

        # Merge JSON data into CIF data, overwriting existing keys with JSON values
        for category, values in container_dict.items():
            if category in cif_dict:
                # Overwrite only keys in CIF that exist in JSON
                for key, val in values.items():
                    cif_dict[category][key] = val
            else:
                cif_dict[category] = values
        container_dict = cif_dict

    translate_json_to_cif(container_dict, input_json_file)

    return container_dict

def translate_json_to_cif(container_dict, input_json_file):
    """Translates input JSON data into a CIF file."""
    cif_data_list = []
    container_id = input_json_file.split(".")[0]
    container = add_container(cif_data_list, container_id)
    for category_name, category_data in container_dict.items():
        category_list = list(category_data.keys())
        cif_values_list = list(category_data.values())
        add_category(container, category_name, category_list)
        insert_data(container, category_name, cif_values_list)
    return write_mmcif_file(cif_data_list, input_json_file)

def download_and_validate(input_json_file, input_cif_file, download_dict, validate):
    mmcif_filename = input_json_file.split(".")[0] + '.cif'
    val_filename = input_json_file.split(".")[0] + '_val.txt'
    dic_file = "mmcif_tools/mmcif_pdbx_v50.dic"
    if download_dict == "yes":
        urllib.request.urlretrieve("https://mmcif.wwpdb.org/dictionaries/ascii/mmcif_pdbx_v50.dic", dic_file)
    if validate == "all":
        validate_and_print(mmcif_filename, dic_file, val_filename)
    elif validate == "only":
        if not input_cif_file:
            print("Error: Please provide the input mmCIF file with -c argument.")
        validate_and_print(input_cif_file, dic_file, val_filename)
    return True


def run():
    args = parse_arguments()
    convert_input_file(args.input_json_file, args.input_cif_file, args.input_format)
    download_and_validate(args.input_json_file, args.input_cif_file, args.download_dict, args.validate)

if __name__ == "__main__":
    run()
