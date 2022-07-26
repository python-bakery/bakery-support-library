try:
    from dataclasses import dataclass
except ImportError:
    pass
from bakery.assertions import (assert_equal, assert_type,
                                assert_true, assert_false,
                                QUIET, student_tests)