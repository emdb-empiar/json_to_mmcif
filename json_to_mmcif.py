import json
import argparse
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxWriter import PdbxWriter

def parse_arguments():
    """Example usage (if no input cif file): python3.7 json_to_mmcif.py -f json -j test_data/TOMO_data.json
    or if there is an input cif file:
    python3.7 json_to_mmcif.py -f cif -j test_data/SPA_data.json -c test_data/input_mmcif.cif """
    parser = argparse.ArgumentParser(description="JSON to mmCIF")
    parser.add_argument("-j", "--input_json_file", required=True, help="input json file to convert or add to mmCIF")
    parser.add_argument("-c", "--input_cif_file", help="input mmCIF file to add the json information to")
    parser.add_argument("-f", "--input_format", choices=["json", "cif"], required=True,
                        help="json for converting directly from json, cif for adding the json file to the exisiting cif file")
    return parser.parse_args()

def json_to_dict(input_json_file):
    """Convert a JSON file to a Python dictionary"""
    try:
        with open(input_json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{input_json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{input_json_file}' is not a valid JSON file.")
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
    written = False
    mmcif_filename = input_json_file.split(".")[0] + '.cif'
    with open(mmcif_filename, "w") as cfile:
        pdbx_writer = PdbxWriter(cfile)
        pdbx_writer.write(data_list)
    written = True
    return written

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
    """Inserts data_list into the specified category_id within the container."""
    cat_obj = container.getObj(category_id)
    if cat_obj is None:
        return
    if all(isinstance(i, list) for i in data_list):
        list_values = [list(t) for t in zip(*data_list)]
        cat_obj.extend(list_values)
    else:
        cat_obj.append(data_list)

def convert_input_file(input_json_file, input_cif_file, input_format):
    container_dict = {}
    if input_format == "json":
        with open(input_json_file, 'r') as file:
            container_dict = json.load(file)

    if input_format == "cif":
        with open(input_json_file, 'r') as file:
            container_dict = json.load(file)
        cif_dict = mmcif_to_json(input_cif_file)
        for category, values in cif_dict.items():
            if category in container_dict:
                container_dict[category].update(values)
            else:
                container_dict[category] = values
    translate_json_to_cif(container_dict, input_json_file)

def translate_json_to_cif(container_dict, input_json_file):
    """Translates input json data into a CIF file."""
    cif_data_list = []
    container_id = input_json_file.split(".")[0]
    container = add_container(cif_data_list, container_id)
    for category_name, category_data in container_dict.items():
        category_list = list(category_data.keys())
        cif_values_list = list(category_data.values())
        add_category(container, category_name, category_list)
        insert_data(container, category_name, cif_values_list)
    return write_mmcif_file(cif_data_list, input_json_file)

def run():
    args = parse_arguments()
    convert_input_file(args.input_json_file, args.input_cif_file, args.input_format)

if __name__ == "__main__":
    run()
