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

        for v in ["E", None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, "aabb"), (1, "a"), (10, "aaabbbccce")]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), "length")


class TestMinLength(unittest.TestCase):
    def setUp(self):
        self.cls = MinLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ["E", None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, "aabb4"), (1, "a11"), (10, "aaabbbccce111")]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, "aab"), (4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), "min_length")


class TestMaxLength(unittest.TestCase):
    def setUp(self):
        self.cls = MaxLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance: Description = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ["E", None, 1.2, 0]:
            self.assertRaises(ValueError, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, "aabb"), (2, "a"), (2, ""), (4, "123")]:
            instance: Description = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, "aabb5"), (4, {}), (1, 1.2), (2, None)]:
            instance: Description = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(self.cls.get_name(), "max_length")


if __name__ == "__main__":
    unittest.main()
