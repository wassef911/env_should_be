import unittest

from src.env_should_be.utils import *

class TestEnvFileFunctions(unittest.TestCase):
    def test_load_env_file(self):
        # Test with a valid file
        file_path = "test_file.env"
        with open(file_path, "w") as file:
            file.write("TEST_KEY=TEST_VALUE")
        env_vars = load_env_file(file_path)
        self.assertEqual(env_vars, {"TEST_KEY": "TEST_VALUE"})
        os.remove(file_path)

        # Test with an invalid file
        file_path = "invalid_file.env"
        self.assertRaises(FileNotFoundError, load_env_file, file_path)

    def test_load_all_env_vars(self):
        env_vars = load_all_env_vars()
        self.assertIsInstance(env_vars, dict)

    def test_load_json_description(self):
        # Test with a valid file
        file_path = "test_file.json"
        with open(file_path, "w") as file:
            file.write('{"TEST_KEY": "TEST_VALUE"}')
        json_data = load_json_description(file_path)
        self.assertEqual(json_data, {"TEST_KEY": "TEST_VALUE"})
        os.remove(file_path)

        # Test with an invalid file
        file_path = "invalid_file.json"
        self.assertRaises(FileNotFoundError, load_json_description, file_path)
