from __future__ import annotations

import unittest

from env_should_be.utils import Number


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertEqual((Number(5) + Number(6)).value, 11)


if __name__ == '__main__':
    unittest.main()
