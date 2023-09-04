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

        for v in ["E", None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (4, "aabb"),
            (1, "a"),
            (10, "aaabbbccce"),
            (4, "5000"),
            (4, "50,0"),
        ]:
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

        for v in ["E", None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, "aabb4"), (1, "a11"), (10, "aaabbbccce111")]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, "aab"), (4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "min_length")


class TestMaxLength(unittest.TestCase):
    def setUp(self):
        self.cls = MaxLength
        super().setUp()

    def test_is_valid(self):
        for v in [4, 5, 2, 6, 8]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ["E", None, 1.2, 0]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(4, "aabb"), (2, "a"), (2, ""), (4, "123")]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, "aabb5"), (4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "max_length")


class TestOption(unittest.TestCase):
    def setUp(self):
        self.cls = Option
        super().setUp()

    def test_is_valid(self):
        for v in [["d", 5], [2.2, False]]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ["E", None, 1.2, 0, [], {}]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (["dev", "prod"], "prod"),
            (["0.0.0.0", "localhost"], "0.0.0.0"),
            ([5000, 6000], 5000),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (["dev", "prod"], "local"),
            (["0.0.0.0", "localhost"], "http://127.0.0.1"),
            ([5000, 6000], 7894),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "option")


class TestRegex(unittest.TestCase):
    def setUp(self):
        self.cls = Regex
        self.valid_regex = [
            r"(?i)(\W|^)(baloney|darn|drat|fooey|gosh\sdarnit|heck)(\W|$)",
            r"(\W|^)[\w.\-]{0,25}@(yahoo|hotmail|gmail)\.com(\W|$)",
            r"192\.168\.1\.\d{1,3}$",
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
            (self.valid_regex[0], "baloney"),
            (self.valid_regex[1], "wassef@yahoo.com"),
            (self.valid_regex[2], "192.168.1.255"),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (self.valid_regex[0], "stock dips"),
            (self.valid_regex[1], "wassef@company.tn"),
            (self.valid_regex[2], "192.168.1.5555"),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "regex")


class TestConstant(unittest.TestCase):
    def setUp(self):
        self.cls = Constant
        super().setUp()

    def test_is_valid(self):
        for v in [
            "True",
            "False",
            "localhost",
            "domain.com.org",
            {},
            "$#{}",
            5555,
            1.2,
            None,
            "null",
        ]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

    def test_does_pass(self):
        for expected, value in [
            (5, "5"),
            ("a string", "a string"),
            (10.2, "10.2"),
            (True, "True"),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(4, "aab"), (4, {}), (1, 1.2), (2, None)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "constant")


class TestIsInt(unittest.TestCase):
    def setUp(self):
        self.cls = IsInt
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ["E", None, 1.2, 0, "True", "False"]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (True, 21),
            (False, "AbC"),
            (True, 4555),
            (False, "5444"),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [(True, {}), (True, 1.2), (True, None), (False, False)]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_int")


class TestIsFloat(unittest.TestCase):
    def setUp(self):
        self.cls = IsFloat
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in ["E", None, 1.2, 0, "True", "False", {}, []]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [(True, 2.2), (False, "21.2"), (False, 2)]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (True, {}),
            (True, 1000),
            (True, None),
            (True, "21.2"),
            (True, False),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_float")


class TestIsNumber(unittest.TestCase):
    def setUp(self):
        self.cls = IsNumber
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        # combinations of IsFloat and IsInt
        for value in [
            2.2,
            2,
        ]:
            instance = self.cls(True)
            self.assertTrue(instance.does_pass(value))

        for value in [{}, None, False, True, "weqe", "2.25", "2"]:
            instance = self.cls(True)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_number")


class TestIsGreaterThanEq(unittest.TestCase):
    def setUp(self):
        self.cls = IsGreaterThanEq
        super().setUp()

    def test_is_valid(self):
        for v in [5, 2.6, 5000, 100.555]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            "True",
            "False",
            True,
            False,
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (4, 4),
            (1000, 1001),
            (10.0, 10),
            (10.001, 10.01),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (4, 3.999),
            (1000, 999.005),
            (10.01, 10),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_greater_than_eq")


class TestIsIsLowerThanEq(unittest.TestCase):
    def setUp(self):
        self.cls = IsLowerThanEq
        super().setUp()

    def test_is_valid(self):
        for v in [5, 2.6, 5000, 100.555]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            "True",
            "False",
            True,
            False,
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for expected, value in [
            (4, 3.999),
            (1000, 999.005),
            (10.01, 10),
            (4, 4.0),
            (4, 4),
        ]:
            instance = self.cls(expected)
            self.assertTrue(instance.does_pass(value))

        for expected, value in [
            (1000, 1001),
            (10.0, 10.00001),
            (10.001, 10.01),
        ]:
            instance = self.cls(expected)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_lower_than_eq")


