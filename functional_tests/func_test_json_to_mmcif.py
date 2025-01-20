"""
func_test_json_to_mmcif.py

Description: This script is a functional test for the json_to_mmcif.py script.

"""
__author__ = 'Amudha Kumari Duraisamy'
__email__ = 'emdbhelp@ebi.ac.uk'
__date__ = '2025-01-07'

import unittest
import os
import sys
import tempfile
import json
import shutil
from unittest.mock import patch

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from json_to_mmcif import run

class TestJsonToMmcif(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.json_file = os.path.join(self.temp_dir, 'input.json')
        self.mmcif_file = os.path.join(self.temp_dir, 'input.cif')
        self.cif_file = os.path.join(self.temp_dir, 'input_existing.cif')
        self.mmcif_tools_path = os.path.join(os.path.dirname(__file__), '..', 'mmcif_tools')

        # Set the mmcif_tools path in the environment
        os.environ['MMCIF_TOOLS_PATH'] = self.mmcif_tools_path
        sys.path.insert(0, self.mmcif_tools_path)

        self.json_data = {
            "em_imaging": {
                "microscope_model": "TFS KRIOS",
                "mode": "BRIGHT FIELD"
            }
        }

    def tearDown(self):
        # Cleanup generated files and directories
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        if os.path.exists(self.mmcif_file):
            os.remove(self.mmcif_file)
        if os.path.exists(self.cif_file):
            os.remove(self.cif_file)
        shutil.rmtree(self.temp_dir)

    @patch('urllib.request.urlretrieve')
    def test_json_conversion(self, mock_urlretrieve):
        # Mock the download to bypass network requests
        mock_urlretrieve.return_value = None

        with open(self.json_file, 'w') as f:
            json.dump(self.json_data, f)

        # Simulate command-line arguments for json conversion
        sys.argv = ['json_to_mmcif.py', '-j', self.json_file, '-f', 'json', '-d', 'no', '-v', 'all']
        run()

        expected_mmcif_file = self.json_file.split(".")[0] + '.cif'
        self.assertTrue(os.path.exists(expected_mmcif_file))

        with open(expected_mmcif_file, 'r') as f:
            self.assertIn('_em_imaging.mode', f.read())

    @patch('urllib.request.urlretrieve')
    def test_data_merging(self, mock_urlretrieve):
        mock_urlretrieve.return_value = None

        with open(self.json_file, "w") as f:
            json.dump(self.json_data, f)

        with open(self.cif_file, "w") as f:
            f.write("_em_imaging.mode BRIGHT FIELD\n")

        # Simulate command-line arguments for merging
        sys.argv = ["json_to_mmcif.py", "-j", self.json_file, "-f", "json", "-c", self.cif_file, "-d", "no", "-v", "all"]
        run()

        self.assertTrue(os.path.exists(self.mmcif_file))

        with open(self.mmcif_file, "r") as f:
            self.assertIn("_em_imaging.mode", f.read())

    @patch('urllib.request.urlretrieve')
    def test_validation_logic(self, mock_urlretrieve):
        with open(self.json_file, 'w') as f:
            json.dump(self.json_data, f)

        # Simulate command-line arguments for dictionary download and validation (all mode)
        sys.argv = ['json_to_mmcif.py', '-j', self.json_file, '-f', 'json', '-d', 'yes', '-v', 'all']
        run()

if __name__ == '__main__':
    unittest.main()