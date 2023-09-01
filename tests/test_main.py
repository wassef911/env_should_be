from __future__ import annotations

import unittest

from src.env_should_be.utils import is_valid_env


class TestIsValidEnv(unittest.TestCase):
    def test_valid_env(self):
        expected_env = {
            'DB_USER': {'length': 6, 'regex': '^[a-zA-Z0-9]+$', 'required': True},
            'DB_PASSWORD': {
                'length': 11,
                'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})',
                'required': True,
            },
            'DB_HOST': {'option': ['localhost', '127.0.0.1'], 'required': True},
            'DB_PORT': {'length': 4, 'regex': '^[0-9]+$'},
            'APP_ENV': {'option': ['dev', 'prod'], 'required': True},
        }

        actual_env = {
            'DB_USER': 'myuser',
            'DB_PASSWORD': 'MyPassw0rd!',
            'DB_HOST': 'localhost',
            'DB_PORT': '3306',
            'APP_ENV': 'dev',
        }
        self.assertEqual(is_valid_env(expected_env, actual_env), True)

    def test_invalid_env(self):
        expected_env = {
            'DB_USER': {'length': 8, 'regex': '^[a-zA-Z0-9]+$', 'required': True},
            'DB_PASSWORD': {
                'length': 12,
                'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})',
                'required': True,
            },
            'DB_HOST': {'option': ['localhost', '127.0.0.1'], 'required': True},
            'DB_PORT': {'length': 4, 'regex': '^[0-9]+$'},
            'APP_ENV': {'option': ['dev', 'prod'], 'required': True},
        }

        actual_env = {
            'DB_USER': 'myuser',
            'DB_PASSWORD': 'MyPassw0rd',
            'DB_HOST': '127.0.0.2',
            'DB_PORT': '3306',
            'APP_ENV': 'testing',
        }
        self.assertEqual(
            is_valid_env(expected_env, actual_env),
            [
                ['APP_ENV', ['option']],
                ['DB_HOST', ['option']],
                ['DB_PASSWORD', ['length', 'regex']],
                ['DB_USER', ['length']],
            ],
        )

    def test_required_arg_for_env(self):
        expected_env = {
            'DB_USER': {
                'length': 6,
            },
            'DB_HOST': {
                'option': ['localhost'],
            },
            'APP_NAME': {
                'length': 6,
                'required': False,  # meaning it will only be validated if it exists
            },
            'SENT_ARTIFACT_EVERY_N_DAYS': {'is_int': True, 'is_float': False},
            'MAX_CURRENCY': {'is_int': False, 'is_float': True},
        }

        actual_env = {
            'DB_USER': 'myuser',
            'DB_HOST': 'localhost',
            'SENT_ARTIFACT_EVERY_N_DAYS': 5,
            'MAX_CURRENCY': 2.5,
        }
        self.assertEqual(
            is_valid_env(expected_env, actual_env),
            True,
        )

        self.assertEqual(
            is_valid_env(expected_env, {'APP_NAME': 'A', **actual_env}),
            [
                ['APP_NAME', ['length']],
            ],
        )

        self.assertEqual(
            is_valid_env(expected_env, {'APP_NAME': 2.5, **actual_env}),
            [
                ['APP_NAME', ['length']],
            ],
        )
        self.assertEqual(
            is_valid_env(expected_env, {'APP_NAME': 'AWERTY', **actual_env}),
            True,
        )


if __name__ == '__main__':
    unittest.main()
