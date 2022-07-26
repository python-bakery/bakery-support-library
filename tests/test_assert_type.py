from bakery import assert_type, student_tests
import unittest
import sys
from tests.helper_methods import captured_output, regex_test_case

Player = {'status': str, 'health': int}
Location = {'about': str, 'neighbors': [str]}
Thing = {'name': str, 'grabbable?': bool}
World = {'player': Player, 'locations': {str: Location}, 'stuff': [Thing]}

class TestAssertType(unittest.TestCase):
    @regex_test_case()
    def test_int_is_int(self):
        return assert_type(5, int)

    @regex_test_case()
    def test_str_is_str(self):
        return assert_type("5", str)

    @regex_test_case()
    def test_bool_is_bool(self):
        return assert_type(True, bool)

    @regex_test_case()
    def test_float_is_float(self):
        return assert_type(5.0, float)

    @regex_test_case()
    def test_int_is_float(self):
        return assert_type(5, float)

    @regex_test_case("value was the wrong type. Expected type was 'integer', but actual value was 5.0 ('float').")
    def test_float_is_not_int(self):
        return assert_type(5.0, int)

    @regex_test_case("value was the wrong type. Expected type was 'boolean', but actual value was 1 ('integer').")
    def test_bool_is_not_int(self):
        return assert_type(1, bool)

    @regex_test_case("value was the wrong type. Expected type was 'integer', but actual value was True ('boolean').")
    def test_int_is_not_bool(self):
        return assert_type(True, int)

    @regex_test_case("value was the wrong type. Expected type was 'string', but actual value was 5 ('integer').")
    def test_int_is_not_str(self):
        return assert_type(5, str)

    @regex_test_case("value was the wrong type. Expected type was 'integer', but actual value was None ('NoneType').")
    def test_none_is_not_int(self):
        return assert_type(None, int)

    @regex_test_case("value was the wrong type. Expected type was 'string', but actual value was None ('NoneType').")
    def test_none_is_not_str(self):
        return assert_type(None, str)

    @regex_test_case("value was the wrong type. Expected type was 'integer', but actual value was [1, 2, 3] ('list').")
    def test_list_ints_is_not_int(self):
        return assert_type([1, 2, 3], int)

    @regex_test_case("value was the wrong type. Expected type was 'list', but actual value was 3 ('integer').")
    def test_int_is_not_list(self):
        return assert_type(3, list)

    @regex_test_case("value was the wrong type. Expected type was 'list', but actual value was 3 ('integer').")
    def test_int_is_not_list_ints(self):
        return assert_type(3, [int])

    @regex_test_case("value[0] was the wrong type. Expected type was 'list', but actual value was 1 ('integer').")
    def test_list_ints_is_not_list_of_list_ints(self):
        return assert_type([1,2,3], [[int]])

    @regex_test_case("value[2] was the wrong type. Expected type was 'integer', but actual value was '3' ('string').")
    def test_wrong_element_inside_list(self):
        return assert_type([1, 2, "3"], [int])

    @regex_test_case("the value was missing the key 'fruit', but there was the key 'banana'.")
    def test_missing_keys(self):
        Store = {'fruit': str}
        return assert_type({'banana': 'fruit'}, Store)

    @regex_test_case("the value was missing the key 'fruit', and there were no keys at all.")
    def test_missing_keys_no_others(self):
        Store = {'fruit': str}
        return assert_type({}, Store)

    @regex_test_case("the value had all the correct keys ('fruit', 'price'), but also had these unexpected keys: 'banana', 'dogs'")
    def test_extra_keys(self):
        Store = {'price': int, 'fruit': str}
        return assert_type({'banana': 'fruit', 'price': 3, 'dogs': 27, 'fruit': 'banana'}, Store)

    @regex_test_case("the value had a wrong type for a key. Expected type of all keys was 'string', but there was the key 44 ('integer').")
    def test_wrong_key_type_homogenous(self):
        Prices = {str: int}
        return assert_type({'fruit': 27, 'apple': 22, 44: 'pineapple'}, Prices)

    @regex_test_case("the value['fruit'] was the wrong type. Expected type was 'integer', but actual value was 'banana' ('string').")
    def test_bad_key_value_type(self):
        Store = {'fruit': int}
        return assert_type({'fruit': 'banana'}, Store)

    @regex_test_case("the value['fruit'] was the value '3' ('integer'). However, that's "
                     "not important because the expected type (3) doesn't make sense! The "
                     "type definition should not have literal values like 3 in it, only types "
                     "(like int). The literal values go into instances of the type.")
    def test_literals_in_type(self):
        Store = {'fruit': 3}
        return assert_type({'fruit': 3}, Store)

    @regex_test_case()
    def test_heavily_nested_example(self):
        return assert_type({'player': {'status': 'playing', 'health': 47},
                            'locations': {'first': {'about': 'First area', 'neighbors': ['second']},
                                          'second': {'about': 'Second area', 'neighbors': ['first']}},
                            'stuff': [{'name': 'Broom', 'grabbable?': True},
                                      {'name': 'Lava', 'grabbable?': False}]}, World)

    @regex_test_case("the value['locations']['second'] was missing the key 'neighbors', but there were the keys "
                     "'about' and 'neighbor'.")
    def test_heavily_nested_example_key_typo(self):
        return assert_type({'player': {'status': 'playing', 'health': 47},
                            'locations': {'first': {'about': 'First area', 'neighbors': ['second']},
                                          'second': {'about': 'Second area', 'neighbor': ['first']}},
                            'stuff': [{'name': 'Broom', 'grabbable?': True},
                                      {'name': 'Lava', 'grabbable?': False}]}, World)

    @regex_test_case("the value['player']['status'] was the wrong type. Expected type was 'string', but actual value "
                     "was True ('boolean').")
    def test_heavily_nested_example_wrong_type(self):
        return assert_type({'player': {'status': True, 'health': 47},
                            'locations': {'first': {'about': 'First area', 'neighbors': ['second']},
                                          'second': {'about': 'Second area', 'neighbors': ['first']}},
                            'stuff': [{'name': 'Broom', 'grabbable?': True},
                                      {'name': 'Lava', 'grabbable?': False}]}, World)

    @regex_test_case("the value['locations']['first']['neighbors'][0] was the wrong type. Expected type was 'string', "
                     "but actual value was {'about': 'Second area', 'neighbors': ['first']} ('dictionary').")
    def test_heavily_nested_example_wrong_type_in_list(self):
        first = {'about': 'First area', 'neighbors': []}
        second = {'about': 'Second area', 'neighbors': ['first']}
        first['neighbors'].append(second)
        return assert_type({'player': {'status': "playing", 'health': 47},
                            'locations': {'first': first,
                                          'second': second},
                            'stuff': [{'name': 'Broom', 'grabbable?': True},
                                      {'name': 'Lava', 'grabbable?': False}]}, World)

    def test_traceback_shim(self):
        # Mock out traceback
        import importlib
        old = sys.modules.copy()
        sys.modules['traceback'] = None
        import bakery

        with captured_output() as (out, err):
            self.assertTrue(bakery.assert_type(5, int))
        self.assertEqual(out.getvalue().strip(), "TEST PASSED")

        with captured_output() as (out, err):
            self.assertFalse(bakery.assert_type(5, str))
        self.assertEqual(out.getvalue().strip(
        ), "FAILURE, value was the wrong type. Expected type was 'string', but actual value was 5 ('integer').")

        # Restore traceback
        sys.modules['traceback'] = old['traceback']

    def test_report(self):
        student_tests.reset()
        with captured_output() as (out, err):
            assert_type(5, int)
            assert_type(5, str)
            assert_type("3", int)
            assert_type("3", str)
            assert_type("3", bool)
        self.assertEqual(student_tests.tests, 5)
        self.assertEqual(student_tests.failures, 3)
        self.assertEqual(student_tests.successes, 2)


if __name__ == '__main__':
    unittest.main(buffer=False)
