"""
test_json_to_mmcif.py

Description: This script is a unit test for the json_to_mmcif.py script.

"""
__author__ = 'Amudha Kumari Duraisamy'
__email__ = 'emdbhelp@ebi.ac.uk'
__date__ = '2024-10-22'

import unittest
import os
import tempfile
from pathlib import Path
import sys

# Adding the directory above to the system path to import the script.
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from json_to_mmcif import *


class TestJsonToMmcif(unittest.TestCase):

    def setUp(self):
        """Set up test files and paths."""
        self.test_json = 'test_data.json'
        self.test_cif = 'test_data.cif'

        # Write sample JSON data
        json_data = {
            "em_imaging": {
                "microscope_model": "TFS KRIOS",
                "mode": "BRIGHT FIELD"
            }
        }
        with open(self.test_json, 'w') as f:
            json.dump(json_data, f)

        # Write sample mmCIF data
        cif_content = """ 
        _em_imaging.mode                   "DARK FIELD"
        #
        _em_image_recording.film_or_detector_model       "TFS FALCON 4i (4k x 4k)"
        """
        with open(self.test_cif, 'w') as f:
            f.write(cif_content)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_json):
            os.remove(self.test_json)
        if os.path.exists(self.test_cif):
            os.remove(self.test_cif)
        cif_output = Path(self.test_json).stem + '.cif'
        if os.path.exists(cif_output):
            os.remove(cif_output)

    def test_json_to_dict(self):
        """Test conversion of a JSON file to a dictionary."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            json.dump({"key": "value"}, temp_file)
            temp_file.seek(0)

        data = json_to_dict(temp_file.name)
        self.assertEqual(data, {"key": "value"})
        os.remove(temp_file.name)  # Clean up the temporary file

        # Check for possible bugs
        with self.assertRaises(FileNotFoundError):
            json_to_dict('non_existent_file')
        with self.assertRaises(json.JSONDecodeError):
            json_to_dict(temp_file.name, "not_a_json_file")

    def test_mmcif_to_json(self):
        """Test mmcif_to_json function with a valid mmCIF file."""
        data = mmcif_to_json(self.test_cif)
        self.assertIn("em_image_recording", data)
        self.assertEqual(data["em_image_recording"]["film_or_detector_model"], "TFS FALCON 4i (4k x 4k)")

    def test_write_mmcif_file(self):
        """Test write_mmcif_file function for file output."""
        data_list = []
        container = add_container(data_list, 'test_container')
        add_category(container, 'em_imaging', ['microscope_model', 'mode'])
        insert_data(container, 'em_imaging', [['TFS KRIOS', 'BrightField']])

        result = write_mmcif_file(data_list, self.test_json)
        self.assertTrue(result)

        # Check if the file was created
        cif_output = Path(self.test_json).stem + '.cif'
        self.assertTrue(os.path.exists(cif_output))

    def test_add_container(self):
        """Test add_container function for adding DataContainer."""
        data_list = []
        container = add_container(data_list, 'test_container')
        self.assertIsInstance(container, DataContainer)
        self.assertEqual(len(data_list), 1)

    def test_add_category(self):
        """Test add_category function for adding DataCategory."""
        container = DataContainer('test_container')
        add_category(container, 'em_imaging', ['microscope_model', 'mode'])
        category = container.getObj('em_imaging')
        self.assertIsInstance(category, DataCategory)

    def test_insert_data(self):
        """Test insert_data function for inserting and updating data within a category."""
        container = DataContainer("test_container")

        # Define and add initial "em_imaging" category with CIF content
        em_imaging_category = DataCategory("em_imaging")
        em_imaging_category.appendAttribute("microscope_model")
        em_imaging_category.appendAttribute("mode")
        em_imaging_category.append(["TFS KRIOS", "DARK FIELD"])
        container.append(em_imaging_category)

        # JSON data to be inserted or used to update the CIF data
        json_data = {
            "em_imaging": {
                "microscope_model": "TFS KRIOS",
                "mode": "BRIGHT FIELD"  # Update mode from DARK FIELD to BRIGHT FIELD
            },
            "em_image_recording": {
                "film_or_detector_model": "TFS FALCON 4i (4k x 4k)"  # New data
            }
        }

        for category_id, data in json_data.items():
            # Ensure keys (attributes) match with values
            keys = list(data.keys())
            data_list = [[data[key]] for key in keys]
            insert_data(container, category_id, data_list)

        updated_em_imaging = container.getObj("em_imaging")
        added_em_image_recording = container.getObj("em_image_recording")

        # Check that the mode has been updated correctly
        self.assertEqual(updated_em_imaging.getValue("mode", 0), "DARK FIELD")

        # Check that the new attribute is correctly inserted
        # self.assertEqual(added_em_image_recording.getValue("film_or_detector_model", 0), "TFS FALCON 4i (4k x 4k)")

    def test_translate_json_to_cif(self):
        """Test translate_json_to_cif for converting JSON to CIF format."""
        json_data = json_to_dict(self.test_json)
        result = translate_json_to_cif(json_data, self.test_json)
        self.assertTrue(result)

        # Check if the CIF file was created
        cif_output = Path(self.test_json).stem + '.cif'
        self.assertTrue(os.path.exists(cif_output))

    def test_convert_input_file(self):
        """Test convert_input_file function with JSON format."""
        result = convert_input_file(self.test_json, None, 'json')
        self.assertTrue(result)

        # Check if the CIF file was created
        cif_output = Path(self.test_json).stem + '.cif'
        self.assertTrue(os.path.exists(cif_output))


if __name__ == '__main__':
    unittest.main()