class TestIsHttp(unittest.TestCase):
    def setUp(self):
        self.cls = IsHttp
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for value in [
            "http://github.com",
            "http://gitlab.com",
            "http://website.something.tn",
            "http://internal.website.something.com.eu",
            #
            "https://github.com",
            "https://gitlab.com",
            "https://website.something.tn",
            "https://internal.website.something.com.eu",
        ]:
            instance = self.cls(True)
            self.assertTrue(instance.does_pass(value))

        for value in [
            [],
            {},
            None,
            False,
            True,
            "weqe",
            "2.25",
            "2",
            "http://githubcom/",
            "htt://gitlab.com",
            "http//gitlab.com",
            "htt:/gitlab.com",
            "http://website.something.$",
            "http://internal.*.something.com.eu",
        ]:
            instance = self.cls(True)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_http")


class TestIsIpv4(unittest.TestCase):
    def setUp(self):
        self.cls = IsIpv4
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for value in [
            "192.168.0.1",
            "10.0.0.1",
            "172.16.0.1",
            "203.0.113.0",
            "127.0.0.1",
        ]:
            instance = self.cls(True)
            self.assertTrue(instance.does_pass(value))

        for value in [
            [],
            {},
            None,
            False,
            True,
            "weqe",
            "2.25",
            "2",
            "http://githubcom/",
            "htt://gitlab.com",
            "http//gitlab.com",
            "htt:/gitlab.com",
            "http://website.something.$",
            "http://internal.*.something.com.eu",
            "http://github.com",
            "http://gitlab.com",
            "http://website.something.tn",
            "http://internal.website.something.com.eu",
            "1278.0.0.1",
            "12.d.0.1",
        ]:
            instance = self.cls(True)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_ipv4")


class TestIsIpv6(unittest.TestCase):
    def setUp(self):
        self.cls = IsIpv6
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for value in [
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "2606:4700:4700::1111",
            "fd12:3456:7890:abcd:ef01:2345:6789:abcd",
            "2001:0db8::ff00:0042:8329",
            "::1",
        ]:
            instance = self.cls(True)
            self.assertTrue(instance.does_pass(value))

        for value in [
            [],
            {},
            None,
            False,
            True,
            "weqe",
            "2.25",
            "2",
            "http://githubcom/",
            "htt://gitlab.com",
            "http//gitlab.com",
            "htt:/gitlab.com",
            "http://website.something.$",
            "http://internal.*.something.com.eu",
            "http://github.com",
            "http://gitlab.com",
            "http://website.something.tn",
            "http://internal.website.something.com.eu",
            "1278.0.0.1",
            "12.d.0.1",
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334:extra",  # Too many groups
            "2606:4700:4700:::1111",  # Double colons
            "fd12:3456:7890:abcd:ef01::2345::6789:abcd",  # Double colons within a group
            "2001:0db8::ff00::0042:8329",  # Double colons without compression
            "127.0.0.1",  # IPv4 address (not IPv6)
            "NotAnIPAddress Dummy",  # Invalid format
        ]:
            instance = self.cls(True)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_ipv6")


class TestIsIsEmail(unittest.TestCase):
    def setUp(self):
        self.cls = IsEmail
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for value in [
            "john.doe@example.com",
            "jane.smith12345@gmail.com",
            "info@company-name.org",
            "support@my-website.co.uk",
            "contact_us@subdomain.example.net",
        ]:
            instance = self.cls(True)
            self.assertTrue(instance.does_pass(value))

        for value in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
            "john.doe@example",  # Missing top-level domain
            "jane.smith12345.gmail.com",  # Missing "@" symbol
            "@company-name.org",  # Missing local part
            "support@.co.uk",  # Empty domain
            "contact@subdomain..net",  # Double dot in domain
            "invalid_email_address",  # No "@" symbol
            "user@invalid_domain@com",  # Multiple "@" symbols
            "user@.example.com",  # Empty local part
        ]:
            instance = self.cls(True)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_email")


class TestIsIsUuid(unittest.TestCase):
    def setUp(self):
        self.cls = IsUuid
        super().setUp()

    def test_is_valid(self):
        for v in [True, False]:
            instance = self.cls(v)
            self.assertTrue(instance.is_valid(v))

        for v in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
        ]:
            self.assertRaises(ValueUnassignableToDescription, self.cls, v)

    def test_does_pass(self):
        for value in [
            "550e8400-e29b-41d4-a716-446655440000",
            "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "9e107d9d-12b1-4efc-9e88-df2c99bcb8dd",
        ]:
            instance = self.cls(True)
            self.assertTrue(instance.does_pass(value))

        for value in [
            "E",
            None,
            1.2,
            0,
            "True",
            "False",
            {},
            [],
            "not-a-uuid",
            "550e8400e29b41d4a716446655440000",  # Missing hyphens
            "g47ac10b-58cc-4372-a567-0e02b2c3d479",  # Invalid character "g"
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8!",  # Special character "!"
            "9e107d9d-12b1-4efc-9e88-df2c99bcb8dd0000",  # Extra characters
        ]:
            instance = self.cls(True)
            self.assertFalse(instance.does_pass(value))

    def test_get_name(self):
        self.assertEqual(to_snake_case(self.cls.__name__), "is_uuid")


if __name__ == "__main__":
    unittest.main()
