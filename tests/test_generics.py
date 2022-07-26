from bakery import *

from contextlib import contextmanager
from io import StringIO
import unittest
import sys
from tests.helper_methods import captured_output, generate_regex


class TestGenerics(unittest.TestCase):
    def test_generics(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_type([5], list[int]))
        self.assertRegex(out.getvalue().strip(), generate_regex(True, "self.assertTrue(assert_equal([5], list[int]))"))
