from __future__ import annotations

import json
import unittest

from yaml.scanner import ScannerError

from src.env_should_be.utils import *


class TestEnvFileFunctions(unittest.TestCase):
    def test_load_env_file(self):
        # Test with a valid file
        file_path = 'test_file.env'
        with open(file_path, 'w') as file:
            file.write('TEST_KEY=TEST_VALUE')
        env_vars = load_env_file(file_path)
        self.assertEqual(env_vars, {'TEST_KEY': 'TEST_VALUE'})
        os.remove(file_path)

        # Test with an invalid file
        file_path = 'invalid_file.env'
        self.assertRaises(FileNotFoundError, load_env_file, file_path)

    def test_load_all_env_vars(self):
        env_vars = load_all_env_vars()
        self.assertIsInstance(env_vars, dict)

    def test_load_json_file(self):
        # Test with a valid file
        file_path = 'test_file.json'
        with open(file_path, 'w') as file:
            file.write('{"TEST_KEY": "TEST_VALUE"}')
        json_data = load_json_file(file_path)
        self.assertEqual(json_data, {'TEST_KEY': 'TEST_VALUE'})
        os.remove(file_path)

        # Test with an invalid file
        file_path = 'invalid_file.json'
        self.assertRaises(FileNotFoundError, load_json_file, file_path)


class TestGetErrorsForEnv(unittest.TestCase):
    test_file_path = 'description.json'

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def create_json_file(self, data, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

    def destroy_json_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_load_env_file(self):
        env = {'DB_USER': 'alfred_computer_man', 'DB_PORT': 5432}
        self.create_json_file(
            {
                'DB_USER': {'length': 19, 'required': True},
                'DB_PORT': {'option': [5432, 5431], 'constant': 5432, 'is_int': True},
            },
            self.test_file_path,
        )
        actual = get_errors_for(env, [self.test_file_path])
        self.assertEqual(actual, [])

        actual = get_errors_for(
            {**env, 'DB_PORT': 8000}, [self.test_file_path])
        self.assertTrue(actual.__len__(), 1)

        file_path = 'invalid_file.something'
        self.assertRaises(FileHasNoExtension, get_errors_for, env, [file_path])


class TestGetFileExtension(unittest.TestCase):
    def test_json_extension(self):
        file_path = 'example.json'
        result = get_file_extension(file_path)
        self.assertEqual(result, '.json')

    def test_yaml_extension(self):
        file_path = 'data.yaml'
        result = get_file_extension(file_path)
        self.assertEqual(result, '.yaml')

    def test_yml_extension(self):
        file_path = 'config.yml'
        result = get_file_extension(file_path)
        self.assertEqual(result, '.yml')

    def test_no_extension(self):
        file_path = 'myfile'
        result = get_file_extension(file_path)
        self.assertEqual(result, '')

    def test_mixed_case_extension(self):
        file_path = 'Docume,nt..JSON'
        result = get_file_extension(file_path)
        self.assertEqual(result, '.json')


class TestLoadYAMLFile(unittest.TestCase):
    test_file_path = 'afile.yaml'

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_valid_yaml_file(self):
        test_yaml_content = """
        key1: value1
        key2: value2
        """
        with open('test.yaml', 'w') as test_file:
            test_file.write(test_yaml_content)

        try:
            result = load_yaml_file('test.yaml')
            expected_data = safe_load(test_yaml_content)
            self.assertEqual(result, expected_data)
        finally:
            os.remove('test.yaml')  # Clean up the temporary test file

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError) as context:
            load_yaml_file('nonexistent.yaml')

        self.assertTrue(
            'nonexistent.yaml does not exist.' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
