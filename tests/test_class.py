from __future__ import annotations

import unittest

from src.env_should_be.description import *
from src.env_should_be.exception import *
from src.env_should_be.utils import *


class TestLength(unittest.TestCase):
    def setUp(self):
        self.cls = Length
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, 'aabb'), (1, 'a'), (10, 'aaabbbccce')]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))


class TestMinLength(unittest.TestCase):
    def setUp(self):
        self.cls = MinLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, 'aabb4'), (1, 'a11'), (10, 'aaabbbccce111')]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, 'aab'), (4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'min_length')


class TestMaxLength(unittest.TestCase):
    def setUp(self):
        self.cls = MaxLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, 'aabb'), (2, 'a'), (2, ''), (4, '123')]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, 'aabb5'), (4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'max_length')


class TestOption(unittest.TestCase):
    def setUp(self):
        self.cls = Option
        super().setUp()

    def test_is_valid(self):
        for v in [['d', 5], [2.2, False]]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0, [], {}]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (['dev', 'prod'], 'prod'),
            (['0.0.0.0', 'localhost'], '0.0.0.0'),
            ([5000, 6000], 5000),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (['dev', 'prod'], 'local'),
            (['0.0.0.0', 'localhost'], 'http://127.0.0.1'),
            ([5000, 6000], 7894),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'option')


class TestRegex(unittest.TestCase):
    def setUp(self):
        self.cls = Regex
        self.valid_regex = [
            r'(?i)(\W|^)(baloney|darn|drat|fooey|gosh\sdarnit|heck)(\W|$)',
            r'(\W|^)[\w.\-]{0,25}@(yahoo|hotmail|gmail)\.com(\W|$)',
            r'192\.168\.1\.\d{1,3}$',
        ]
        super().setUp()

    def test_is_valid(self):
        for v in self.valid_regex:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [False, {}, None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (self.valid_regex[0], 'baloney'),
            (self.valid_regex[1], 'wassef@yahoo.com'),
            (self.valid_regex[2], '192.168.1.255'),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (self.valid_regex[0], 'stock dips'),
            (self.valid_regex[1], 'wassef@company.tn'),
            (self.valid_regex[2], '192.168.1.5555'),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'regex')


class TestConstant(unittest.TestCase):
    def setUp(self):
        self.cls = Constant
        super().setUp()

    def test_is_valid(self):
        for v in [
            'True',
            'False',
            'localhost',
            'domain.com.org',
            {},
            '$#{}',
            5555,
            1.2,
            None,
            'null',
        ]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

    def test_does_pass(self):
        for expected, value in [
            (5, '5'),
            ('a string', 'a string'),
            (10.2, '10.2'),
            (True, 'True'),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, 'aab'), (4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'constant')


class TestIsInt(unittest.TestCase):
    def setUp(self):
        self.cls = IsInt
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance: Boolean = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0, 'True', 'False']:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(True, 21), (False, 'AbC')]:
            instance: Boolean = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(True, {}), (True, 1.2), (True, None), (False, False)]:
            instance: Boolean = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'is_int')


class TestIsFloat(unittest.TestCase):
    def setUp(self):
        self.cls = IsFloat
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance: Boolean = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0, 'True', 'False', {}, []]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(True, 2.2), (False, '21.2'), (False, 2)]:
            instance: Boolean = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(True, {}), (True, 1), (True, None), (True, False)]:
            instance: Boolean = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), 'is_float')


if __name__ == '__main__':
    unittest.main()
