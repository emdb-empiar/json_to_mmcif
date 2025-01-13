"""
test_mmcif_Validator.py

Description: This script is a unit test for the mmcif_validator script.

"""
__author__ = 'Amudha Kumari Duraisamy'
__email__ = 'emdbhelp@ebi.ac.uk'
__date__ = '2025-01-13'

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the parent directory to the system path to import the script
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mmcif_validator import *

class TestMmcifValidator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cif_file = os.path.join(self.temp_dir, 'test.cif')
        self.output_file = os.path.join(self.temp_dir, 'output.txt')
        self.mmcif_tools_path = os.path.join(os.path.dirname(__file__), '..', 'mmcif_tools')
        os.makedirs(self.mmcif_tools_path, exist_ok=True)

        # Set environment variables
        os.environ['MMCIF_TOOLS_PATH'] = self.mmcif_tools_path
        sys.path.insert(0, self.mmcif_tools_path)

        # Create a dummy CIF file
        with open(self.cif_file, 'w') as f:
            f.write('')

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)

    def test_parse_argument(self):
        test_args = [
            "mmcif_validator.py",
            "-c", self.cif_file,
            "-d", "no"
        ]
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.input_cif_file, self.cif_file)
            self.assertEqual(args.download_dict, "no")

    @patch('subprocess.run')
    @patch('urllib.request.urlretrieve')
    def test_mmcif_validation_success(self, mock_urlretrieve, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr='')
        mock_urlretrieve.return_value = ('', '')

        result = mmcif_validation(self.cif_file, 'yes', self.output_file)
        self.assertTrue(result)


    @patch('subprocess.run')
    @patch('os.path.isfile', side_effect=lambda x: True if 'mmcif_pdbx_v50.dic' in x or 'test.cif' in x else False)
    def test_mmcif_validation_failure(self, mock_isfile, mock_run):
        # Simulate a subprocess error
        mock_run.return_value = MagicMock(returncode=1, stderr='Validation failed due to an error.')
        result = mmcif_validation(self.cif_file, 'no', self.output_file)
        self.assertFalse(result)

    @patch('urllib.request.urlretrieve')
    def test_mmcif_validation_missing_dict(self, mock_urlretrieve):
        mock_urlretrieve.return_value = ('', '')
        # Simulate missing dictionary file
        dic_file = os.path.join(self.mmcif_tools_path, 'mmcif_pdbx_v50.dic')
        if os.path.exists(dic_file):
            os.remove(dic_file)

        result = mmcif_validation(self.cif_file, 'no', self.output_file)
        self.assertFalse(result[0])
        self.assertIn("Dictionary file", result[1])

    @patch('subprocess.run')
    @patch('os.path.isfile', side_effect=lambda x: True if 'mmcif_pdbx_v50.dic' in x or 'test.cif' in x else False)
    def test_unexpected_exception(self, mock_isfile, mock_run):
        # Simulate an unexpected exception
        mock_run.side_effect = Exception('Unexpected error occurred during validation.')
        result = mmcif_validation(self.cif_file, 'no', self.output_file)
        is_valid, error_message = result
        self.assertFalse(is_valid)
        self.assertIn("Unexpected error occurred", error_message)

    @patch('mmcif_validator.mmcif_validation')
    def test_validate_and_print(self, mock_validation):
        mock_validation.return_value = (True, "Validation succeeded")

        # Call validate_and_print and verify the mock was called
        validate_and_print(self.cif_file, "no", self.output_file)
        mock_validation.assert_called_once_with(self.cif_file, "no", self.output_file)

if __name__ == '__main__':
    unittest.main()

