Bakery Support Library
======================

A collection of tools to help students write code, meant for the Python Bakery CS1 curriculum.

For now, mostly improved assertions.

Installation
============

Install from PyPi::
    
    pip install bakery

Or install from: https://github.com/python-bakery/bakery-support-library

Examples
========

.. code-block:: python
    
    from bakery import assert_equal
    
    def halve(number):
        return number / 2
    
    # Correctly handles floating points
    assert_equal(halve(10), 5.0)
    
Output
======

This library will print a message to STDOUT if an assertion fails, and returns True/False. It does not raise an exception or print to STDERR.

Supported Types
===============

* Numbers: strictly compares numeric types, but allows floats to have imprecision, defaults to 4 places
* Strings: can strictly compare types with exact_strings=True, but defaults to ignore whitespace on newlines and capitalization
* Lists, Tuples: applies same rules to inner types as container types
* Sets, Frozensets, Dictionary: checks that all elements are contained in both, in any order
* Generators: functions like `enumerate` and `.items()` that produce generators are converted to lists and sets (as appropriate), then checked that their values match.
* Other types should work as well, but require that the result of `type` match, and that `x == y`
