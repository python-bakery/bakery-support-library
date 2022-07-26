from bakery import assert_false
import unittest
import sys
from helper_methods import captured_output, generate_regex


class TestAssertFalse(unittest.TestCase):
    def test_non_bool(self):
        with captured_output() as (out, err):
            self.assertFalse(assert_false(5))
        self.assertRegex(out.getvalue().strip(), generate_regex(
            False, "self.assertFalse(assert_false(5)), predicted answer was False ('bool'), computed answer was 5 ('int'). You attempted to compare unrelated data types."))
        with captured_output() as (out, err):
            self.assertFalse(assert_false(10+3))
        self.assertRegex(out.getvalue().strip(), generate_regex(
            False, "self.assertFalse(assert_false(10+3)), predicted answer was False ('bool'), computed answer was 13 ('int'). You attempted to compare unrelated data types."))
        #with captured_output() as (out, err):
        #    self.assertFalse(assert_false("hi" + " there!"))
        #self.assertRegex(out.getvalue().strip(), generate_regex(
        #    False, "self.assertFalse(assert_false(\"hi\" + \" there!\")), predicted answer was False ('bool'), computed answer was \'hi there!\' ('str'). You attempted to compare unrelated data types."))

    def test_bool(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_false(False))
        self.assertRegex(out.getvalue().strip(), generate_regex(
            True, "self.assertTrue(assert_false(False))"))
        with captured_output() as (out, err):
            self.assertFalse(assert_false(True))
        self.assertRegex(out.getvalue().strip(), generate_regex(
            False, "self.assertFalse(assert_false(True))"))

    def test_traceback_shim(self):
        # Mock out traceback
        import importlib
        old = sys.modules.copy()
        sys.modules['traceback'] = None
        import bakery

        with captured_output() as (out, err):
            self.assertTrue(bakery.assert_false(False))
        self.assertEqual(out.getvalue().strip(), "TEST PASSED")

        with captured_output() as (out, err):
            self.assertFalse(bakery.assert_false(5))
        self.assertEqual(out.getvalue().strip(
        ), "FAILURE, predicted answer was False ('bool'), computed answer was 5 ('int'). You attempted to compare unrelated data types.")

        # Restore traceback
        sys.modules['traceback'] = old['traceback']


if __name__ == '__main__':
    unittest.main(buffer=False)
