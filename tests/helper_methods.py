import re
import sys
import os
from functools import wraps
from contextlib import contextmanager
from io import StringIO
import inspect

bakery_library = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, bakery_library)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def generate_regex(successOrFailure: bool, message: str) -> str:
    regex: str = r"TEST PASSED - \[line \d+\] " if successOrFailure else r"FAILURE - \[line \d+\] "
    regex += re.escape(message)
    return regex



def regex_test_case(extendedMessage=""):
    successOrFailure = not bool(extendedMessage)
    if extendedMessage:
        extendedMessage = ", "+extendedMessage
    def decorator_test(method):
        @wraps(method)
        def wrapper_test(self, *args, **kwargs):
            new_out, new_err = StringIO(), StringIO()
            old_out, old_err = sys.stdout, sys.stderr
            try:
                sys.stdout, sys.stderr = new_out, new_err
                result = method(self, *args, **kwargs)
            finally:
                sys.stdout, sys.stderr = old_out, old_err
            source_code = [line.strip() for line in inspect.getsource(method).split("\n") if line.strip()]
            final_line = source_code[-1]
            actual_output = new_out.getvalue().strip()
            regex_test = generate_regex(successOrFailure, final_line+extendedMessage)
            self.assertRegex(actual_output, regex_test)
            if successOrFailure:
                self.assertTrue(result)
            else:
                self.assertFalse(result)
            return result
        return wrapper_test
    return decorator_test
