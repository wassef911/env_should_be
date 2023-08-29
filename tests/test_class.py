from __future__ import annotations

import unittest

from src.env_should_be.description import *


class TestLength(unittest.TestCase):
    def setUp(self):
        self.cls = Length
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, 'aabb'), (1, 'a'), (10, 'aaabbbccce')]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'length')


class TestMinLength(unittest.TestCase):
    def setUp(self):
        self.cls = MinLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, 'aabb4'), (1, 'a11'), (10, 'aaabbbccce111')]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, 'aab'), (4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'min_length')


class TestMaxLength(unittest.TestCase):
    def setUp(self):
        self.cls = MaxLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, 'aabb'), (2, 'a'), (2, ''), (4, '123')]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, 'aabb5'), (4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'max_length')


class TestOption(unittest.TestCase):
    def setUp(self):
        self.cls = Option
        super().setUp()

    def test_is_valid(self):
        for v in [['d', 5], [2.2, False]]:
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0, [], {}]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (['dev', 'prod'], 'prod'),
            (['0.0.0.0', 'localhost'], '0.0.0.0'),
            ([5000, 6000], 5000),
        ]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (['dev', 'prod'], 'local'),
            (['0.0.0.0', 'localhost'], 'http://127.0.0.1'),
            ([5000, 6000], 7894),
        ]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'option')


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
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [False, {}, None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (self.valid_regex[0], 'baloney'),
            (self.valid_regex[1], 'wassef@yahoo.com'),
            (self.valid_regex[2], '192.168.1.255'),
        ]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (self.valid_regex[0], 'stock dips'),
            (self.valid_regex[1], 'wassef@company.tn'),
            (self.valid_regex[2], '192.168.1.5555'),
        ]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'regex')


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
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

    def test_does_pass(self):
        for expected, value in [
            (5, '5'),
            ('a string', 'a string'),
            (10.2, '10.2'),
            (True, 'True'),
        ]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, 'aab'), (4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'constant')


class TestIsInt(unittest.TestCase):
    def setUp(self):
        self.cls = IsInt
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance: Boolean = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0, 'True', 'False']:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(True, 21), (False, 'AbC')]:
            instance: Boolean = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(True, {}), (True, 1.2), (True, None), (False, False)]:
            instance: Boolean = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'is_int')


class TestIsFloat(unittest.TestCase):
    def setUp(self):
        self.cls = IsFloat
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance: Boolean = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ['E', None, 1.2, 0, 'True', 'False', {}, []]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(True, 2.2), (False, '21.2'), (False, 2)]:
            instance: Boolean = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(True, {}), (True, 1), (True, None), (True, False)]:
            instance: Boolean = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), 'is_float')


if __name__ == '__main__':
    unittest.main()
